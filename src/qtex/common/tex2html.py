#!/usr/bin/python3
import re
# -------------------------------------------------------------------------------------------------
def replace_texttt(s):
    pattern = re.compile(r'\\texttt\{')
    while True:
        m = pattern.search(s)
        if not m:
            break
        # position juste après '\texttt{'
        start = m.end()
        depth = 1
        i = start
        while i < len(s) and depth > 0:
            if s[i] == '{':
                depth += 1
            elif s[i] == '}':
                depth -= 1
            i += 1
        if depth != 0:
            # accolade fermante non trouvée : on arrête (ou on choisit de laisser tel quel)
            break
        # i-1 est la position de la '}' fermante
        content = s[start:i-1]
        # reconstruire la chaîne en remplaçant la portion entière m.start():i
        s = s[:m.start()] + f"<tt>{content}</tt>" + s[i:]
    return s
# -------------------------------------------------------------------------------------------------
def replace_outside_tt(match):
    content = match.group(0)
    # Replace \$ with $ in the match
    return re.sub(r"\\\$", "$", content)

def gen_filters() :
    filters=[]
    filters+=[lambda t : re.sub(r"\\\,",r""  ,t)]                                    # \, -> null (enlever les espaces)
    filters+=[lambda t : re.sub(r"\\\&",r"&amp;",t)]                                 # \& -> &
    filters+=[lambda t : re.sub(r"\{\}",r""  ,t)]                                    # {} -> null (enlever les {})
    filters+=[lambda t : re.sub(r"\\\{",r"OPEN_CURLY_BRACKET",t)]                    # \{ -> OPEN_CURLY_BRACKET
    filters+=[lambda t : re.sub(r"\\\}",r"CLOSE_CURLY_BRACKET",t)]                   # \} -> CLOSE_CURLY_BRACKET
    filters+=[lambda t : re.sub(r"\\\#",r"#"  ,t)]                                   # \# -> #
    filters+=[lambda t : re.sub(r"\\\$",r"&dollar;" ,t)]                             # \$ -> $
    filters+=[lambda t : re.sub(r"\$",r"&dollar;" ,t)]                               # \$ -> $
    filters+=[lambda t : re.sub(r"\\\%",r"%"  ,t)]                                   # \% -> %   
    filters+=[lambda t : re.sub(r"\\\!",r""  ,t)]                                    # \! -> null enlever
    filters+=[lambda t : re.sub(r"\\_",r"_"  ,t)]                                    # \_ -> _
    filters+=[lambda t : re.sub(r"\\textasciitilde",r"~",t)]                         # \textasciitilde -> ~
    filters+=[lambda t : re.sub(r"\\textquotesingle",r"'",t)]                        # \textquotesingle -> '
    filters+=[lambda t : re.sub(r"\\textbackslash",r"\\",t)]                         # \\textbackslash -> \  
    filters+=[lambda t : re.sub(r"\\textasciicircum",r"^",t)]                        # \textasciicircum -> ^
    filters+=[lambda t : re.sub(r"\\\tr",r"\'",t)]                                   # \tr -> ' (raccourci de fmv) 
    filters+=[lambda t : re.sub(r"\\textbf\{([^}]*)\}",r"<strong>\1</strong>",t)]    # \textbf{group} -> <strong>groupe</strong>
    filters+=[lambda t : re.sub(r"\\verb\?([^\?]*)\?",r"<tt>\1</tt>"  ,t)]           # \verb?group? -> <tt>group</tt>
    #filters+=[lambda t : re.sub(r"\\texttt\{([^{}*]?)\}", r"<tt>\1</tt>", t)]       # \texttt{group} -> <tt>group</tt>
    #filters+=[lambda t : re.sub(r"\\texttt\{(.*?)\}", r"<tt>\1</tt>", t)]           # \texttt{group} -> <tt>group</tt>
    filters+=[lambda t : replace_texttt(t)]
    filters+=[lambda t : re.sub(r"\\path\{(.*?)\}", r"<tt>\1</tt>", t)]              # \path{group} -> <tt>group</tt>
    filters+=[lambda t : re.sub(r"\\emph\{([^}]*)\}",r"<em>\1</em>"  ,t)]            # \emph{group} -> <em>group</em>
    filters+=[lambda t : re.sub(r"OPEN_CURLY_BRACKET",r"{"  ,t)]
    filters+=[lambda t : re.sub(r"CLOSE_CURLY_BRACKET",r"}"  ,t)]
    #filters+=[lambda t : re.sub(r"(<tt>.*?</tt>)|([^<]*)", lambda m: m.group(1) or replace_outside_tt(m), t)]
    return filters

def main(file):
    out=file.read().strip()
    filters=gen_filters()
    for f in filters :
        out=f(out)
    print(out)
