# Entrées de qtex

## Règles :

* une clé est une ligne qui commence par # suivi de [A-Z][A-Z0-9_]* (colonne 0) ;
* si la clé est « courte » (entrees[k]['long'] is False) : valeur = reste de la ligne après un espace (éventuellement vide) ;
* si la clé est « longue » : bloc jusqu'à une ligne exactement égale à #END <KEY> ; à l'intérieur d'un bloc, aucune clé n'est interprétée ;
* l'ordre d'apparition est conservé.

## Quelques acronymes :
1. GFBACK: general Feedback
2. CFBACK: Correct Feedback
3. PFBACK: Partially Correct Feedback
4. IFBACK: Incorrect Feedback
5. ANSW_GRAD : Answer Grad
6. ANSW_TEXT : Answer Text 
7. ANSW_FBACK : Answer Feedback 
8. ANSW_IMG : Image en réponse 
9. CR_CASE_ASEXAMPLE : use as example  
10. Q_IMG : permet de ajouter un image à une question
