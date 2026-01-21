import sys
from .format_qtex import types_with_requirements,same_number,infos
from .string_ import get, grep, mult
#--------------------------------------------------------------------------------------------------
# retourne la clé présente dans le fichier qtex si il y a plusieurs possibilités.
# La fonction retourne un tuple: le premier élément est la clé (dictionnaire) d'accès info 
# et la forme de la clé qui réellement présente dans le fichier.
# Le tuple peut donc présenter deux fois la même valeur
# Note : c'est pour traiter les cas de #Q et #Q_LONG #END Q_LONG. Ce qui est lu est rangé dans 
# info["Q"] même si Q_LONG est la clé présente dans le fichier qtex. 
def quellecle(cle,data):
    which_index = [k for k,c in enumerate(cle) if grep(c,data)]
    if not isinstance(cle,tuple) :
        return (cle,cle)
    else :
        return tuple([cle[0]]+[cle[c] for c in which_index])

#--------------------------------------------------------------------------------------------------
# pour définir quelques valeurs par défaut (test si des clés exigées sont absentes, 
# le prétexte étant de pouvoir compter le nombre d'éléments)
# et retourne le dictionnaire info qui regroupe tous les paramètres lues dans le fichier qtex
def default_values_before(data):
    info={}
    qtype=get("TYPE",data)
    info["Q_IMG"]=""
    info["EXTRA_Q_LONG"]=""

    if qtype in types_with_requirements:  
        assert any([grep(cle,data) for cle in same_number[qtype]]),\
               f"some of the keys are missing for {qtype} : {same_number[qtype]} {[grep(cle,data) for cle in same_number[qtype]]}"

        m=mult(same_number[qtype][[grep(cle,data) for cle in same_number[qtype]].index(True)],data)
    else:
        m=1

    match qtype :
        case "multichoice" | "numerical" | "multichoicewiris" | "shortanswerwiris" | "matching" | "shortanswer" :
            if not grep('ANSW_FBACK',data) : info['ANSW_FBACK']=[None]*m
            if not grep('ANSW_TEXT',data)  : info['ANSW_TEXT']=[""]*m
            if not grep('ANSW_GRAD',data)  : info['ANSW_GRAD']=["0"]*m
            if not grep('ANSW_IMG',data)   : info['ANSW_IMG']=[""]*m
        case "matching" :
            if not grep('SUB_Q',data)      : info['SUB_Q']=[""]*m
        case "coderunner" :
            if not grep("CR_TYPE",data)                  : info["CR_TYPE"]="python3"
            if not grep("CR_TEMPLATE",data)              : info["CR_TEMPLATE"]=""
            if not grep("CR_ACELANG",data)               : info["CR_ACELANG"]=""
            if not grep("CR_TWIGALL",data)               : info["CR_TWIGALL"]="0"
            if not grep("CR_ISCOMBINATORTEMPLATE",data)  : info["CR_ISCOMBINATORTEMPLATE"]="1"
            if not grep("CR_PENALTYREGIME",data)         : info["CR_PENALTYREGIME"]="0,5,10,..."
            if not grep("CR_CASE_ASEXAMPLE",data)        : info["CR_CASE_ASEXAMPLE"] =["0"]*m
            if not grep("CR_CASE_MARK",data)             : info["CR_CASE_MARK"] = ["1.0"]*m
            if not grep("CR_CASE_EXPECTED",data) and \
               not grep("CR_CASE_EXPECTED_LONG",data)    : info["CR_CASE_EXPECTED"] = [""]*m
            if not grep("CR_CASE_DISPLAY",data)          : info["CR_CASE_DISPLAY"] = ["SHOW"]*m
            if not grep("CR_CASE_STDIN",data)            : info["CR_CASE_STDIN"] = [""]*m
            if not grep("CR_CASE_EXTRA",data)            : info["CR_CASE_EXTRA"] = [""]*m
            info["answerboxlines"]=str(int((get("CR_ANSWER",data).count("\n")+1)*1.2))
    return info

def check_values_after(info):
    ALLOWED_CR_CASE_DISPLAY=["SHOW", "HIDE", "HIDE_IF_SUCCEED","HIDE_IF_FAIL"]
    match info["TYPE"] :
        case "coderunner" :
            for v in info["CR_CASE_DISPLAY"]:
                assert v in ALLOWED_CR_CASE_DISPLAY, f"{v} is not in CR_CASE_DISPLAY\nCheck your input"
        case _ :
            return

#--------------------------------------------------------------------------------------------------
# Lecture des fichiers au format maison qtex
# retourne un dictionnaire des infos lues dans le fichier qtex
def readqtex(path,file):
    data=file.read()
    # ------------------------------------------
    # default value
    # ------------------------------------------
    info=default_values_before(data) 
    info["PATH"]=path
    # lectures des entrées globales
    for c in infos["global"] :
        cle=quellecle(c,data)
        if not grep(cle[1],data) : continue
        info[cle[0]]=get(cle[1],data) 
    if info["TYPE"] == "category" : return info
    # lectures des entrées globales pour les questions de type différente de category
    for c in infos["question"]:
        #if info["TYPE"] == "description" and c == "TAGS" : continue
        cle=quellecle(c,data)
        if not grep(cle[1],data) : continue
        info[cle[0]]=get(cle[1],data) 
    if info["TYPE"] == "description" : return info
    # les entrées en fonctions du type info["TYPE"]
    for c in infos[info["TYPE"]] :
        cle=quellecle(c,data)
        for cc in cle[1:]:
            if not grep(cc,data) : break 
            if cle[0] in info.keys() :
                info[cle[0]].extend(get(cc,data))
            else:
                info[cle[0]]=get(cc,data)
    check_values_after(info)
    return info

if __name__=="__main__":
    info=readqtex("./",sys.stdin)
    print(info)
