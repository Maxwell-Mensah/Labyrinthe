# Labyrinthe Aventure 🐢

Un jeu de labyrinthe interactif et complet ecrit en Python avec `turtle` et `tkinter`.

## Fonctionnalites

### Gameplay
-   **Deplacement manuel** : Utilisez les fleches du clavier pour guider la tortue vers la sortie.
-   **Generation aleatoire** : Labyrinthes generes automatiquement avec l'algorithme de recursive backtracking.
-   **15 niveaux de difficulte** : Labyrinthes de plus en plus grands et complexes, avec progression automatique.
-   **Exploration Automatique** : IA (DFS) qui resout le labyrinthe devant vos yeux.

### Systeme de score
-   **Compteur de mouvements** : Suivez le nombre de pas effectues.
-   **Chronometre** : Temps ecoule en temps reel.
-   **Score** : Calcule selon l'efficacite (proximite du chemin optimal), le temps, et les indices utilises.
-   **Score cumule** : Le score se cumule a travers les niveaux.

### Fonctionnalites avancees
-   **Systeme d'indices** : Cliquez sur "Indice" pour voir les prochains pas du chemin optimal (penalite de score).
-   **Brouillard de guerre** : Activez le mode "Brouillard" pour une vision limitee autour du joueur.
-   **4 themes visuels** : Classique, Ocean, Foret, Nuit - changez en temps reel.
-   **Trace du joueur** : Visualisez votre parcours avec des points sur les cases visitees.

## Installation

Assurez-vous d'avoir Python 3 installe. Aucune dependance externe requise.

```bash
git clone <url-du-depot>
cd snake
```

## Lancement

```bash
python3 main.py
```

Choisissez le mode 1 (genere) pour jouer directement, ou le mode 2 pour charger un fichier personnalise.

## Controles

| Touche / Bouton | Action |
|---|---|
| Fleches directionnelles | Deplacer la tortue |
| Recommencer | Reinitialiser le niveau |
| Auto-Solve | Laisser l'IA resoudre |
| Indice | Afficher le chemin optimal (3s) |
| Nouveau Labyrinthe | Generer un nouveau labyrinthe |
| Brouillard | Activer/desactiver le fog of war |
| Theme | Changer le theme visuel |
| Niveau | Selectionner la difficulte |

## Personnalisation

Vous pouvez creer vos propres niveaux dans un fichier `.txt` :
-   `#` : Mur
-   `.` : Passage
-   `x` : Depart
-   `X` : Sortie

Exemple :
```
#########
#x......#
#.#####.#
#.#...#.#
#.#.#.#.#
#...#...X
#########
```

## Architecture

```
snake/
├── main.py              # Point d'entree
├── labyrinthe.txt       # Labyrinthe exemple
├── README.md
└── src/
    ├── game.py          # Logique du jeu, timer, score, niveaux
    ├── maze.py          # Modele du labyrinthe, BFS shortest path
    ├── player.py        # Joueur, mouvements, trace
    ├── generator.py     # Generation aleatoire de labyrinthes
    ├── solver.py        # Solveur DFS automatique
    └── ui.py            # Interface graphique, themes, fog of war
```

Amusez-vous bien !
