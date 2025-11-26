#!/usr/bin/env python3
import sys
import os
import re
import random
from qtex.common.lib_qtex import quellecle,readqtex,default_values_before 

# --------------------------------------------------------------------------
def newline(size="0.2cm"):
    if len(size) :
        return f"\\\\[{size}]\n"
    else:
        return f"\n"
# --------------------------------------------------------------------------
def benv(name):
    return "\\begin{"f"{name}""}"+newline('')
# --------------------------------------------------------------------------
def eenv(name):
    return "\\end{"f"{name}""}"+newline('')
# --------------------------------------------------------------------------
def cmd(name):
    return f"\\{name}"
# --------------------------------------------------------------------------
def macro(name,value):
    return f"{cmd(name)}{'{'}{value}{'}'}"
# --------------------------------------------------------------------------
def lans(answ_text,grad,index,corrige=True):
    out="\\indent\\textbf{"f"{chr(index+65)}.""}"
    if corrige :
        if float(grad) > 0. :
            out+=" {\color{OliveGreen}" f" {answ_text} " " {\\large\\cmark}}\\newline"
        else:
            out+=" {\color{BrickRed}  " f" {answ_text} " " {\\large\\xmark}}\\newline"
        return out
    else:
        return out+f" {answ_text} "+"\\newline\hfill"
    return out
# --------------------------------------------------------------------------
def multichoice_to_latex(info,outfile,corrige=True):
    outfile.write(macro("question",info["Q"])+newline())
    answ=list(zip(info['ANSW_TEXT'],info['ANSW_GRAD']))
    random.shuffle(answ)
    for k, (answ_txt,answ_grad) in enumerate(answ):
        outfile.write(lans(answ_txt,answ_grad,k,corrige=True)+newline(""))
# --------------------------------------------------------------------------
def tikz_matching(k,subq,answ_text,gw=80,dw=80):
    #print(k,G,D)
    if k == 0 :
        return \
        f"""
        {cmd('node')}[text width={gw}mm,align=left] (a1) at (0,0) {"{"} {macro("textbf",chr(65+k)+'.')} {subq} {"}"};
        {cmd('node')} (b1) at ($(a1.east)+(1,0)$) {{}};
        {cmd('node')} (c1) at ($(b1.east)+(2,0)$) {{}};
        {cmd('draw')}[thick,outer sep=8mm] (b1) circle(0.5ex);
        {cmd('draw')}[thick,outer sep=8mm] (c1) circle(0.5ex);
        {cmd('node')}[text width={dw}mm,align = right] (d1) at ($(c1.east)+(6,0)$) {"{"} {macro("textbf",str(k+1)+'.')} {answ_text} {"}"};"""
    else:
        return \
        f"""
        {cmd('node')}[text width={gw}mm,below=0.75cm of a{k}.center,anchor=center,align=left] (a{k+1}) {"{"} {macro("textbf",chr(65+k)+'.')} {subq} {"}"};
        {cmd('node')}[below=0.75cm of b{k}.center,anchor=center] (b{k+1}) {{}};
        {cmd('node')}[below=0.75cm of c{k}.center,anchor=center] (c{k+1}) {{}};
        {cmd('draw')}[thick,outer sep=8mm] (b{k+1}) circle(0.5ex);
        {cmd('draw')}[thick,outer sep=8mm] (c{k+1}) circle(0.5ex);
        {cmd('node')}[below=0.75cm of d{k}.center,anchor=center,text width={dw}mm,align = right] (d{k+1}) {"{"} {macro("textbf",str(k+1)+'.')} {answ_text} {"}"};"""
# --------------------------------------------------------------------------
def tikz_relie(indices):
    return "\n".join([ f"{cmd('draw')}[very thick] (b{k+1}) -- (c{i+1});" for k,i in enumerate(indices)])
