#!/usr/bin/env python3
import sys
import os
import argparse
import re
import random
from qtex.common.lib_qtex import quellecle,readqtex,default_values_before 
# -----------------------------------------------------------------
# join lines d'une liste
# -----------------------------------------------------------------
def concatenate(lines): return "".join(lines)
# -----------------------------------------------------------------
# applique \n à un ensemble de chaines dans une liste
# -----------------------------------------------------------------
def newlines(lines): return "\n".join(lines)
# -----------------------------------------------------------------
def newline(size="0.2cm"):
    if len(size) :
        return f"\\\\[{size}]\n"
    else:
        return f"\n"
# -----------------------------------------------------------------
# retourne \begin{env}[options]
# -----------------------------------------------------------------
def begin(env,options="",arguments=None):
    out=["\\begin{"f"{env}""}"]
    if len(options): out+=[f"[{options}]"]
    if arguments is not None: out+=[f"{{{arguments}}}"]
    return concatenate(out)
# -----------------------------------------------------------------
# retourne \end{env}
# -----------------------------------------------------------------
def end(env):
    return "\\end{"f"{env}""}"
# -----------------------------------------------------------------
# \macro[options]{value} (if semicolon=False,braces=True) 
# \macro[options] value;  (if semicolon=True,braces=False) 
# -----------------------------------------------------------------
def macro(name,value="",options=""):
    out=[f"\\{name}"]
    if len(options) : out+=["["f"{options}""]"]
    if len(value)   : out+=[f"{{{value}}}"]
    return concatenate(out)
# ------------------------------------------------------------------------------
# \draw[options] path ;
def tikz_draw(path, options=""):
    return f"{macro('draw',options=options)} {path};"
# ------------------------------------------------------------------------------
# \node[options] (name) at (pos) {content};
def tikz_node(name, pos="",content="", options=""):
    if len(pos) :
        return f"{macro('node', options=options)} ({name}) at ({pos}) {{{content}}};"
    else:
        return f"{macro('node', options=options)} ({name}) {{{content}}};"
# --------------------------------------------------------------------------
# \indent \textbf{A.} {\color{BrickRed} <réponse_incorrecte> \large\xmark}\newline
# \indent \textbf{B.} {\color{OliveGreen} <réponse_correcte< \large\cmark}\newline
def ans_to_latex(answ_text,answ_grad,answ_img,path,index,corrige=True):
    label=f"\\indent {macro('textbf',chr(index+65)+'.')}"
    grad=float(answ_grad)
    # si il n'y a pas d'image dans la réponse
    if not len(answ_img) :
        if corrige :
            color = "OliveGreen" if grad > 0 else "BrickRed"
            symbol = "\\large\\cmark" if grad > 0 else "\\large\\xmark"
            return f"{label} {{\\color{{{color}}} {answ_text} {symbol}}}\\newline"
        else:
            return f"{label} {answ_text}\\newline\\hfill"
    # s'il y a une image dans la réponse
    filepath_img,w_img,h_img = answ_img.split(" ")
    filepath_img = path+filepath_img
    img_code = f"{macro('includegraphics')}[width=0.5\\linewidth]{{{filepath_img}}}"
    if corrige and grad > 0. : 
        img_code = f"{macro('fbox')}{{{img_code}}}"
    return f"{label} {img_code}"
# --------------------------------------------------------------------------
def ans_to_frame(answ_text,answ_grad,answ_img,path,index,corrige=True):
    grad = float(answ_grad)
    if corrige :
        color = "OliveGreen" if grad > 0 else "BrickRed"
    symbol = "\\cmark" if grad > 0 else "\\xmark"
    if answ_img:
        # séparer nom fichier, largeur, hauteur
        filepath_img, w_img, h_img = answ_img.split(" ")
        filepath_img = path + filepath_img
        content = f"\\includegraphics[width=0.5\\linewidth]{{{filepath_img}}}"
    else:
        content = answ_text
    if corrige :
        correction = f"{{~{symbol}}}" 
        return f"\\item \\color{{{color}}}{{{content}}}{correction}"
    else:
        return f"\\item {{{content}}}"
# --------------------------------------------------------------------------
def write_question(info,outfile):
    if len(info["EXTRA_Q_LONG"]) :
        outfile.write(macro("question",info["Q"])+newline(""))
        outfile.write(info["EXTRA_Q_LONG"]+newline(""))
    else:
        outfile.write(macro("question",info["Q"])+newline())
