# QTeX

Monodépôt[^1] contenant les trois sous-modules QTeX :

- `qtex2xml` : conversion QTeX → XML
- `qtex2latex` : conversion QTeX → LaTeX
- `xml2xml` : transformations XML → XML (traduction)

D'autres scripts utiles:

- `qtex2pdf` : utilise `qtex2latex` pour générer un aperçu de la question au format pdf.
- `merge_xml` : qui permet de **fusionner plusieurs fichiers XML Moodle** (traduit ou non) en un seul 
                fichier global prêt à être importé dans Moodle.
- `qtex2examen` : utilise `qtex2latex` pour générer un examen LaTeX en utilisant le template examen 
                  du dépôt [templatesLaTex](https://github.com/EsmeEngineeringSchool/templatesLaTeX)

## TODO
Les scripts de filtre du type `html2tex` et `tex2html` pourrait aller dans `qtex/common/`

[^1]: Ce dépôt est le résultat de la fusion de trois précédents dépôts maintenant disparus de https://github.com/EsmeEngineeringSchool/ 