# --------------------------------------------------------------------------
def matching_to_latex(info,outfile,corrige=True):
    outfile.write(macro("question",info["Q"]))
    outfile.write(cmd('indent')+macro('resizebox','\linewidth')+'{!}{%'+newline(""))
    outfile.write(benv("tikzpicture"))
    maxwidth_sub_q, maxwidth_answ_text = (max(map(len,info['SUB_Q']))+8)*1.51323 , (max(map(len,info['ANSW_TEXT']))+8)*1.51323
    indices=[k for k in range(len(info['SUB_Q']))]
    shuff=list(zip(info['ANSW_TEXT'],indices))
    random.shuffle(shuff)
    shuff_answ_text,indices=zip(*shuff)
    for k,(subq,answ_text) in enumerate(zip(info['SUB_Q'],shuff_answ_text)) :
        outfile.write(tikz_matching(k,subq,answ_text,gw=maxwidth_sub_q,dw=maxwidth_answ_text))
    if corrige:
        outfile.write(tikz_relie(indices))
    outfile.write(eenv("tikzpicture"))
    outfile.write('}')
# --------------------------------------------------------------------------
def coderunner_to_latex(info,outfile,numlines=18):
    outfile.write(macro("question",info["Q"])+newline())
    outfile.write(benv("tikzpicture"))
    outfile.write(cmd('draw')+"[ultra thick,inner sep=0] (0,0) rectangle (\linewidth,"+f"{numlines*0.5}cm)"+";\n")
    outfile.write(cmd('draw')+"[gray!40] (0,0) grid[step=0.5cm](\linewidth,"+f"{numlines*0.5}cm)"+";\n")
    outfile.write(eenv("tikzpicture"))
                #\begin{tikzpicture}
                #    \draw[ultra thick,inner sep=0] (0,0) rectangle (\linewidth,\sizegrid);
                #    \draw[gray!40] (0,0) grid[step=0.5cm](\linewidth,\sizegrid);
                #\end{tikzpicture}
# --------------------------------------------------------------------------
def qtex_to_latex(info,outfile):
    match info["TYPE"]:
        case "multichoice":
            multichoice_to_latex(info,outfile)
        case "matching":
            matching_to_latex(info,outfile)
        case "coderunner":
            coderunner_to_latex(info,outfile)
        case _:
            print(f"{info['TYPE']}->latex not possible")
#--------------------------------------------------------------------------------------------------
# main parsing function
def parsing():
    import os
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input', nargs='+', type=argparse.FileType('r'),
                        default=sys.stdin,help='input files (on single or a set)',required=True)
    parser.add_argument('-o','--output', nargs='?', type=argparse.FileType('a'),
                        default=sys.stdout, help='output file or stdout')
    args = parser.parse_args()

    output=args.output
    if output.name !="<stdout>":
        output.seek(0,0)
        output.truncate()

    path=os.path.dirname(args.input[0].name)+'/'
    filespath=args.input
    return path,filespath,output
#--------------------------------------------------------------------------------------------------
def html_to_tex(info):
    filters=[]
    filters+=[lambda t : re.sub(r"{", r"\{", t)]
    filters+=[lambda t : re.sub(r"}", r"\}", t)]
    filters+=[lambda t : re.sub(r"<tt>(.*?)</tt>", r"\\texttt{\1}", t)]
    filters+=[lambda t : re.sub(r"\$", r"\\$", t)]
    filters+=[lambda t : re.sub(r"&dollar;", r"\\\$", t)]
    for key in info :
        for f in filters:
            if info[key] is not None :
                if isinstance(info[key],list):
                    if all(e is not None for e in info[key]) :
                        info[key]=list(map(f,info[key]))
                else:
                    info[key]=f(info[key])
#--------------------------------------------------------------------------------------------------
def main():
    path,filespath,outfile=parsing()
    for file in filespath :
        if file.name[-13:]=="category.qtex" : continue
        print(file.name,file=sys.stderr,end=' ')
        info=readqtex(path,file)
        html_to_tex(info)
        print(f"\n\ttype : {info['TYPE']}\n\tname : {info['NAME']}\n\ttags : {info['TAGS']} ",file=sys.stderr)
        qtex_to_latex(info,outfile)

