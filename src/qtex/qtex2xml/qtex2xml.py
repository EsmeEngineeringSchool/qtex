#!/usr/bin/python3
import sys
import os
from qtex.common.string_     import tab
from qtex.common.conversion  import png_to_base64
from qtex.common.lib_qtex    import quellecle, readqtex, default_values_before

# return une chaine vide "" ou "0" en fonction du boléen lue au format qtex 0,1,true,false 
def qtexbool(v):
    if v in "01":
        return "" if bool(int(v)) else "0"
    if v in ["true","false"]:
        return "" if v=="true" else "0"
#--------------------------------------------------------------------------------------------------
# balise xml d'ouverture (openning) 
# les arguments de *args modifie les options de la balise
# <nombalise arg[0][0]=arg[0][1] arg[1][0]=arg[1][1] ... >
# il est possible de rajouter un caracère à la balise ex. bal=?
def oxml(nombalise,*args,bal=""):
    if len(args) !=0 :
        out=f"<{bal}{nombalise}"
        for arg in args:
            out+=f" {arg[0]}=\"{arg[1]}\""
        return out+f"{bal}>"
    else:
        return f"<{nombalise}>"
#--------------------------------------------------------------------------------------------------
# balise xml de fermeture (closing)
def cxml(nombalise):
    return f"</{nombalise}>\n"

#--------------------------------------------------------------------------------------------------
# <nombalise>valeur</nombalise>
def ocxml(nombalise,*args,valeur=None):
    return oxml(nombalise,*args)+valeur+cxml(nombalise) if valeur else oxml(nombalise,*args)+cxml(nombalise)

#--------------------------------------------------------------------------------------------------
# retourne des balises xml de texte
def textxml(text=None):
    return f"<text>{text}</text>" if text else f"<text></text>"

#--------------------------------------------------------------------------------------------------
# retourne la balise CDATA 
def cdataxml(cdata=None):
    return f"<![CDATA[{cdata}]]>" if cdata else f"<![CDATA[]]>"

#--------------------------------------------------------------------------------------------------
# retourne la balise <text><![CDATA[text]]><text> 
def textcdataxml(text=None):
    return textxml(text=cdataxml(cdata=text)) 

#--------------------------------------------------------------------------------------------------
# <nombalise><text>valeur</text></nombalise>
def octextxml(nombalise,*args,text="",indent=0):
    return oxml(nombalise,*args)+\
           textxml(text)+\
           cxml(nombalise) if not indent else \
           oxml(nombalise,*args)+'\n'+\
           tab(indent+1)+textxml(text)+'\n'+\
           tab(indent)+cxml(nombalise)

#--------------------------------------------------------------------------------------------------
# <nombalise><![CDATA[valeur]]></nombalise>
def occdataxml(nombalise,*args,cdata="",indent=0):
    return oxml(nombalise,*args)+cdataxml(cdata)+cxml(nombalise) if not indent \
      else oxml(nombalise,*args)+'\n'+tab(indent+1)+cdataxml(cdata)+'\n'+tab(indent)+cxml(nombalise)

#--------------------------------------------------------------------------------------------------
# <nombalise><text><![CDATA[valeur]]></text>
def otextcdataxml(nombalise,*args,cdata="",indent=0):
    return oxml(nombalise,*args)+textcdataxml(cdata) if not indent \
      else oxml(nombalise,*args)+'\n'+tab(indent+1)+textcdataxml(cdata)+'\n'+tab(indent)
#--------------------------------------------------------------------------------------------------
# <nombalise><text><![CDATA[valeur]]></text></nombalise>
def octextcdataxml(nombalise,*args,cdata="",indent=0):
    return otextcdataxml(nombalise,*args,cdata=cdata,indent=indent)+cxml(nombalise)

