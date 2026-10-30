import sys
from pathlib import Path

from .format_qtex import types_with_requirements, same_number, infos, entrees
from .qtex_parser import tokenize, ParseError

# --------------------------------------------------------------------
# indentation LaTeX/XML (déplacée depuis string_.py, utilisée par qtex2xml)
def tab(k):
    return k * "\t"

# --------------------------------------------------------------------
# (clé d'info, variantes présentes dans le fichier) pour un élément de infos :
#   'Q'            -> ('Q', ['Q'])
#   ('Q','Q_LONG') -> ('Q', ['Q', 'Q_LONG'])
def _variants(spec):
    if isinstance(spec, tuple):
        return spec[0], list(spec[1:])
    return spec, [spec]

# --------------------------------------------------------------------
# Valeurs par défaut ; entries = sortie de tokenize(), pas le texte brut.
def default_values_before(entries, filename=None):
    info = {}
    type_entries = [e for e in entries if e.key == "TYPE"]
    if not type_entries:
        raise ParseError(0, "entrée #TYPE absente", filename)
    info["TYPE"] = type_entries[0].value
    qtype = info["TYPE"]

    def values(*keys):
        return [e.value for e in entries if e.key in keys]

    # clé canonique -> toutes ses variantes (courte + longue(s))
    var = {}
    for spec in infos.get(qtype, []) + infos["question"]:
        ik, vs = _variants(spec)
        var.setdefault(ik, []).extend(vs)

    def has_key(g):
        return bool(values(*var.get(g, [g])))

    def count_key(g):
        return len(values(*var.get(g, [g])))

    info["Q_IMG"] = ""
    info["EXTRA_Q_LONG"] = ""

    m = 1
    if qtype in types_with_requirements:
        present = [g for g in same_number[qtype] if has_key(g)]
        if not present:
            raise ParseError(1,
                             f"clés manquantes pour {qtype} : "
                             f"au moins une de {same_number[qtype]} est requise",
                             filename)
        m = count_key(present[0])

    match qtype:
        case "truefalse":
            if not has_key("ANSW_FBACK"): info["ANSW_FBACK"] = [None] * 2
            if not has_key("ANSW_TEXT"):  info["ANSW_TEXT"]  = [""] * 2
            if not has_key("ANSW_GRAD"): info["ANSW_GRAD"]  = ["0"] * 2
            if not has_key("ANSW_IMG"):  info["ANSW_IMG"]   = [""] * 2
        case "multichoice" | "numerical" | "multichoicewiris" | "shortanswerwiris" | "matching" | "shortanswer":
            if not has_key("ANSW_FBACK"): info["ANSW_FBACK"] = [None] * m
            if not has_key("ANSW_TEXT"):  info["ANSW_TEXT"]  = [""] * m
            if not has_key("ANSW_GRAD"): info["ANSW_GRAD"]  = ["0"] * m
            if not has_key("ANSW_IMG"):  info["ANSW_IMG"]   = [""] * m
        case "coderunner":
            if not has_key("CR_TYPE"):                 info["CR_TYPE"] = "python3"
            if not has_key("CR_TEMPLATE"):             info["CR_TEMPLATE"] = ""
            if not has_key("CR_ACELANG"):              info["CR_ACELANG"] = ""
            if not has_key("CR_TWIGALL"):              info["CR_TWIGALL"] = "0"
            if not has_key("CR_ISCOMBINATORTEMPLATE"): info["CR_ISCOMBINATORTEMPLATE"] = "1"
            if not has_key("CR_PENALTYREGIME"):        info["CR_PENALTYREGIME"] = "0,5,10,..."
            if not has_key("CR_CASE_ASEXAMPLE"):       info["CR_CASE_ASEXAMPLE"] = ["0"] * m
            if not has_key("CR_CASE_MARK"):            info["CR_CASE_MARK"] = ["1.0"] * m
            if not has_key("CR_CASE_EXPECTED"):        info["CR_CASE_EXPECTED"] = [""] * m
            if not has_key("CR_CASE_DISPLAY"):         info["CR_CASE_DISPLAY"] = ["SHOW"] * m
            if not has_key("CR_CASE_STDIN"):           info["CR_CASE_STDIN"] = [""] * m
            if not has_key("CR_CASE_EXTRA"):           info["CR_CASE_EXTRA"] = [""] * m
            cr_answer = values("CR_ANSWER")
            if not cr_answer:
                raise ParseError(1, "entrée #CR_ANSWER absente pour une question coderunner", filename)
            info["answerboxlines"] = str(int((cr_answer[0].count("\n") + 1) * 1.2))
    # NB : dans l'ancien code, le second 'case "matching":' (défaut SUB_Q) était
    # du code mort, jamais atteint. Déplacé ici, il s'applique réellement :
    if qtype == "matching" and not has_key("SUB_Q"):
        info["SUB_Q"] = [""] * m
    return info

# --------------------------------------------------------------------
# Range les entrées dans info, DANS L'ORDRE DU FICHIER.
def _fill(info, entries, specs):
    mapping = {}
    for spec in specs:
        ik, vs = _variants(spec)
        for v in vs:
            mapping[v] = ik
    for e in entries:
        ik = mapping.get(e.key)
        if ik is None:
            continue
        if entrees[e.key]["multiple"]:
            info.setdefault(ik, []).append(e.value)
        else:
            info[ik] = e.value      # dernier gagnant, en ordre du fichier (Q, Q_LONG…)

# --------------------------------------------------------------------
# Lecture d'un fichier au format qtex : retourne le dictionnaire info.
def readqtex(path, file):
    data = file.read()
    filename = getattr(file, "name", "<qtex>")
    try:
        entries, _errors = tokenize(data, strict=True)
        info = default_values_before(entries, filename)
    except ParseError as err:
        if err.filename is None:
            raise ParseError(err.line, err.message, filename) from None
        raise
    info["PATH"] = path
    info["ID"] = Path(filename).stem
    qtype = info["TYPE"]
    if qtype == "category":
        _fill(info, entries, infos["global"])
        return info
    _fill(info, entries, infos["global"] + infos["question"])
    if qtype == "description":
        return info
    if qtype not in infos:
        raise ParseError(1, f"type de question inconnu : {qtype}", filename)
    _fill(info, entries, infos[qtype])
    check_values_after(info)
    return info
