# qtex2latex

Convertisseur de fichiers QTEX vers LaTeX pour la génération de documents d'évaluation.

## Description

`qtex2latex.py` est un outil en ligne de commande qui convertit des fichiers au format QTEX en code LaTeX. Il permet de générer automatiquement des questions formatées en LaTeX à partir de fichiers sources structurés.

## Installation

Le script nécessite Python 3.10+ et la bibliothèque `qtex` :

## Utilisation

### Syntaxe de base

```bash
./qtex2latex.py -i fichier.qtex -o sortie.tex
```

### Options

- `-i, --input` : Fichier(s) d'entrée QTEX (obligatoire)
- `-o, --output` : Fichier de sortie LaTeX (par défaut : sortie standard)

### Exemples

Convertir un seul fichier :
```bash
./qtex2latex.py -i questions.qtex -o document.tex
```

Convertir plusieurs fichiers :
```bash
./qtex2latex.py -i q1.qtex q2.qtex q3.qtex -o examen.tex
```

Afficher le résultat dans le terminal :
```bash
./qtex2latex.py -i questions.qtex
```

## Types de questions supportés

### Questions à choix multiples (multichoice)

Génère des questions avec des réponses formatées et colorées :
- Réponses correctes marquées en vert avec ✓
- Réponses incorrectes marquées en rouge avec ✗
- Mélange automatique des réponses

### Questions d'appariement (matching)

Crée des diagrammes TikZ interactifs pour relier des éléments :
- Génération automatique de nœuds avec espacement optimal
- Ajustement dynamique de la largeur selon le contenu
- Affichage des correspondances correctes dans le corrigé
- Mélange aléatoire des réponses

## Fonctionnalités

- **Conversion HTML vers LaTeX** : Traitement automatique des balises HTML courantes (`<tt>`, caractères spéciaux)
- **Génération de corrigés** : Affichage des bonnes réponses avec code couleur
- **Mise en page automatique** : Formatage LaTeX optimisé avec macros personnalisées
- **Support TikZ** : Création de graphiques pour les questions d'appariement
- **Filtrage intelligent** : Ignore automatiquement les fichiers `category.qtex`

## Packages LaTeX requis

Le code LaTeX généré nécessite les packages suivants :

```latex
\usepackage{xcolor}
\usepackage{tikz}
\usepackage{pifont} % pour les symboles ✓ et ✗
\usetikzlibrary{calc}
```

C.f le paquet qtex2pdf utilise qtex2latex pour générer un aperçu de la question au format pdf.

## Licence

Ce script fait partie du projet QTEX.
