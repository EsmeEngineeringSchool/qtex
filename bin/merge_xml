#!/usr/bin/env python3
import os
import sys

# header d'un quiz
def header_quiz():
    out=["<?xml version=\"1.0\" encoding=\"UTF-8\"?>"]
    out+=["<quiz>"]
    out+=[""]
    return "\n".join(out)

# fusion des fichiers xml donnés par une liste
def merge_xml_files(path,files):
    out=header_quiz()
    for file in files:
        with open(f"{path}/{file}","r") as f:
            lines=f.readlines()
        out+="".join(lines[2:-1])
    out+="<quiz>"
    return out

# retourne la liste des sous-repertoires
def lsdir(root):
    return [ content for content in os.listdir(root) if os.path.isdir(os.path.join(root, content))] 
# retourne la liste des fichiers xml à la racine
def lsxml(root):
    return [ content for content in os.listdir(root) if test_extension(content)] 
# on teste l'extension d'un fichier 
def test_extension(filename,extension=".xml"):
    return os.path.splitext(filename)[1] == extension

# parcours en profondeur !
def merge_xml_in_directory(root):
    #if len(lsdir(root)) == 0 :
    #    return 
    for subdir in lsdir(root):
        merge_xml_in_directory(f"{root}/{subdir}")
    basename = root.split("/")[-1]
    parent = os.path.dirname(root) 
    parent = f"{parent}/" if  parent != "" else parent
    filename=f"{parent}{basename}.xml"
    print(filename)
    with open(filename,"w") as f :
        f.write(merge_xml_files(root,lsxml(root)))

if __name__ == "__main__":
    assert len(sys.argv) > 1, f"Usage: {sys.argv[0]} <dir>"
    root = sys.argv[1].replace("/","")
    merge_xml_in_directory(root)