#--------------------------------------------------------------------------------------------------
# <nombalise><text><![CDATA[valeur]]></text><file name="" path="/" encoding="base64">png_to_base64(path_img)</file></nombalise>
def octextcdataimagebase64xml(nombalise,*args,cdata="",path_img="",indent=0):
    if path_img != "":
        filename=os.path.basename(path_img)
        return oxml(nombalise,*args)+\
               textcdataxml(cdata)+\
               oxml("file",("name",filename),("path","/"),("encoding","base64"))+\
               png_to_base64(path_img)+cxml("file")+\
               cxml(nombalise) if not indent else \
               oxml(nombalise,*args)+'\n'+ \
               tab(indent+1)+textcdataxml(cdata)+'\n'+\
               tab(indent+1)+oxml("file",("name",filename),("path","/"),("encoding","base64"))+\
               png_to_base64(path_img)+cxml("file")+\
               tab(indent)+cxml(nombalise)
    else:
        return octextcdataxml(nombalise,args,cdata,indent)
#--------------------------------------------------------------------------------------------------
# answer in xml (multichoice,numerical)
def xml_answer(info,data,outfile,indent=0):
    fraction,text,feedback,img=data
    outfile.write(tab(indent)+oxml("answer",("fraction",fraction),("format","html"))+'\n')
    if img != "":
        filepath_img,w_img,h_img = img.split(" ")
        filepath_img = info["PATH"]+filepath_img
        filename=os.path.basename(filepath_img)
        outfile.write(tab(indent+1)+textcdataxml(oxml("img",("src","@@PLUGINFILE@@/"+filename),\
                                                       ("alt","qtex2xml"),\
                                                       ("width",w_img),\
                                                       ("height",h_img),\
                                                       ("class","img-fluid atto_image_button_text-bottom")))+'\n')
        outfile.write(oxml("file",("name",filename),("path","/"),("encoding","base64"))+png_to_base64(filepath_img))
        outfile.write(cxml("file"))
    else:
        outfile.write(tab(indent+1)+textcdataxml(text)+'\n')
    outfile.write(tab(indent+1)+octextxml("feedback",("format","html"),text=feedback,indent=indent+1))
    outfile.write(tab(indent+1)+ocxml("tolerance",valeur="0.0"))
    outfile.write(tab(indent)+cxml("answer"))

#--------------------------------------------------------------------------------------------------
# testcase of coderunner in xml
def xml_testcase(data,outfile,indent=0):
    testcode,stdin,expected,extra,mark,display,useasexample=data
    # la balise testcase
    outfile.write(tab(indent)+oxml("testcase",
                          ("testtype","0"),
                          ("useasexample",useasexample),
                          ("hiderestiffail","0"),
                          ("mark",mark))+'\n')
    outfile.write(tab(indent+1)+octextcdataxml("testcode",cdata=testcode,indent=indent+1))
    outfile.write(tab(indent+1)+octextxml("stdin",text=stdin,indent=indent+1))
    outfile.write(tab(indent+1)+octextcdataxml("expected",cdata=expected,indent=indent+1))
    outfile.write(tab(indent+1)+octextxml("extra",text=extra,indent=indent+1))
    outfile.write(tab(indent+1)+octextxml("display",text=display,indent=indent+1))
    outfile.write(tab(indent)+cxml("testcase"))

#--------------------------------------------------------------------------------------------------
# header and footer d'un test au format xml
def xml_headerquiz(outfile,indent=0):
    outfile.write(tab(indent)+oxml("xml",("version","1.0"),("encoding","UTF-8"),bal="?")+'\n')
    outfile.write(tab(indent)+oxml("quiz")+'\n')
#--------------------------------------------------------------------------------------------------
def xml_footerquiz(outfile,indent=0):
    outfile.write(tab(indent)+cxml("quiz"))
#--------------------------------------------------------------------------------------------------
# category header in xml file
def xml_category_globalinfo(info,outfile,indent):
    outfile.write(tab(indent)+octextxml("category",text=info["NAME"]))
    outfile.write(tab(indent)+octextxml("info",("format","html"),text=""))
    outfile.write(tab(indent)+ocxml("idnumber"))
