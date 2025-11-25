#!/usr/bin/env python3
import os
import sys
import html
import requests
import argparse
from lxml import etree
#--------------------------------------------------------------------------------------------------
#  Les tags à traduire
#--------------------------------------------------------------------------------------------------
# les tags liées à toutes les questions
question_tags=["//name/text","//questiontext/text"]
# les tags de catégorie à traduire
category_tags=["//category/text"]
# d'autres tags à traduire
general_feedback = ["//generalfeedback/text"]
# les tags de feedbacks partiels 
partial_feedbacks=["//correctfeedback/text",
                   "//partiallycorrectfeedback/text",
                   "//incorrectfeedback/text"]
# les tags qui ont des CDATA
with_cdata=["//questiontext/text","//answer/text"]

# dictionnaire qui regroupe les tags par type
tags_a_traduire_par_type={"coderunner"  : question_tags + general_feedback,
                          "matching"    : question_tags + general_feedback + partial_feedbacks,
                          "multichoice" : question_tags + general_feedback + partial_feedbacks,
                          "shortanswer" : question_tags + general_feedback + partial_feedbacks,
                          "shortanswerwiris" : question_tags + general_feedback,
                          "numerical"   : question_tags + general_feedback,
                          "category"    : category_tags }
#--------------------------------------------------------------------------------------------------
# choisir parmi les 'engines' disponible pour la traduction
def translate_text(target,text,engine):
    match engine :
        case "google_cloud" :
            return translate_text_google_cloud(target,text)
        case "libretranslate" : 
            return translate_text_libretranslate(target,text)
#--------------------------------------------------------------------------------------------------
# requete en local avec translate
def translate_text_libretranslate(target,text,url="http://localhost:5000/translate"):
    data = {
    "q": text,
    "source": "fr",
    "format": "text",
    "target": target}
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()["translatedText"]
#--------------------------------------------------------------------------------------------------
def translate_text_google_cloud(target: str, text: str) -> dict:
    """Translates text into the target language.
    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    from google.cloud import translate_v2 as translate
    translate_client = translate.Client()
    if isinstance(text, bytes):
        text = text.decode("utf-8")
    result = translate_client.translate(text, target_language=target,format_ ="html")
    return html.unescape(result["translatedText"])
#--------------------------------------------------------------------------------------------------
def translate_xml(file,target,outpath,engine,tags_config):
    tags_a_traduire={}
    string_translated_once={}
    for qtype in tags_a_traduire_par_type.keys() :
        tags_a_traduire[qtype]=tags_a_traduire_par_type[qtype]
        if "translate" in tags_config :
            tags_a_traduire[qtype]+=tags_config["translate"]
        for tag in tags_a_traduire[qtype] :
            string_translated_once[tag]=None

    fileout=outpath+os.path.basename(file.name).replace(".xml","_en.xml")
    print(f"{file.name} -> {fileout}",file=sys.stderr)
    tree = etree.parse(file, parser)
    root = tree.getroot()
    # parcourir toutes les questions
    k=0
    for question in root.findall(".//question"):
        k+=1
        qtype = question.get("type")
        # tag par type 
        for tag in tags_a_traduire[qtype] : 
            for t in question.xpath(tag.lstrip('/')):
                if tag not in tags_config["translate_once"] or string_translated_once[tag] is None :
                    if t.text:
                        translated=translate_text(target,t.text,engine)
                        t.text = etree.CDATA(translated) if tag in with_cdata else translated
                        string_translated_once[tag]=translated
                        print(f"q.{k} {qtype} {tag.lstrip('/')} translated -> {translated[:50]}",end='')
                        if len(translated) > 50 : print("...",end="")
                        print()
                else:
                    if t.text:
                        t.text = string_translated_once[tag]
                        print(f"q.{k} {qtype} {tag.lstrip('/')} already translated -> {string_translated_once[tag][:50]}",end='')
                        if len(string_translated_once[tag]) > 50 : print("...",end='')
                        print()

    tree.write(fileout, encoding="UTF-8", xml_declaration=True, pretty_print=False)
#--------------------------------------------------------------------------------------------------
# lecture du fichier de configuration 
# # [translate]
#   //tag1
#   //tag2
#
# # [translate_once]
#   //tagA
#   //tagB
def load_tag_config(configfile):
    config = {"translate": [], "translate_once": []}
    current_section = None
    if configfile is None : return config 
    # lecture ligne par ligne
    for line in configfile:
        line = line.strip()

        # si une ligne de commentaire et pas une ligne de section
        if not line or line.startswith("#") and not line.startswith("# ["): continue

        # si une ligne de section on définit current_section 
        if line.startswith("# [") and line.endswith("]"):
            current_section = line[3:-1].strip()
            continue
        # si pas dans une section -> erreur
        if current_section is None:
            raise ValueError(f"Ligne hors section détectée : {line}")
        else:
            config[current_section].append(line)

    return config
#--------------------------------------------------------------------------------------------------
def dir_path(path):
    return path if os.path.isdir(path) else argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")
#--------------------------------------------------------------------------------------------------
def parsing_command_line():
    import os
    ENGINES=["google_cloud","libretranslate"]
    formatter = lambda prog: argparse.HelpFormatter(prog,max_help_position=52)
    parser = argparse.ArgumentParser(formatter_class=formatter)
    parser.add_argument('-t','--target', nargs="?", default="en", help='langue cible de la traduction : en, pt, es')
    parser.add_argument('-i','--input', nargs='+', type=argparse.FileType('r'),
                        default=sys.stdin,help='input files (on single or a set)',required=True)
    parser.add_argument('-o','--outpath', nargs='?', type=dir_path, default='./', help='output path')
    parser.add_argument('-c','--config', nargs='?', type=argparse.FileType('r'), help='configuration file')
    parser.add_argument('-g','--google_cloud',   action='store_true', default=True, 
                         help='utiliser l\'api translate de google-cloud')
    parser.add_argument('-l','--libretranslate', action='store_true', default=False,
                         help='utiliser l\'api de libretranslate')
    args = parser.parse_args()
    engine = next((name for name in ENGINES if getattr(args, name)), None)
    setattr(args, "engine", engine)
    #print(args)
    return args
#--------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    args = parsing_command_line()
    f=args.config
    tags_from_config_file=load_tag_config(f)
    parser = etree.XMLParser(strip_cdata=False, remove_comments=False)
    for file in args.input :
        translate_xml(file,target=args.target,outpath=args.outpath,engine=args.engine,tags_config=tags_from_config_file)
