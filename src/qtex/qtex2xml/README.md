# qtex2xml
qtex2xml permet de produire des fichiers xml de questions de différents types (Coderunner, multichoice, Numerical, Stack, Wiris) de Moodle

## Exemple : 

    bin/qtex2xml -i examples/*.qtex -o all_examples.xml

si l'option -o n'est pas donnée écrit dans la sortie standard (DEBUG seulement)


## À propos du format de question `qtex`

Pour l'instant quelques types de questions Moodle sont pris en charge par les scripts 
`qtex2xml` et `transqtex` :

0. category
1. multichoice
2. numerical
3. coderunner (en phase de test)
3. stack      (en phase de test)

Voici les templates de ces types de question : 
### "category"
```
TYPE category
NAME [Nom de la catégorie]
```
### "multichoice"
```
#TYPE multichoice
#NAME [Nom de la question]
#GFBACK Merci d'avoir pris le temps de répondre à cette question.
#CFBACK Bravo! Votre réponse est correcte.
#PFBACK Votre réponse est partiellement correcte.
#IFBACK Votre réponse est incorrecte.
#Q [Texte de la question]
#ANSW_GRAD [Note de la réponse 1]
#ANSW_GRAD [Note de la réponse 2]
...
#ANSW_GRAD [Note de la réponse n]
#ANSW_TEXT [Texte de la réponse 1]
#ANSW_TEXT [Texte de la réponse 2]
#ANSW_TEXT [Texte de la réponse 3]
...
#ANSW_TEXT [Texte de la réponse n]
#TAGS [TAGS associés à la question]
```
### "numerical"
```
#TYPE numerical
#NAME [Nom de la question]
#GFBACK Merci d'avoir pris le temps de répondre à cette question.
#Q [Texte de la question]
#ANSW_GRAD [Note de la réponse]
#ANSW_TEXT [Texte de la réponse]
#TAGS [TAGS associés à la question]
```
### "coderunner"
```
#TYPE coderunner
#NAME [Nom de la question]
#Q Donner une fonction f qui prend un paramètre et retourne son carré
#GFBACK Merci d'avoir pris le temps de répondre à cette question.
#CR_PRELOAD
def f(x):
    return ...
#END CR_PRELOAD
#CR_ANSWER
def f(x):
    return x**2
#END CR_ANSWER
#CR_CASE_CODE
print(f(3))
#END CR_CASE_CODE
#CR_CASE_CODE
print(f(4))
#END CR_CASE_CODE
#CR_CASE_CODE
print(f(5))
#END CR_CASE_CODE
#CR_CASE_EXPECTED 9
#CR_CASE_EXPECTED 16
#CR_CASE_EXPECTED 25
#CR_CASE_MARK 1.0
#CR_CASE_MARK 1.0
#CR_CASE_MARK 1.0
#TAGS [TAGS associés à la question] 
```
### "stack"
```
#TYPE stack
#NAME [Nom de la question]
#GFBACK Merci d'avoir pris le temps de répondre à cette question.
#Q_LONG
#END Q_LONG
#STACK_QVAR 
#STACK_SFBACK 
#TAGS
```
## Outils
[Quelques scripts utiles pour le traitement des fichiers qtex](doc/utils.md)
## Description des toutes les entrées
[Description des entrées](doc/entrees.md)
## un peu de couleur
[La coloration syntaxique avec vim](doc/vim.md)