#--------------------------------------------------------------------------------------------------
# write pour tous les types sauf category
def xml_globalinfo(info,outfile,indent):
    outfile.write(tab(indent)+octextxml("name",text=info["NAME"]))
    if info["Q_IMG"] == "" :
        outfile.write(tab(indent)+octextcdataxml("questiontext",("format","html"),cdata=info["Q"]+info["EXTRA_Q_LONG"],indent=indent))
    else:
        outfile.write(tab(indent)+\
        octextcdataimagebase64xml("questiontext",("format","html"),cdata=info["Q"]+info["EXTRA_Q_LONG"],path_img=info["PATH"]+info["Q_IMG"],indent=indent))

    outfile.write(tab(indent)+octextcdataxml("generalfeedback",("format","html"),cdata=info["GFBACK"]))
    outfile.write(tab(indent)+ocxml("defaultgrade",valeur="1.0000000"))
    if info["TYPE"] == "truefalse" :
        outfile.write(tab(indent)+ocxml("penalty",valeur="1"))
    else:
        outfile.write(tab(indent)+ocxml("penalty",valeur="0.3333333"))
    outfile.write(tab(indent)+ocxml("hidden",valeur="0"))
    outfile.write(tab(indent)+ocxml("idnumber"))
#--------------------------------------------------------------------------------------------------
# write pour matching
def xml_matching_globalinfo(info,outfile,indent):
    outfile.write(tab(indent)+ocxml("shuffleanswers",valeur="true"))
    outfile.write(tab(indent)+octextxml("correctfeedback",("format","html"),\
                                  text=info['CFBACK'],indent=indent))
    outfile.write(tab(indent)+octextxml("partiallycorrectfeedback",("format","html"),\
                                  text=info['PFBACK'],indent=indent))
    outfile.write(tab(indent)+octextxml("incorrectfeedback",("format","html"),\
                                  text=info['IFBACK'],indent=indent))
    outfile.write(tab(indent)+"<shownumcorrect/>"+'\n')
#--------------------------------------------------------------------------------------------------
# write pour multichoice
def xml_multichoice_globalinfo(info,outfile,indent):
    outfile.write(tab(indent)+ocxml("single",valeur="false"))
    outfile.write(tab(indent)+ocxml("shuffleanswers",valeur="true"))
    outfile.write(tab(indent)+ocxml("answernumbering",valeur="123"))
    outfile.write(tab(indent)+ocxml("showstandardinstruction",valeur="0"))
    outfile.write(tab(indent)+octextxml("correctfeedback",("format","html"),\
                                  text=info['CFBACK'],indent=indent))
    outfile.write(tab(indent)+octextxml("partiallycorrectfeedback",("format","html"),\
                                  text=info['PFBACK'],indent=indent))
    outfile.write(tab(indent)+octextxml("incorrectfeedback",("format","html"),\
                                  text=info['IFBACK'],indent=indent))
    outfile.write(tab(indent)+"<shownumcorrect/>"+'\n')
#--------------------------------------------------------------------------------------------------
# ecrire globalinfo pour numerical 
def xml_numerical_globalinfo(info,outfile,indent):
    outfile.write(tab(indent)+ocxml("unitgradingtype",valeur="0"))
    outfile.write(tab(indent)+ocxml("unitpenalty",valeur="0"))
    outfile.write(tab(indent)+ocxml("showunits",valeur="3"))
    outfile.write(tab(indent)+ocxml("unitsleft",valeur="0"))

