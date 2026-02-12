
import tkinter as tk
import time
from .maze import Maze
from .ui import GameUI
from .player import Player
from .generator import MazeGenerator


class Game:
    def __init__(self, maze_file=None):
        self.root = tk.Tk()
        self.maze_file = maze_file
        self.current_level = 1
        self.total_score = 0
        self.game_won = False
        self.hints_used = 0
        self.start_time = None
        self.timer_id = None
        self.elapsed = 0
        
        # Initialize UI first to get the screen
        self.ui = GameUI(self.root, self)
        
        # Load Maze (from file or generate level 1)
        self.maze = None
        self.player = None

        if maze_file:
            try:
                self.maze = Maze(self.maze_file)
            except Exception as e:
                print(f"Error loading maze: {e}")
                self.ui.update_status(f"Erreur chargement: {e}")
                self._generate_level(1)
        else:
            self._generate_level(1)

        self._init_level()
        
        # Bind Keys
        self.ui.screen.onkeypress(self.move_up, "Up")
        self.ui.screen.onkeypress(self.move_down, "Down")
        self.ui.screen.onkeypress(self.move_left, "Left")
        self.ui.screen.onkeypress(self.move_right, "Right")
        self.ui.screen.listen()

    def _generate_level(self, level):
        """Generate a random maze for the given level."""
        rows, cols = MazeGenerator.difficulty_settings(level)
        grid, start_pos, end_pos = MazeGenerator.generate(rows, cols)
        self.maze = Maze(grid=grid, start_pos=start_pos, end_pos=end_pos)

    def _init_level(self):
        """Initialize/reinitialize the current level display."""
        if not self.maze:
            return
        self.game_won = False
        self.hints_used = 0
        self.ui.calculate_cell_size(self.maze)
        self.ui.draw_maze(self.maze)
        self.setup_player()
        self.ui.update_level_display(self.current_level)
        self.ui.update_score(self.total_score)
        self.start_timer()

    def setup_player(self):
        if self.player:
            self.player.turtle.clear()
            self.player.turtle.hideturtle()
            self.player.clear_trail()
            
        self.ui.screen.tracer(0)
        self.player = Player(self.maze, self.ui.screen, self.ui.cell_size)
        self.ui.screen.update()
        self.ui.screen.tracer(1)
        self.ui.update_moves(0)
    
    def move_up(self): self.handle_move(-1, 0)
    def move_down(self): self.handle_move(1, 0)
    def move_left(self): self.handle_move(0, -1)
    def move_right(self): self.handle_move(0, 1)
    
    def handle_move(self, dr, dc):
        if self.game_won:
            return
        if self.player.move(dr, dc):
            self.ui.update_moves(self.player.move_count)
            # Redraw maze if fog is enabled (to update visibility)
            if self.ui.fog_enabled:
                self.redraw_current_maze()
            self.check_win()
        else:
            self.ui.update_status("Mur! Impossible de passer.")

    def check_win(self):
        if self.maze.is_exit(self.player.row, self.player.col):
            self.game_won = True
            self.stop_timer()
            score = self._calculate_score()
            self.total_score += score
            self.ui.update_score(self.total_score)
            
            # Optimal path length for reference
            optimal = len(self.maze.shortest_path(self.maze.start_pos, self.maze.end_pos))
            
            msg = (f"Victoire! Niveau {self.current_level} termine! "
                   f"Score: +{score} | Mouvements: {self.player.move_count} "
                   f"(optimal: {optimal}) | Temps: {int(self.elapsed)}s")
            self.ui.update_status(msg)
            
            # Flash victory effect
            theme = self.ui.get_theme()
            self.ui.screen.bgcolor(theme["start"])
            self.root.after(500, lambda: self.ui.screen.bgcolor(theme["bg"]))
            
            # Auto-advance to next level after delay
            self.root.after(2500, self._prompt_next_level)
        else:
            self.ui.update_status(f"Pos: ({self.player.row},{self.player.col}) | "
                                  f"Mouvements: {self.player.move_count}")

    def _calculate_score(self):
        """Calculate score based on moves, time, hints, and level."""
        optimal = len(self.maze.shortest_path(self.maze.start_pos, self.maze.end_pos))
        if optimal == 0:
            optimal = 1
        
        # Base score from level
        base = self.current_level * 1000
        
        # Efficiency bonus (how close to optimal path)
        efficiency = max(0, optimal / max(self.player.move_count, 1))
        move_bonus = int(base * efficiency)
        
        # Time bonus (faster = more points)
        time_bonus = max(0, int(500 - self.elapsed * 2))
        
        # Hint penalty
        hint_penalty = self.hints_used * 200
        
        return max(100, move_bonus + time_bonus - hint_penalty)

    def _prompt_next_level(self):
        """Advance to next level."""
        self.current_level += 1
        self.ui.level_var.set(self.current_level)
        self.generate_new_maze()

    def restart_game(self):
        """Restart current level."""
        self.stop_timer()
        self.ui.clear_hints()
        if self.player:
            self.player.reset_stats()
            self.player.teleport(*self.maze.start_pos)
        self.game_won = False
        self.hints_used = 0
        self.ui.update_moves(0)
        self.ui.update_status("Recommence!")
        self.redraw_current_maze()
        self.start_timer()

    def generate_new_maze(self):
        """Generate a new random maze at the selected level."""
        self.stop_timer()
        level = self.ui.level_var.get()
        self.current_level = level
        self._generate_level(level)
        self._init_level()
        self.ui.update_status(f"Nouveau labyrinthe - Niveau {level}!")

    def redraw_current_maze(self):
        """Redraw the maze (used for theme/fog changes)."""
        if not self.maze:
            return
        player_pos = None
        if self.player:
            player_pos = (self.player.row, self.player.col)
        self.ui.calculate_cell_size(self.maze)
        self.ui.draw_maze(self.maze, player_pos=player_pos)
        # Re-setup player on new drawing
        if self.player:
            old_r, old_c = self.player.row, self.player.col
            old_moves = self.player.move_count
            old_visited = self.player.visited_cells.copy()
            old_heading = self.player.turtle.heading()
            self.player.turtle.clear()
            self.player.turtle.hideturtle()
            self.player.clear_trail()
            self.ui.screen.tracer(0)
            self.player = Player(self.maze, self.ui.screen, self.ui.cell_size)
            self.player.teleport(old_r, old_c)
            self.player.turtle.setheading(old_heading)
            self.player.move_count = old_moves
            self.player.visited_cells = old_visited
            self.ui.screen.update()
            self.ui.screen.tracer(1)

    def show_hint(self):
        """Show the optimal path from current position to exit."""
        if self.game_won or not self.player or not self.maze.end_pos:
            return
        self.hints_used += 1
        path = self.maze.shortest_path(
            (self.player.row, self.player.col), self.maze.end_pos
        )
        if path:
            # Show only next few steps (not the whole path)
            hint_steps = path[:min(6, len(path))]
            self.ui.draw_hint_path(self.maze, hint_steps, self.player.grid_to_screen)
            self.ui.update_status(f"Indice: {len(path)-1} pas restants (indice #{self.hints_used})")
            # Auto-clear hint after 3 seconds
            self.root.after(3000, self.ui.clear_hints)
        else:
            self.ui.update_status("Aucun chemin trouve!")

    def start_auto_solve(self):
        if self.game_won:
            return
        from .solver import Solver
        solver = Solver(self.maze)
        self.solver_gen = solver.solve_generator((self.player.row, self.player.col))
        self.ui.update_status("Exploration automatique en cours...")
        self.auto_solve_step()

    def auto_solve_step(self):
        try:
            dr, dc = next(self.solver_gen)
            self.handle_move(dr, dc)
            if not self.maze.is_exit(self.player.row, self.player.col):
                speed = max(20, 150 - self.current_level * 10)
                self.root.after(speed, self.auto_solve_step)
        except StopIteration:
            self.ui.update_status("Exploration terminee.")

    # === Timer ===
    def start_timer(self):
        self.start_time = time.time()
        self.elapsed = 0
        self.ui.update_timer(0)
        self._tick_timer()

    def _tick_timer(self):
        if self.start_time and not self.game_won:
            self.elapsed = time.time() - self.start_time
            self.ui.update_timer(self.elapsed)
            self.timer_id = self.root.after(500, self._tick_timer)

    def stop_timer(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

    def run(self):
        self.root.mainloop()
