"""Tokenizer du format qtex : syntaxe uniquement (clés, blocs, numéros de ligne)."""
import re
from dataclasses import dataclass

from .format_qtex import entrees

_END = re.compile(r"#END(?:[ \t]+(\S+))?[ \t]*")
_KEY = re.compile(r"#([A-Z][A-Z0-9_]*)(?:[ \t](.*))?")

@dataclass(frozen=True)
class Entry:
    key: str          # clé telle qu'écrite, sans le '#', ex. "ANSW_TEXT_LONG"
    value: str
    long: bool        # True si c'était un bloc #KEY ... #END KEY
    line_start: int   # numéro de ligne (à partir de 1) de la clé
    line_end: int     # ligne du #END pour un bloc, sinon line_start

    def __str__(self):
        return f"#{self.key} : '{self.value}' from l{self.line_start} to l{self.line_end}"


class ParseError(ValueError):
    def __init__(self, line: int, code: str, message: str):
        super().__init__(f"ligne {line}: {message}")
        self.line = line
        self.code = code      # unclosed_block, orphan_end, mismatched_end, stray_line
        self.message = message
    def __str__(self):
        return f"{self.code}  {self.message}"


def _block_value(lines: list[str]) -> str:
    # même découpage que l'ancien rmnewlineboth(...).rstrip()
    if lines and lines[0] == "":
        lines = lines[1:]
    return "\n".join(lines).rstrip()

# prend une chaine et retourne les entrées et erreurs qtex
def tokenize(text: str) -> tuple[list[Entry], list[ParseError]]:
    entries: list[Entry] = []
    errors: list[ParseError] = []
    open_key = None
    open_line = 0
    buf: list[str] = []

    for n, line in enumerate(text.lstrip("\ufeff").splitlines(), start=1):
        if open_key is not None:                      # à l'intérieur d'un bloc long
            m = _END.fullmatch(line)
            if m is None:
                buf.append(line)                      # texte brut, rien n'est interprété
                continue
            if m.group(1) != open_key:
                errors.append(ParseError(
                    n, "mismatched_end",
                    f"#END {m.group(1) or ''} ferme le bloc #{open_key} ouvert ligne {open_line}"))
            entries.append(Entry(open_key, _block_value(buf), True, open_line, n))
            open_key = None
            continue

        if not line.strip():
            continue
        m = _END.fullmatch(line)
        if m is not None:
            errors.append(ParseError(n, "orphan_end", f"#END {m.group(1) or ''} sans bloc ouvert"))
            continue
        m = _KEY.fullmatch(line)
        if m is None:
            errors.append(ParseError(n, "stray_line", "ligne hors entrée, ignorée"))
            continue
        key, rest = m.group(1), m.group(2)
        if entrees.get(key, {}).get("long"):          # ouverture d'un bloc
            open_key, open_line = key, n
            buf = [] if rest is None else [rest]
        else:                                         # clé courte
            entries.append(Entry(key, (rest or "").rstrip(), False, n, n))

    if open_key is not None:
        errors.append(ParseError(open_line, "unclosed_block",
                                 f"bloc #{open_key} jamais fermé (#END {open_key} attendu)"))
    return entries, errors

def main(file):
    out=file.read().strip()
    entries,errors=tokenize(out)
    print(f"{len(entries)} entries found")
    print(f"ParseError: {len(errors)}")
    for error in errors :
        print(error)
