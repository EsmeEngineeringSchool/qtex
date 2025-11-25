# QTeX

Monodépôt[^1] contenant les trois sous-modules QTeX :

- `qtex2xml` : conversion QTeX → XML
- `qtex2latex` : conversion QTeX → LaTeX
- `xml2xml` : transformations XML → XML (traduction)

D'autres scripts utiles:

- `qtex2pdf` : utilise `qtex2latex` pour générer un aperçu de la question au format pdf.
- `merge_xml` : qui permet de **fusionner plusieurs fichiers XML Moodle** (traduit ou non) en un seul 
                fichier global prêt à être importé dans Moodle.

### Exemple d'utilisation

```bash
merge_xml.py <repertoire>
```

Le script parcourt récursivement le répertoire indiqué, fusionne tous les fichiers XML qu'il contient et crée un fichier `<repertoire>.xml` à la racine.
Chaque fichier est intégré à l'intérieur d'une balise `<quiz>...</quiz>` complète.


[^1] Ce dépôt est le résultat de la fusion de trois précédents dépôts maintenant disparus de https://github.com/EsmeEngineeringSchool/ 
