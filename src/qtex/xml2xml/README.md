# xml2xml

`xml2xml` est un outil en ligne de commande en Python permettant de **traduire automatiquement des fichiers XML Moodle** (banques de questions, quiz, etc.)  
en ciblant des balises spécifiques selon le type de question.

Il s'appuie sur le module [`lxml`](https://lxml.de/) pour la manipulation des fichiers XML et offre deux moteurs de traduction :

- **[LibreTranslate](https://libretranslate.com/)** (par défaut, via un serveur local ou distant)
- **[Google Cloud Translate](https://cloud.google.com/translate/docs)** (optionnel, via le SDK officiel)

Ce dépôt inclut également un utilitaire complémentaire [`merge_xml`](#merge_xml) permettant de **fusionner plusieurs fichiers XML** traduits ou non.

---
> ATTENTION: L'utilisation de l'API Google Cloud nécessite une configuration valide du SDK (clé d'API et variable d'environnement `GOOGLE_APPLICATION_CREDENTIALS`).  
> **LibreTranslate** doit être lancé et attendu sur `http://localhost:5000/translate`.
> Si aucun moteur n'est spécifié, `xml2xml` utilisera **Google Cloud Translate** par défaut.

---

## Utilisation

### help :
```bash
xml2xml.py -h
usage: xml2xml.py [-h] -i INPUT [INPUT ...] [-o [OUTPATH]] [-g] [-l] [-t [TARGET]]

options:
  -h, --help                                       show this help message and exit
  -i INPUT [INPUT ...], --input INPUT [INPUT ...]  input files (on single or a set)
  -o [OUTPATH], --outpath [OUTPATH]                output path
  -g, --google_cloud                               utiliser l'api translate de google-cloud
  -l, --libretranslate                             utiliser l'api de libretranslate
  -t [TARGET], --target [TARGET]                   langue cible de la traduction
```

### Traduire un ou plusieurs fichiers XML

```bash
xml2xml.py -i examples/*.xml
```

Par défaut :
- la **langue cible** est `en` (anglais),
- le **moteur de traduction** est `libretranslate`,
- les fichiers traduits sont enregistrés dans le répertoire courant.

Exemple de sortie :

```
examples/coderunner.xml    -> ./coderunner_en.xml
examples/matching.xml      -> ./matching_en.xml
examples/multichoice.xml   -> ./multichoice_en.xml
examples/numerical.xml     -> ./numerical_en.xml
examples/shortanswer.xml   -> ./shortanswer_en.xml
```

---

### Définir la langue cible

```bash
xml2xml.py -i examples/*.xml -t pt
```

Traduit les fichiers XML vers le **portugais**.

---

### Spécifier le moteur de traduction

#### Utiliser LibreTranslate 

```bash
xml2xml.py -i examples/*.xml -l
```
ou
```bash
xml2xml.py -i examples/*.xml --libretranslate
```

LibreTranslate doit être accessible localement sur :

```
http://localhost:5000/translate
```

#### Utiliser Google Cloud Translate (par défaut)

```bash
xml2xml.py -i examples/*.xml -g
```
ou
```bash
xml2xml.py -i examples/*.xml --google_cloud
```


Cette option nécessite que l'environnement Google Cloud soit configuré correctement.

---
### Définir un répertoire de sortie

```bash
xml2xml.py -i examples/*.xml -o translations/
```

Tous les fichiers traduits seront créés dans le dossier `translations/`.

---

### Fichier de configuration

Vous pouvez enrichir la liste des **balises à traduire** ou à ne traduire qu'une seule fois
en fournissant un fichier via `--config` ou `-c`:

```bash
xml2xml.py -i examples/*.xml -c tags.conf
```

Le fichier comporte des sections et pour chaque ligne définit après la section
doit contenir un **XPath** vers un tag, par exemple :

```
# [ translate ]
//answer/text
# [ translate_once ]
//correctfeedback/text
//partiallycorrectfeedback/text
//incorrectfeedback/text
```

---

## Tags traduisibles par défaut

Le script traduit uniquement certains tags selon le type de question Moodle.  
Ces règles sont définies dans le dictionnaire `tags_a_traduire_par_type` du fichier `xml2xml.py` :

```python
tags_a_traduire_par_type = {
    "coderunner"       : question_tags + general_feedback,
    "matching"         : question_tags + general_feedback + partial_feedbacks,
    "multichoice"      : question_tags + general_feedback + partial_feedbacks,
    "shortanswer"      : question_tags + general_feedback + partial_feedbacks,
    "shortanswerwiris" : question_tags + general_feedback,
    "numerical"        : question_tags + general_feedback,
    "category"         : category_tags
}
```

> Les balises `<name>` et `<questiontext>` sont toujours traduites.  
> Le contenu `<questiontext>` est automatiquement réécrit en CDATA si nécessaire.  
> Les réponses ne sont pas traduites (par défaut).

---

## merge_xml

Le dépôt contient également un second script : **`merge_xml.py`**.  
Il permet de **fusionner plusieurs fichiers XML Moodle** (traduit ou non) en un seul fichier global prêt à être importé dans Moodle.

### Exemple d'utilisation

```bash
merge_xml.py <repertoire>
```

Le script parcourt récursivement le répertoire indiqué, fusionne tous les fichiers XML qu'il contient et crée un fichier `<repertoire>.xml` à la racine.  
Chaque fichier est intégré à l'intérieur d'une balise `<quiz>...</quiz>` complète.

---

## Améliorations possibles

- Support d'autres moteurs de traduction (DeepL, OpenAI, etc.)  
- Détection automatique de la langue source  
- Meilleure gestion des CDATA et des balises complexes  
