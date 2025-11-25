import re
from .format_qtex import entrees 

#--------------------------------------------------------------------------------------------------
def tab(k):
    return k*'\t'
#--------------------------------------------------------------------------------------------------
def rmnewline(s='',end=True):
    if end :
        return ( s[:-1] if s[-1]=='\n' else s ) if len(s) != 0 else s
    else :
        return ( s[1:] if s[0]=='\n' else s ) if len(s) != 0 else s

def rmnewlineboth(s):
    return rmnewline(rmnewline(s),end=False)

def rmnewlines(x):
    return [rmnewline(s).rstrip() for s in x]

def rmnewlinesboth(x):
    return [rmnewlineboth(s).rstrip() for s in x]

#--------------------------------------------------------------------------------------------------
#Récupérer la chaine de caractère associé à une clé
#la fonction retourne une chaine par défaut sinon une liste de chaines des "match"
def get(pattern,data):
    if entrees[pattern]["long"] :
        # Récupérer la chaine de caractères entre les champ #{pattern} et  #END {pattern}
        regex=f"(?<=\#{pattern}\s|\#{pattern}\n).*?(?=\#END {pattern}.*)"
        if entrees[pattern]["multiple"] :
            return rmnewlinesboth(re.findall(regex,data,re.DOTALL))
        else:  
            return rmnewlineboth(re.findall(regex,data,re.DOTALL)[0]).rstrip() 
    else:
        #Récupérer la chaine de caractères après le champ #{pattern}
        regex=f"(?<=\#{pattern}\s).*"
        if entrees[pattern]["multiple"]  :
            return rmnewlines(re.findall(regex,data))
        else:
            return rmnewline(re.findall(regex,data)[0]).rstrip()

#--------------------------------------------------------------------------------------------------
#retourne combien d'occurences sont trouvés
def mult(pattern,data):
    return len(re.findall(r"\#"+pattern+r'\s', data))

#--------------------------------------------------------------------------------------------------
#un grep simplifié retourne True si la recherche de "\#pattern\s" dans data est un succès
def grep(pattern,data):
    return re.search(r"\#"+pattern+r'\s', data) != None

