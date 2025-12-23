
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.game import Game

def main():
    print("Bienvenue dans le jeu du Labyrinthe!")
    default_file = "labyrinthe.txt"
    filename = input(f"Entrez le fichier du labyrinthe (defaut: {default_file}): ").strip()
    if not filename:
        filename = default_file
        
    if not os.path.exists(filename):
        print(f"Erreur: Le fichier '{filename}' n'existe pas.")
        # Create a default one if missing for demo purposes
        print("Création d'un labyrinthe par défaut...")
        with open(default_file, "w") as f:
            f.write("#######\n#x... #\n#.#.#.#\n#...#.X\n#######\n")
        filename = default_file

    app = Game(filename)
    app.run()

if __name__ == "__main__":
    main()
