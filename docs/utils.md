# Quelques scripts secondaires utiles 

## `transqtex`

Permet de traduire une question qtex du français à l'anglais en utilisant l'API Google Cloud

Exemple :

    bin/transqtex -i examples/bashcoderunner.qtex qtex_en/bashcoderunner_en.qtex

si l'option -o n'est pas donnée écrit dans la sortie standard

## `transqtexAll` :

Applique `transqtex` à tous les fichiers d'un répertoire passé en argument

Exemple :

    bin/transqtexAll qtex qtex_en