# --------------------------------------------------------------------------
def description_to_latex(info,outfile):
    outfile.write(info["Q"]+newline(""))
# --------------------------------------------------------------------------
def multichoice_to_latex(info,outfile,corrige=True,shuffle=[0,1,2,4]):
    write_question(info,outfile)
    answ=list(zip(info['ANSW_TEXT'],info['ANSW_GRAD'],info['ANSW_IMG']))
    #random.shuffle(answ)
    answ=[answ[i] for i in shuffle]
    for k, (answ_txt,answ_grad,answ_img) in enumerate(answ):
        outfile.write(ans_to_latex(answ_txt,answ_grad,answ_img,info['PATH'],k,corrige=corrige)+newline(""))
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#\begin{frame}
#    \frametitle{Quiz}
#    \begin{blockWooclap}[Cours03]
#    \emph{<QUES>}
#    \begin{itemize}
#        \item \color<2->{BrickRed}{<reponse1_incorrecte>}\only<2->{~\xmark}
#        \item \color<2->{BrickRed}{<reponse2_incorrecte>}\only<2->{~\xmark}
#        \item \color<2->{OliveGreen}{<reponse3_correcte>}\only<2->{~\cmark}
#        \item \color<2->{BrickRed}{<reponse4_incorrecte>}\only<2->{~\xmark}
#    \end{itemize}
#    \end{blockWooclap}
#\end{frame}
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def multichoice_to_frame(info,outfile,**kwargs):
    wooclap=kwargs.get("wooclap_name","")
    corrige=kwargs.get("corrige",True)
    shuffle=kwargs.get("shuffle",[0,1,2,3])
    out=[begin("frame")]
    if len(wooclap) :
        out+=[begin("blockWooclap",options=wooclap)]
    else:
        out+=[begin("blockQues")]
    out+=[macro("emph",info["Q"])]
    out+=[begin("itemize")]
    answ=list(zip(info['ANSW_TEXT'],info['ANSW_GRAD'],info['ANSW_IMG']))
    #random.shuffle(answ)
    answ=[answ[i] for i in shuffle]
    for k, (answ_txt,answ_grad,answ_img) in enumerate(answ):
        out+=[ans_to_frame(answ_txt,answ_grad,answ_img,info['PATH'],k,corrige=corrige)]
    out+=[end("itemize")]
    if len(wooclap) : 
        out+=[end("blockWooclap")]
    else:
        out+=[end("blockQues")]
    out+=[end("frame")]
    outfile.write(newlines(out))
    
# --------------------------------------------------------------------------
def tikz_matching(k, subq, answ_text, gw=80, dw=80):
    if k == 0:
        label_tmp=f"{macro('textbf', chr(65+k)+'.')} {subq}"
        node_a = tikz_node(name="a1",pos="0,0",content=label_tmp,options=f"text width={gw}mm,align=left")
        node_b = tikz_node(name="b1", pos="$(a1.east)+(1,0)$", content="")
        node_c = tikz_node(name="c1", pos="$(b1.east)+(2,0)$", content="")
        draw_b = tikz_draw("(b1) circle(0.5ex)", options="thick,outer sep=8mm")
        draw_c = tikz_draw("(c1) circle(0.5ex)", options="thick,outer sep=8mm")
        label_tmp = f"{macro('textbf', str(k+1)+'.')} {answ_text}"
        node_d = tikz_node(name="d1",pos="$(c1.east)+(6,0)$",content=label_tmp,options=f"text width={dw}mm,align=right")
    else:
        # k > 0 : positions relatives aux nœuds précédents
        label_tmp = f"{macro('textbf', chr(65+k)+'.')} {subq}"
        node_a = tikz_node(name=f"a{k+1}",options=f"below=0.75cm of a{k}.center,anchor=center,text width={gw}mm,align=left",
                           content=label_tmp)
        node_b = tikz_node(name=f"b{k+1}",options=f"below=0.75cm of b{k}.center,anchor=center",content="")
        node_c = tikz_node(name=f"c{k+1}",options=f"below=0.75cm of c{k}.center,anchor=center",content="")
        draw_b = tikz_draw(f"(b{k+1}) circle(0.5ex)", options="thick,outer sep=8mm")
        draw_c = tikz_draw(f"(c{k+1}) circle(0.5ex)", options="thick,outer sep=8mm")
        label_tmp = f"{macro('textbf', str(k+1)+'.')} {answ_text}"
        node_d = tikz_node(name=f"d{k+1}",options=f"below=0.75cm of d{k}.center,anchor=center,text width={dw}mm,align=right",
                           content=label_tmp)
    return newlines([node_a, node_b, node_c, draw_b, draw_c, node_d])

