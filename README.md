# Projet Python - Rattrapage ISUP 2025

**Nom :** Sihem YENBOU

**Mail :** yenbousihem@gmail.com

**GitHub :** https://github.com/sihemynb/Projet-Rattrapage

## Présentation

Ce projet a été réalisé dans le cadre du rattrapage du cours de Python du Master 1 ISDS (ISUP), en mai-juin 2025.

L'objectif est d'analyser des données de la NBA à partir de plusieurs fichiers `.csv`, en utilisant exclusivement les bibliothèques `numpy`, `pandas`, `matplotlib` et `seaborn`.

Le projet est structuré comme un package Python, et les scripts ont été développés sans utiliser de bibliothèques comme `sklearn` ou `statsmodels`.

## Fonctionnalités développées

- **Leaderboard** : affichage des meilleurs joueurs selon des critères choisis (statistique, saison, playoffs/saison régulière).
- **Fiche descriptive d’équipe** : résumé des performances d'une équipe pour une saison donnée.
- **Modèle de régression linéaire** : implémentation de la méthode des moindres carrés pour prédire le salaire d’un joueur à partir de ses performances.

## Utilisation

Le projet est exécutable à l’aide de scripts en ligne de commande. Les données sont à placer dans un dossier `data/`.

Exemple d’exécution :
```bash
python scripts/run_leaderboard.py