#--------------------------------------------------------------------------------------------------
# ecrire globalinfo pour coderunner
def xml_coderunner_globalinfo(info,outfile,indent):
    outfile.write(tab(indent)+ocxml("coderunnertype",valeur=info["CR_TYPE"]))
    outfile.write(tab(indent)+ocxml("prototypetype",valeur="0"))
    outfile.write(tab(indent)+ocxml("allornothing",valeur="1"))
    outfile.write(tab(indent)+ocxml("penaltyregime",valeur=info["CR_PENALTYREGIME"]))
    outfile.write(tab(indent)+ocxml("precheck",valeur="0"))
    outfile.write(tab(indent)+ocxml("hidecheck",valeur="0"))
    outfile.write(tab(indent)+ocxml("showsource",valeur="0"))
    outfile.write(tab(indent)+ocxml("answerboxlines",valeur=info["answerboxlines"]))
    outfile.write(tab(indent)+ocxml("answerboxcolumns",valeur="100"))
    outfile.write(tab(indent)+occdataxml("answerpreload",cdata=info["CR_PRELOAD"],indent=indent))
    outfile.write(tab(indent)+ocxml("globalextra",valeur=""))
    outfile.write(tab(indent)+ocxml("useace",valeur=""))
    outfile.write(tab(indent)+ocxml("resultcolumns",valeur=""))
    outfile.write(tab(indent)+occdataxml("template",cdata=info["CR_TEMPLATE"]))
    outfile.write(tab(indent)+ocxml("iscombinatortemplate",valeur=qtexbool(info["CR_ISCOMBINATORTEMPLATE"])))
    outfile.write(tab(indent)+ocxml("allowmultiplestdins",valeur=""))
    outfile.write(tab(indent)+occdataxml("answer",cdata=info["CR_ANSWER"],indent=indent))
    outfile.write(tab(indent)+ocxml("validateonsave",valeur="1"))
    outfile.write(tab(indent)+ocxml("testsplitterre",valeur=""))
    outfile.write(tab(indent)+ocxml("language",valeur=""))
    outfile.write(tab(indent)+ocxml("acelang",valeur=info["CR_ACELANG"]))
    outfile.write(tab(indent)+ocxml("sandbox",valeur=""))
    outfile.write(tab(indent)+ocxml("grader",valeur=""))
    outfile.write(tab(indent)+ocxml("cputimelimitsecs",valeur=""))
    outfile.write(tab(indent)+ocxml("memlimitmb",valeur=""))
    outfile.write(tab(indent)+ocxml("sandboxparams",valeur=""))
    outfile.write(tab(indent)+ocxml("templateparams",valeur=""))
    outfile.write(tab(indent)+ocxml("hoisttemplateparams",valeur="1"))
    outfile.write(tab(indent)+ocxml("extractcodefromjson",valeur="1"))
    outfile.write(tab(indent)+ocxml("templateparamslang",valeur="None"))
    outfile.write(tab(indent)+ocxml("templateparamsevalpertry",valeur="0"))
    outfile.write(tab(indent)+ocxml("templateparamsevald",valeur="{}"))
    outfile.write(tab(indent)+ocxml("twigall",valeur=info["CR_TWIGALL"]))
    outfile.write(tab(indent)+ocxml("uiplugin",valeur=""))
    outfile.write(tab(indent)+ocxml("uiparameters",valeur=""))
    outfile.write(tab(indent)+ocxml("attachments",valeur="0"))
    outfile.write(tab(indent)+ocxml("attachmentsrequired",valeur="0"))
    outfile.write(tab(indent)+ocxml("maxfilesize",valeur="10240"))
    outfile.write(tab(indent)+ocxml("filenamesregex",valeur=""))
    outfile.write(tab(indent)+ocxml("filenamesexplain",valeur=""))
    outfile.write(tab(indent)+ocxml("displayfeedback",valeur="1"))
    outfile.write(tab(indent)+ocxml("giveupallowed",valeur="0"))
    outfile.write(tab(indent)+ocxml("prototypeextra",valeur=""))

#--------------------------------------------------------------------------------------------------
# ecrire testcases pour coderunner
def xml_coderunner_testcases(info,outfile,indent):
    testcases=list(zip(info["CR_CASE_CODE"],
                       info["CR_CASE_STDIN"],
                       info["CR_CASE_EXPECTED"],
                       info["CR_CASE_EXTRA"], 
                       info["CR_CASE_MARK"],
                       info["CR_CASE_DISPLAY"],
                       info["CR_CASE_ASEXAMPLE"]))
    outfile.write(tab(indent)+oxml("testcases")+'\n')
    for testcase in testcases:  
        xml_testcase(testcase,outfile,indent=indent)
    outfile.write(tab(indent)+cxml("testcases"))
