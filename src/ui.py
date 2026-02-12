
import tkinter as tk
from tkinter import ttk
from turtle import TurtleScreen, RawTurtle

# Theme definitions: wall, passage, start, end, bg, accent
THEMES = {
    "Classique": {
        "wall": "#2c3e50", "passage": "#ecf0f1", "start": "#2ecc71",
        "end": "#e74c3c", "bg": "#bdc3c7", "accent": "#3498db",
        "fog": "#7f8c8d", "hint": "#f39c12",
    },
    "Ocean": {
        "wall": "#1a3c5e", "passage": "#d4f1f9", "start": "#00e676",
        "end": "#ff5252", "bg": "#90caf9", "accent": "#0288d1",
        "fog": "#37474f", "hint": "#ffab40",
    },
    "Foret": {
        "wall": "#1b5e20", "passage": "#e8f5e9", "start": "#ffd600",
        "end": "#d50000", "bg": "#a5d6a7", "accent": "#388e3c",
        "fog": "#33691e", "hint": "#ff6d00",
    },
    "Nuit": {
        "wall": "#0d0d0d", "passage": "#1a1a2e", "start": "#00ff87",
        "end": "#ff2e63", "bg": "#16213e", "accent": "#533483",
        "fog": "#0a0a0a", "hint": "#e94560",
    },
}


