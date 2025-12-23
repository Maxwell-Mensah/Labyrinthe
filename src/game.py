
import tkinter as tk
from .maze import Maze
from .ui import GameUI
from .player import Player

class Game:
    def __init__(self, maze_file):
        self.root = tk.Tk()
        self.maze_file = maze_file
        
        # Initialize UI first to get the screen
        self.ui = GameUI(self.root, self)
        
        # Load Maze
        try:
            self.maze = Maze(self.maze_file)
            self.ui.calculate_cell_size(self.maze)
            self.ui.draw_maze(self.maze)
        except Exception as e:
            print(f"Error loading maze: {e}")
            self.ui.update_status(f"Erreur chargement: {e}")
            return

        # Initialize Player
        self.player = None
        self.setup_player()
        
        # Bind Keys
        self.ui.screen.onkeypress(self.move_up, "Up")
        self.ui.screen.onkeypress(self.move_down, "Down")
        self.ui.screen.onkeypress(self.move_left, "Left")
        self.ui.screen.onkeypress(self.move_right, "Right")
        self.ui.screen.listen()

    def setup_player(self):
        if self.player:
            self.player.turtle.clear()
            self.player.turtle.hideturtle()
            
        self.player = Player(self.maze, self.ui.screen, self.ui.cell_size)
    
    def move_up(self): self.handle_move(-1, 0)
    def move_down(self): self.handle_move(1, 0)
    def move_left(self): self.handle_move(0, -1)
    def move_right(self): self.handle_move(0, 1)
    
    def handle_move(self, dr, dc):
        if self.player.move(dr, dc):
            self.check_win()
        else:
            self.ui.update_status("Mur! Impossible de passer.")

    def check_win(self):
        if self.maze.is_exit(self.player.row, self.player.col):
            self.ui.update_status("Victoire! 🎉")
            self.ui.screen.bgcolor("lightgreen")
        else:
            self.ui.update_status(f"Position: {self.player.row}, {self.player.col}")

    def restart_game(self):
        self.ui.screen.bgcolor("white")
        self.ui.update_status("Recommencé!")
        self.player.teleport(*self.maze.start_pos)

    def start_auto_solve(self):
        from .solver import Solver
        solver = Solver(self.maze)
        self.solver_gen = solver.solve_generator((self.player.row, self.player.col))
        self.ui.update_status("Exploration en cours...")
        self.auto_solve_step()

    def auto_solve_step(self):
        try:
            dr, dc = next(self.solver_gen)
            self.handle_move(dr, dc)
            # Schedule next step (adjust time for speed)
            if not self.maze.is_exit(self.player.row, self.player.col):
                self.root.after(100, self.auto_solve_step)
        except StopIteration:
            self.ui.update_status("Exploration terminée.")

    def run(self):
        self.root.mainloop()