#--------------------------------------------------------------------------------------------------
def xml_stack_globalinfo(info,outfile,indent):
    outfile.write(tab(indent)+octextxml("stackversion",text="2023060500",indent=indent))
    outfile.write(tab(indent)+octextxml("questionvariables",text=info["STACK_QVAR"],indent=indent))
    outfile.write(tab(indent)+octextxml("specificfeedback",("format","html"),text=info["STACK_SFBACK"],indent=indent))
    outfile.write(tab(indent)+octextxml("questionnote",("format","html"),text="",indent=indent))
    outfile.write(tab(indent)+octextxml("questiondescription",("format","html"),text="",indent=indent))
    outfile.write(tab(indent)+ocxml("questionsimplify",valeur="1"))
    outfile.write(tab(indent)+ocxml("assumepositive",valeur="0"))
    outfile.write(tab(indent)+ocxml("assumereal",valeur="0"))
    outfile.write(tab(indent)+ocxml("decimals",valeur="."))
    outfile.write(tab(indent)+ocxml("scientificnotation",valeur="*10"))
    outfile.write(tab(indent)+ocxml("multiplicationsign",valeur="cross"))
    outfile.write(tab(indent)+ocxml("sqrtsign",valeur="1"))
    outfile.write(tab(indent)+ocxml("complexno",valeur="i"))
    outfile.write(tab(indent)+ocxml("inversetrig",valeur="arccos"))
    outfile.write(tab(indent)+ocxml("logicsymbol",valeur="lang"))
    outfile.write(tab(indent)+ocxml("matrixparens",valeur="["))
    outfile.write(tab(indent)+ocxml("variantsselectionseed",valeur=""))
#--------------------------------------------------------------------------------------------------
def xml_stack_input(info,outfile,indent):
    outfile.write(tab(indent)+oxml("input")+'\n')
    outfile.write(tab(indent+1)+ocxml("name",valeur="ans1")) 
    outfile.write(tab(indent+1)+ocxml("type",valeur="algebraic")) 
    outfile.write(tab(indent+1)+ocxml("tans",valeur="sol")) 
    outfile.write(tab(indent+1)+ocxml("boxsize",valeur="15")) 
    outfile.write(tab(indent+1)+ocxml("strictsyntax",valeur="1")) 
    outfile.write(tab(indent+1)+ocxml("insertstars",valeur="0")) 
    outfile.write(tab(indent+1)+ocxml("syntaxhint",valeur="")) 
    outfile.write(tab(indent+1)+ocxml("syntaxattribute",valeur="")) 
    outfile.write(tab(indent+1)+ocxml("forbidwords",valeur="")) 
    outfile.write(tab(indent+1)+ocxml("allowwords",valeur="")) 
    outfile.write(tab(indent+1)+ocxml("forbidfloat",valeur="1")) 
    outfile.write(tab(indent+1)+ocxml("requirelowestterms",valeur="0")) 
    outfile.write(tab(indent+1)+ocxml("checkanswertype",valeur="0")) 
    outfile.write(tab(indent+1)+ocxml("mustverify",valeur="1")) 
    outfile.write(tab(indent+1)+ocxml("showvalidation",valeur="1")) 
    outfile.write(tab(indent+1)+ocxml("options",valeur="")) 
    outfile.write(tab(indent)+cxml("input"))