# --------------------------------------------------------------------------
def tikz_relie(indices):
    # relie toutes les sous questions à leurs réponses
    return "\n".join([ f"{macro('draw')}[very thick] (b{k+1}) -- (c{i+1});" for k,i in enumerate(indices)])
# --------------------------------------------------------------------------
def matching_to_latex(info,outfile,corrige=True,shuffle=[0,1,2,3]):
    write_question(info,outfile)
    outfile.write(macro('indent')+macro('resizebox','\linewidth')+'{!}{%'+newline())
    outfile.write(begin("tikzpicture"))
    maxwidth_sub_q, maxwidth_answ_text = (max(map(len,info['SUB_Q']))+8)*1.51323 , (max(map(len,info['ANSW_TEXT']))+8)*1.51323
    indices=[k for k in range(len(info['SUB_Q']))]
    shuff=list(zip(info['ANSW_TEXT'],indices))
    #random.shuffle(shuff)
    shuff=[shuff[i] for i in shuffle]
    shuff_answ_text,indices=zip(*shuff)
    for k,(subq,answ_text) in enumerate(zip(info['SUB_Q'],shuff_answ_text)) :
        outfile.write(tikz_matching(k,subq,answ_text,gw=maxwidth_sub_q,dw=maxwidth_answ_text))
    if corrige: outfile.write(tikz_relie(indices))
    outfile.write(end("tikzpicture"))
    outfile.write('}')
# --------------------------------------------------------------------------
def coderunner_to_latex(info,outfile,numlines=18,corrige=True):
    write_question(info,outfile)
    outfile.write(begin("tikzpicture"))
    outfile.write(macro('draw')+"[gray!40] (0,0) grid[step=0.5cm](16.5cm,"+f"{numlines*0.5}cm)"+";\n")
    outfile.write(macro('draw')+"[ultra thick,inner sep=0] (0,0) rectangle (16.5cm,"+f"{numlines*0.5}cm)"+";\n")
    numline=numlines*0.5
    range_for=','.join([f"{numlines*0.5-k*0.5}" for k in range(1,3)])+',...,0.0} {\n'
    outfile.write(macro('foreach')+' '+macro('y')+'[count='+macro('n')+'] in {'+f"{range_for}")
    outfile.write(macro('node')+"[anchor=east, font=\\ttfamily\small,align=right] at (-0.1,"+macro('y')+') {'+macro('n')+"};\n")
    outfile.write("}\n")
    match info["CR_TYPE"]:
        case "python3" :
            language='[style=colorPython]\n'
        case "bash" :
            language='[style=colorBash]\n'
    if corrige :
        code_displayed = info['CR_ANSWER']
    else:
        code_displayed = info['CR_PRELOAD']
    outfile.write(macro('node')+"[anchor=north west, font=\\ttfamily\small,inner sep=0] at (0.1,"+f"{numline}cm"+"+0.5ex) {"+\
                  begin("minipage",options=True)+'{\linewidth}\n'+\
                  begin("lstlisting",options=True)+language+\
                  code_displayed+\
                  end("lstlisting")+\
                  end("minipage")+"};\n")
    outfile.write(end("tikzpicture"))
# --------------------------------------------------------------------------
def qtex_to_latex(info,outfile,corrige,shuffle):
    match info["TYPE"]:
        case "multichoice":
            multichoice_to_latex(info,outfile,corrige=corrige,shuffle=shuffle)
        case "matching":
            matching_to_latex(info,outfile,corrige=corrige,shuffle=shuffle)
        case "coderunner":
            coderunner_to_latex(info,outfile,numlines=int(info['answerboxlines']),corrige=corrige)
        case "description":
            description_to_latex(info,outfile)
        case _:
            print("\n"f"le type {info['TYPE']} n'est pas disponible au format LaTeX""\n",file=sys.stderr)
    outfile.write(macro("clearpage")+"\n")
# --------------------------------------------------------------------------
def qtex_to_frame(info,outfile,corrige,shuffle):
    match info["TYPE"]:
        case "multichoice":
            multichoice_to_frame(info,outfile,corrige=corrige,shuffle=shuffle)
        case "matching":
            matching_to_frame(info,outfile,corrige=corrige)
        case _:
            print("\n"f"le type {info['TYPE']} n'est pas disponible au format frame (Beamer/LaTeX)""\n",file=sys.stderr)
