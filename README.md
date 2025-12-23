# Jeu du Labyrinthe 🐢

Un jeu de labyrinthe interactif écrit en Python avec `turtle` et `tkinter`.

## Fonctionnalités

-   **Déplacement manuel** : Utilisez les flèches du clavier pour guider la tortue vers la sortie ('X').
-   **Génération dynamique** : Le jeu charge le labyrinthe depuis `labyrinthe.txt` et s'adapte à toutes les tailles.
-   **Exploration Automatique** : Cliquez sur le bouton "Exploration Auto" pour voir une IA (DFS) résoudre le labyrinthe.
-   **Physique** : Collisions avec les murs, détection de victoire.

## Installation

Assurez-vous d'avoir Python 3 installé.

```bash
# Clonez ce dépôt (si applicable) ou téléchargez les fichiers
cd snake
```

## Lancement

Pour lancer le jeu :

```bash
python3 main.py
```

## Personnalisation

Vous pouvez modifier le fichier `labyrinthe.txt` pour créer vos propres niveaux :
-   `#` : Mur
-   `.` : Passage
-   `x` : Départ
-   `X` : Sortie

Amusez-vous bien !