class GameUI:
    def __init__(self, root, game_instance):
        self.root = root
        self.game = game_instance
        self.cell_size = 40
        self.current_theme = "Classique"
        self.fog_enabled = False
        self.fog_radius = 3
        self.hint_turtles = []
        self.fog_turtles = []
        self.drawer = None
        self.setup_window()
        self.setup_widgets()
        
    def setup_window(self):
        self.root.title("Labyrinthe Aventure")
        self.root.geometry("950x750")
        self.root.configure(bg="#2c3e50")
        self.root.minsize(700, 550)
        
    def setup_widgets(self):
        style = ttk.Style()
        style.theme_use("clam")

        # === Top Frame: Action Buttons ===
        self.frame_top = tk.Frame(self.root, bg="#34495e", height=50)
        self.frame_top.pack(side=tk.TOP, fill=tk.X)

        btn_font = ("Segoe UI", 10, "bold")
        btn_pad = {"padx": 5, "pady": 6}

        self.btn_restart = tk.Button(self.frame_top, text="Recommencer", command=self.game.restart_game,
                                     bg="#27ae60", fg="white", font=btn_font, relief="flat", cursor="hand2")
        self.btn_restart.pack(side=tk.LEFT, **btn_pad)

        self.btn_explore = tk.Button(self.frame_top, text="Auto-Solve", command=self.game.start_auto_solve,
                                     bg="#2980b9", fg="white", font=btn_font, relief="flat", cursor="hand2")
        self.btn_explore.pack(side=tk.LEFT, **btn_pad)

        self.btn_hint = tk.Button(self.frame_top, text="Indice", command=self.game.show_hint,
                                  bg="#f39c12", fg="white", font=btn_font, relief="flat", cursor="hand2")
        self.btn_hint.pack(side=tk.LEFT, **btn_pad)

        self.btn_new_maze = tk.Button(self.frame_top, text="Nouveau Labyrinthe", command=self.game.generate_new_maze,
                                      bg="#8e44ad", fg="white", font=btn_font, relief="flat", cursor="hand2")
        self.btn_new_maze.pack(side=tk.LEFT, **btn_pad)

        # Fog of war toggle
        self.fog_var = tk.BooleanVar(value=False)
        self.chk_fog = tk.Checkbutton(self.frame_top, text="Brouillard", variable=self.fog_var,
                                       command=self.toggle_fog, bg="#34495e", fg="white",
                                       selectcolor="#2c3e50", font=("Segoe UI", 10),
                                       activebackground="#34495e", activeforeground="white")
        self.chk_fog.pack(side=tk.LEFT, **btn_pad)

        # Theme selector
        tk.Label(self.frame_top, text="Theme:", bg="#34495e", fg="white",
                 font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=(10, 2))
        self.theme_var = tk.StringVar(value=self.current_theme)
        self.theme_combo = ttk.Combobox(self.frame_top, textvariable=self.theme_var,
                                         values=list(THEMES.keys()), state="readonly", width=10)
        self.theme_combo.pack(side=tk.LEFT, padx=2, pady=6)
        self.theme_combo.bind("<<ComboboxSelected>>", self.on_theme_change)

        # Level selector
        tk.Label(self.frame_top, text="Niveau:", bg="#34495e", fg="white",
                 font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=(10, 2))
        self.level_var = tk.IntVar(value=1)
        self.level_spin = tk.Spinbox(self.frame_top, from_=1, to=15, textvariable=self.level_var,
                                      width=3, font=("Segoe UI", 10), command=self.game.generate_new_maze)
        self.level_spin.pack(side=tk.LEFT, padx=2, pady=6)

        self.btn_quit = tk.Button(self.frame_top, text="Quitter", command=self.root.destroy,
                                  bg="#c0392b", fg="white", font=btn_font, relief="flat", cursor="hand2")
        self.btn_quit.pack(side=tk.RIGHT, **btn_pad)

        # === Middle Frame: Turtle Canvas ===
        self.frame_canvas = tk.Frame(self.root, bg="#2c3e50")
        self.frame_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.canvas = tk.Canvas(self.frame_canvas, width=900, height=550, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.screen = TurtleScreen(self.canvas)
        self.screen.bgcolor(THEMES[self.current_theme]["bg"])
        
        # === Bottom Frame: Stats ===
        self.frame_bottom = tk.Frame(self.root, bg="#34495e", height=60)
        self.frame_bottom.pack(side=tk.BOTTOM, fill=tk.X)

        stats_font = ("Segoe UI", 11)
        
        self.lbl_status = tk.Label(self.frame_bottom, text="Bienvenue dans le Labyrinthe!",
                                   bg="#34495e", fg="#ecf0f1", font=("Segoe UI", 11, "bold"))
        self.lbl_status.pack(side=tk.LEFT, padx=15, pady=8)

        self.lbl_timer = tk.Label(self.frame_bottom, text="Temps: 0s",
                                  bg="#34495e", fg="#f1c40f", font=stats_font)
        self.lbl_timer.pack(side=tk.RIGHT, padx=15, pady=8)

        self.lbl_moves = tk.Label(self.frame_bottom, text="Mouvements: 0",
                                  bg="#34495e", fg="#3498db", font=stats_font)
        self.lbl_moves.pack(side=tk.RIGHT, padx=15, pady=8)

        self.lbl_score = tk.Label(self.frame_bottom, text="Score: 0",
                                  bg="#34495e", fg="#2ecc71", font=stats_font)
        self.lbl_score.pack(side=tk.RIGHT, padx=15, pady=8)

        self.lbl_level = tk.Label(self.frame_bottom, text="Niveau: 1",
                                  bg="#34495e", fg="#e67e22", font=stats_font)
        self.lbl_level.pack(side=tk.RIGHT, padx=15, pady=8)

    def get_theme(self):
        return THEMES.get(self.current_theme, THEMES["Classique"])

    def on_theme_change(self, event=None):
        self.current_theme = self.theme_var.get()
        self.game.redraw_current_maze()

    def toggle_fog(self):
        self.fog_enabled = self.fog_var.get()
        self.game.redraw_current_maze()

    def calculate_cell_size(self, maze):
        cw = 900
        ch = 550
        try:
             cw = self.canvas.winfo_width()
             ch = self.canvas.winfo_height()
             if cw <= 1 or ch <= 1:
                 cw = 900
                 ch = 550
        except:
            pass
            
        max_w = cw - 40
        max_h = ch - 40
        
        size_w = max_w // maze.cols
        size_h = max_h // maze.rows
        
        self.cell_size = min(size_w, size_h, 40)
        self.cell_size = max(self.cell_size, 8)

    def draw_maze(self, maze, player_pos=None):
        theme = self.get_theme()
        self.screen.tracer(0)
        self.screen.bgcolor(theme["bg"])

        # Clear previous drawings
        if self.drawer:
            self.drawer.clear()
        self.clear_fog()
        self.clear_hints()

        self.drawer = RawTurtle(self.screen)
        self.drawer.hideturtle()
        self.drawer.speed(0)
        self.drawer.pensize(1)
        
        rows = maze.rows
        cols = maze.cols
        
        total_width = cols * self.cell_size
        total_height = rows * self.cell_size
        start_x = -total_width // 2
        start_y = total_height // 2

        visible = None
        if self.fog_enabled and player_pos:
            visible = self._get_visible_cells(player_pos, maze)
        
        for r in range(rows):
            for c in range(cols):
                val = maze.grid[r][c]

                # Fog of war: hide cells not visible
                if visible is not None and (r, c) not in visible:
                    color = theme["fog"]
                elif val == 1:
                    color = theme["wall"]
                elif maze.start_pos == (r, c):
                    color = theme["start"]
                elif maze.end_pos == (r, c):
                    color = theme["end"]
                else:
                    color = theme["passage"]
                
                x = start_x + (c * self.cell_size)
                y = start_y - (r * self.cell_size) 
                
                self.drawer.penup()
                self.drawer.goto(x, y)
                self.drawer.pendown()
                self.drawer.pencolor(theme["bg"])
                self.drawer.fillcolor(color)
                self.drawer.begin_fill()
                for _ in range(4):
                    self.drawer.forward(self.cell_size)
                    self.drawer.right(90)
                self.drawer.end_fill()
                
        self.drawer.penup()
        self.drawer.hideturtle()
        self.screen.update()
        self.screen.tracer(1)

    def _get_visible_cells(self, player_pos, maze):
        """Return set of (r,c) cells visible from player position within fog_radius."""
        pr, pc = player_pos
        visible = set()
        for dr in range(-self.fog_radius, self.fog_radius + 1):
            for dc in range(-self.fog_radius, self.fog_radius + 1):
                if dr * dr + dc * dc <= self.fog_radius * self.fog_radius:
                    r, c = pr + dr, pc + dc
                    if 0 <= r < maze.rows and 0 <= c < maze.cols:
                        visible.add((r, c))
        return visible

    def draw_hint_path(self, maze, path, player_grid_to_screen):
        """Draw hint markers along the optimal path."""
        self.clear_hints()
        theme = self.get_theme()
        self.screen.tracer(0)
        for r, c in path[1:]:  # Skip current position
            t = RawTurtle(self.screen)
            t.hideturtle()
            t.speed(0)
            t.penup()
            x, y = player_grid_to_screen(r, c)
            t.goto(x, y)
            t.dot(max(6, self.cell_size // 3), theme["hint"])
            self.hint_turtles.append(t)
        self.screen.update()
        self.screen.tracer(1)

    def clear_hints(self):
        for t in self.hint_turtles:
            t.clear()
            t.hideturtle()
        self.hint_turtles = []

    def clear_fog(self):
        for t in self.fog_turtles:
            t.clear()
            t.hideturtle()
        self.fog_turtles = []

    def update_status(self, text):
        self.lbl_status.config(text=text)

    def update_moves(self, count):
        self.lbl_moves.config(text=f"Mouvements: {count}")

    def update_timer(self, seconds):
        mins = int(seconds) // 60
        secs = int(seconds) % 60
        self.lbl_timer.config(text=f"Temps: {mins:02d}:{secs:02d}")

    def update_score(self, score):
        self.lbl_score.config(text=f"Score: {score}")

    def update_level_display(self, level):
        self.lbl_level.config(text=f"Niveau: {level}")