#--------------------------------------------------------------------------------------------------
def xml_stack_prt(info,outfile,indent):
    # prt
    outfile.write(tab(indent)+oxml("prt")+'\n')
    outfile.write(tab(indent+1)+ocxml("name",valeur="prt1")) 
    outfile.write(tab(indent+1)+ocxml("value",valeur="1.0000000")) 
    outfile.write(tab(indent+1)+ocxml("autosimplify",valeur="1")) 
    outfile.write(tab(indent+1)+ocxml("feedbackstyle",valeur="1")) 
    outfile.write(tab(indent+1)+octextxml("feedbackvariables",text="",indent=indent+1))
    #   node
    outfile.write(tab(indent+1)+oxml("node")+'\n')
    outfile.write(tab(indent+2)+ocxml("name",valeur="0"))
    outfile.write(tab(indent+2)+ocxml("description",valeur=""))
    outfile.write(tab(indent+2)+ocxml("answertest",valeur="AlgEquiv"))
    outfile.write(tab(indent+2)+ocxml("sans",valeur="ans1"))
    outfile.write(tab(indent+2)+ocxml("tans",valeur="sol"))
    outfile.write(tab(indent+2)+ocxml("testoptions",valeur=""))
    outfile.write(tab(indent+2)+ocxml("quiet",valeur="0"))
    outfile.write(tab(indent+2)+ocxml("truescoremode",valeur="="))
    outfile.write(tab(indent+2)+ocxml("truescore",valeur="1"))
    outfile.write(tab(indent+2)+ocxml("truepenalty",valeur=""))
    outfile.write(tab(indent+2)+ocxml("truenextnode",valeur="-1"))
    outfile.write(tab(indent+2)+ocxml("trueanswernote",valeur="prt1-1-T"))
    outfile.write(tab(indent+2)+octextxml("truefeedback",("format","html"),text="",indent=indent+2))
    outfile.write(tab(indent+2)+ocxml("falsescoremode",valeur="="))
    outfile.write(tab(indent+2)+ocxml("falsescore",valeur="0"))
    outfile.write(tab(indent+2)+ocxml("falsepenalty",valeur=""))
    outfile.write(tab(indent+2)+ocxml("falsenextnode",valeur="-1"))
    outfile.write(tab(indent+2)+ocxml("falseanswernote",valeur="prt1-1-T"))
    outfile.write(tab(indent+2)+octextxml("falsefeedback",("format","html"),text="",indent=indent+2))
    outfile.write(tab(indent+1)+cxml("node"))
    outfile.write(tab(indent)+cxml("prt"))
#--------------------------------------------------------------------------------------------------
def xml_stack_qtest(info,outfile,indent):
    outfile.write(tab(indent)+oxml("qtest")+'\n')
    outfile.write(tab(indent+1)+ocxml("testcase",valeur="1"))
    outfile.write(tab(indent+1)+ocxml("description",valeur="Test case assuming the teacher's input gets full marks."))
    outfile.write(tab(indent+1)+oxml("testinput")+'\n')
    outfile.write(tab(indent+2)+ocxml("name",valeur="ans1"))
    outfile.write(tab(indent+2)+ocxml("value",valeur="sol"))
    outfile.write(tab(indent+1)+cxml("testinput"))
    outfile.write(tab(indent+1)+oxml("expected")+'\n')
    outfile.write(tab(indent+2)+ocxml("name",valeur="prt1"))
    outfile.write(tab(indent+2)+ocxml("expectedscore",valeur="1.000000"))
    outfile.write(tab(indent+2)+ocxml("expectedpenalty",valeur="1.000000"))
    outfile.write(tab(indent+2)+ocxml("expectedanswernote",valeur="prt1-1-T"))
    outfile.write(tab(indent+1)+cxml("expected"))
    outfile.write(tab(indent)+cxml("qtest"))
#--------------------------------------------------------------------------------------------------
def xml_wirisquestion(info,outfile,indent):
    pass

def xml_subquestion(info,data,outfile,indent):
    fraction,text,feedback,img,sub_q=data
    outfile.write(tab(indent+1)+otextcdataxml("subquestion",("format","html"),cdata=sub_q,indent=indent+1))
    outfile.write(tab(indent)+oxml("answer")+'\n')
    outfile.write(tab(indent+3)+textcdataxml(text)+'\n')
    outfile.write(tab(indent+2)+cxml("answer"))
    outfile.write(tab(indent+1)+cxml("subquestion"))


