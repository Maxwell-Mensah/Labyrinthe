
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.game import Game

def main():
    print("=" * 50)
    print("   Labyrinthe Aventure")
    print("=" * 50)
    print()
    print("Options:")
    print("  1. Jouer avec un labyrinthe genere (recommande)")
    print("  2. Charger un fichier labyrinthe")
    print()
    
    choice = input("Votre choix (1/2, defaut: 1): ").strip()
    
    if choice == "2":
        default_file = "labyrinthe.txt"
        filename = input(f"Fichier du labyrinthe (defaut: {default_file}): ").strip()
        if not filename:
            filename = default_file
            
        if not os.path.exists(filename):
            print(f"Erreur: Le fichier '{filename}' n'existe pas.")
            print("Creation d'un labyrinthe par defaut...")
            with open(default_file, "w") as f:
                f.write("#######\n#x... #\n#.#.#.#\n#...#.X\n#######\n")
            filename = default_file

        app = Game(maze_file=filename)
    else:
        print("Generation d'un labyrinthe aleatoire...")
        app = Game()
    
    app.run()

if __name__ == "__main__":
    main()