#--------------------------------------------------------------------------------------------------
def check_shuffle(value):
    # convertir en int et vérifier la valeur
    try:
        ivalue = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{value} n'est pas un entier")
    if ivalue < 0 or ivalue > 3:
        raise argparse.ArgumentTypeError(f"{value} doit être entre 0 et 3")
    return ivalue
#--------------------------------------------------------------------------------------------------
# main parsing function
def parsing():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input', nargs='+', type=argparse.FileType('r'),
                        default=sys.stdin,help='input files (on single or a set)',required=True)
    parser.add_argument('-o','--output', nargs='?', type=argparse.FileType('a'),
                        default=sys.stdout, help='output file or stdout')
    parser.add_argument('-c','--corrige',   action='store_true', default=False, 
                         help='générer la version corrigée de la question')
    parser.add_argument('-s','--shuffle',type=check_shuffle, nargs=4,metavar=('I1','I2','I3','I4'), help='Permutation des indices (4 entiers uniques entre 0 et 3)')
    args = parser.parse_args()
    output=args.output
    if output.name !="<stdout>":
        output.seek(0,0)
        output.truncate()
    path=os.path.dirname(args.input[0].name)+'/'
    filespath=args.input
    return path,filespath,output,args.corrige,args.shuffle
#--------------------------------------------------------------------------------------------------
def html_to_tex(info):
    filters=[]
    filters+=[lambda t : re.sub(r"{", r"\{", t)]
    filters+=[lambda t : re.sub(r"}", r"\}", t)]
    filters+=[lambda t : re.sub(r"<tt>(.*?)</tt>", r"\\texttt{\1}", t)]
    filters+=[lambda t : re.sub(r"<strong>(.*?)</strong>", r"\\textbf{\1}", t)]
    filters+=[lambda t : re.sub(r"<p>(.*?)</p>", r"\1", t, flags=re.DOTALL)]
    filters+=[lambda t : re.sub(r"<pre>(.*?)</pre>", r"\\begin{verbatim}\n\1\\end{verbatim}", t, flags=re.DOTALL)]
    filters+=[lambda t : re.sub(r"<ul>(.*?)</ul>", r"\\begin{itemize}\1\\end{itemize}", t, flags=re.DOTALL)]
    filters+=[lambda t : re.sub(r"<li>(.*?)</li>", r"\\item \1", t, flags=re.DOTALL)]
    filters+=[lambda t : re.sub(r"\$", r"\\$", t)]
    filters+=[lambda t : re.sub(r"&dollar;", r"\\\$", t)]
    filters+=[lambda t : re.sub(r"<img[^>]*\bsrc=\"([^\"]+)\"[^>]*>",r"\\begin{center}\n\\includegraphics[width=0.5\\linewidth]{\1}\\end{center}\n",t,flags=re.DOTALL)]
    filters+=[lambda t : re.sub(r"@@PLUGINFILE@@",rf"{info['PATH']}assets",t,flags=re.DOTALL)]
    for key in info :
        if key in ["CR_PRELOAD","CR_ANSWER"] : continue 
        for f in filters:
            if info[key] is not None :
                if isinstance(info[key],list):
                    if all(e is not None for e in info[key]) :
                        info[key]=list(map(f,info[key]))
                else:
                    info[key]=f(info[key])
#--------------------------------------------------------------------------------------------------
def printinfodebug(file,info):
    print(f"\n{64*'-'}",file=sys.stderr)
    print(f"{file.name}",file=sys.stderr)
    print(f"\ttype : {info['TYPE']}\n\tname : {info['NAME']}\n\ttags : {info['TAGS']} ",file=sys.stderr)
    print(f"{64*'-'}",file=sys.stderr)
#--------------------------------------------------------------------------------------------------
def main_qtex_to_latex():
    path,filespath,outfile,corrige,shuffle=parsing()
    for file in filespath :
        if file.name.endswith("category.qtex"): continue
        info=readqtex(path,file)
        html_to_tex(info)
        qtex_to_latex(info,outfile,corrige,shuffle)
        printinfodebug(file,info)
#--------------------------------------------------------------------------------------------------
def main_qtex_to_frame():
    path,filespath,outfile,corrige,shuffle=parsing()
    for file in filespath :
        if file.name.endswith("category.qtex"): continue
        info=readqtex(path,file)
        html_to_tex(info)
        qtex_to_frame(info,outfile,corrige,shuffle)
        printinfodebug(file,info)