#--------------------------------------------------------------------------------------------------
# question au format xml toutes les variables sont lues par readqtex()
# info est dictionnaire avec toutes les entrées utiles
def xml_question(info,outfile,indent=0):

    questiontype=info["TYPE"]
    # EN-TETE d'une question
    outfile.write(tab(indent)+"<!-- question: gentestmoodle.py  -->"+'\n')
    outfile.write(tab(indent)+oxml("question",("type",info["TYPE"]))+'\n')

    # TOUS LES TYPES DE QUESTION sauf category (pas de contre exemple pour l'instant)
    if info["TYPE"] != "category" :
        xml_globalinfo(info,outfile,indent+1)
    else :
        xml_category_globalinfo(info,outfile,indent+1)
    #MULTICHOICE | TRUEFALSE | NUMERICAL | SHORTANSWERWIRIS | MATCHING | SHORTANSWER
    if info["TYPE"] in [ "multichoice", "truefalse", "numerical" , "multichoicewiris", "shortanswerwiris", "matching" , "shortanswer" ] :

        if info["TYPE"] in ["multichoice","multichoicewiris","shortanswer"] : xml_multichoice_globalinfo(info,outfile,indent+1)
        if info["TYPE"] == "matching" : xml_matching_globalinfo(info,outfile,indent+1)
        if info["TYPE"] == "numerical" : xml_numerical_globalinfo(info,outfile,indent+1)
        if info["TYPE"] == "shortanswerwiris" : outfile.write(tab(indent+1)+ocxml("usecase",valeur="1"))
        # "sections" answer (il n'y a pas de sections balise xml answers ou les answer sont regroupés)
        # answer : grad, text, fback, img 
        answ_ =[info["ANSW_GRAD" ],\
                info["ANSW_TEXT" ],\
                info["ANSW_FBACK"],\
                info["ANSW_IMG"]]
        if info["TYPE"] == "matching" : 
            answ_.append(info["SUB_Q"])

        for ans in list(zip(*answ_)) :
            if info["TYPE"] == "matching" : 
                xml_subquestion(info,ans,outfile,indent=indent)
            else:
                xml_answer(info,ans,outfile,indent=indent+1)
        if info["TYPE"] == "multichoicewiris" :
            xml_wirisquestion(info,outfile,indent+1)
    #CODERUNNER
    if info["TYPE"] == "coderunner" :
        xml_coderunner_globalinfo(info,outfile,indent+1)
        # section testcases avec plusieurs testcase: testcode,stdin,expected,extra,mark,display,useasexample
        xml_coderunner_testcases(info,outfile,indent+1)
    #STACK
    if info["TYPE"] == "stack" :
        xml_stack_globalinfo(info,outfile,indent+1)
        xml_stack_input(info,outfile,indent+1)
        xml_stack_prt(info,outfile,indent+1)
        xml_stack_qtest(info,outfile,indent+1)

    # END OF QUESTION (we finish with tags if not category or description)
    if info["TYPE"] not in ["category","description"] : 
        outfile.write((indent+1)*'\t'+oxml("tags")+'\n')
        for tag in info["TAGS"].split():
            outfile.write((indent+2)*'\t'+ocxml("tag",valeur=textxml(tag)))
        outfile.write((indent+1)*'\t'+cxml("tags"))
    
    #END OF QUESTION
    outfile.write(indent*'\t'+cxml("question"))

#--------------------------------------------------------------------------------------------------
# main parsing function
def parsing():
    import os 
    import argparse
    parser = argparse.ArgumentParser(
            description="qtex2xml permet de transformer une qtex au format xml de Moodle")
    parser.add_argument('-i','--input', nargs='+', type=argparse.FileType('r'),
                        default=sys.stdin,help='input files (on single or a set)',required=True)
    parser.add_argument('-o','--output', nargs='?', type=argparse.FileType('a'),
                        default=sys.stdout, help='output file or stdout')
    args = parser.parse_args()

    output=args.output
    if output.name !="<stdout>":
        output.seek(0,0)
        output.truncate()

    dirname=os.path.dirname(args.input[0].name)
    path = './' if not dirname else dirname+'/'
    filespath=args.input
    return path,filespath,output

#--------------------------------------------------------------------------------------------------
def main() :
    path,filespath,outfile=parsing()
    xml_headerquiz(outfile=outfile)
    with open(path+"category.qtex","r") as file:
        info=readqtex(path,file)
    xml_question(info,outfile,1)
    for file in filespath :
        if file.name.endswith("category.qtex"): continue 
        print(file.name,file=sys.stderr,end=' ')
        info=readqtex(path,file)
        for printinfo in ['TYPE','NAME','TAGS']:
            if printinfo in info :
                print(f"\n\ttype : {info[printinfo]}",file=sys.stderr,end="")
        xml_question(info,outfile,1)

    xml_footerquiz(outfile=outfile)

