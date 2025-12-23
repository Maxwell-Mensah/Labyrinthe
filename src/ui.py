
import tkinter as tk
from turtle import Canvas, TurtleScreen, RawTurtle

class GameUI:
    def __init__(self, root, game_instance):
        self.root = root
        self.game = game_instance
        self.cell_size = 40
        self.setup_window()
        self.setup_widgets()
        
    def setup_window(self):
        self.root.title("Labyrinthe Fun - Refactored")
        self.root.geometry("850x700")
        
    def setup_widgets(self):
        # Top Frame: Buttons
        self.frame_top = tk.Frame(self.root, bg="lightgray", height=50)
        self.frame_top.pack(side=tk.TOP, fill=tk.X)
        
        self.btn_restart = tk.Button(self.frame_top, text="Recommencer", command=self.game.restart_game, bg="green", fg="white", font=("Arial", 12))
        self.btn_restart.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.btn_quit = tk.Button(self.frame_top, text="Quitter", command=self.root.destroy, bg="red", fg="white", font=("Arial", 12))
        self.btn_quit.pack(side=tk.RIGHT, padx=10, pady=10)

        self.btn_explore = tk.Button(self.frame_top, text="Exploration Auto", command=self.game.start_auto_solve, bg="blue", fg="white", font=("Arial", 12))
        self.btn_explore.pack(side=tk.LEFT, padx=10, pady=10)

        # Middle Frame: Turtle Canvas
        self.frame_canvas = tk.Frame(self.root, width=800, height=500, bg="blue")
        self.frame_canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.frame_canvas, width=800, height=500)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.screen = TurtleScreen(self.canvas)
        self.screen.bgcolor("white")
        
        # Bottom Frame: Stats
        self.frame_bottom = tk.Frame(self.root, bg="lightgray", height=100)
        self.frame_bottom.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.lbl_status = tk.Label(self.frame_bottom, text="Bienvenue!", bg="lightgray", font=("Arial", 12))
        self.lbl_status.pack(pady=10)

    def calculate_cell_size(self, maze):
        # Default canvas size if not yet rendered
        cw = 800
        ch = 500
        try:
             cw = self.canvas.winfo_width()
             ch = self.canvas.winfo_height()
             if cw <= 1 or ch <= 1: # Window not fully drawn yet
                 cw = 800
                 ch = 500
        except:
            pass
            
        max_w = cw - 40 # 20px margin
        max_h = ch - 40
        
        size_w = max_w // maze.cols
        size_h = max_h // maze.rows
        
        # Set dynamic size, capped at 40
        self.cell_size = min(size_w, size_h, 40)
        # Ensure at least a reasonable minimum
        self.cell_size = max(self.cell_size, 10)

    def draw_maze(self, maze):
        self.screen.tracer(0) # Disable animation for fast drawing
        drawer = RawTurtle(self.screen)
        drawer.hideturtle()
        drawer.speed(0)
        
        rows = maze.rows
        cols = maze.cols
        
        total_width = cols * self.cell_size
        total_height = rows * self.cell_size
        start_x = -total_width // 2
        start_y = total_height // 2
        
        for r in range(rows):
            for c in range(cols):
                val = maze.grid[r][c]
                # Determine color
                if val == 1: color = "black"
                elif maze.start_pos == (r, c): color = "lime"
                elif maze.end_pos == (r, c): color = "skyblue"
                else: color = "white"
                
                # Calculate pos
                x = start_x + (c * self.cell_size)
                y = start_y - (r * self.cell_size) 
                
                # Draw square (top-left origin for drawing)
                drawer.penup()
                drawer.goto(x, y)
                drawer.pendown()
                drawer.fillcolor(color)
                drawer.begin_fill()
                for _ in range(4):
                    drawer.forward(self.cell_size)
                    drawer.right(90)
                drawer.end_fill()
                
        self.screen.update()
        self.screen.tracer(1) # Re-enable animation for the player

    def update_status(self, text):
        self.lbl_status.config(text=text)
