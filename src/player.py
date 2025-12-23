
from turtle import RawTurtle

class Player:
    def __init__(self, maze, screen, cell_size=40):
        self.maze = maze
        self.cell_size = cell_size
        self.turtle = RawTurtle(screen)
        self.turtle.speed(0)
        self.turtle.shape("turtle")
        self.turtle.color("black")
        self.turtle.penup()
        
        self.row = 0
        self.col = 0
        
        # Initialize at start position
        if self.maze.start_pos:
            self.teleport(*self.maze.start_pos)
            self.turtle.showturtle()
        else:
            self.turtle.hideturtle()

    def teleport(self, r, c):
        """Teleport player to grid coordinates (r, c)."""
        self.row = r
        self.col = c
        x, y = self.grid_to_screen(r, c)
        self.turtle.goto(x, y)

    def grid_to_screen(self, r, c):
        """Convert grid rows/cols to screen x/y based on center origin."""
        # Screen (0,0) is center.
        # Maze top-left should be offset so the whole maze is centered.
        
        total_width = self.maze.cols * self.cell_size
        total_height = self.maze.rows * self.cell_size
        
        start_x = -total_width // 2
        start_y = total_height // 2
        
        # Center of the cell
        x = start_x + (c * self.cell_size) + (self.cell_size // 2)
        y = start_y - (r * self.cell_size) - (self.cell_size // 2)
        return x, y

    def move(self, dr, dc):
        """Attempt to move by (dr, dc)."""
        new_r = self.row + dr
        new_c = self.col + dc
        
        if not self.maze.is_wall(new_r, new_c):
            # Calculate heading
            if dr == -1: self.turtle.setheading(90)  # Up
            elif dr == 1: self.turtle.setheading(270) # Down
            elif dc == -1: self.turtle.setheading(180) # Left
            elif dc == 1: self.turtle.setheading(0)   # Right
            
            # Move logic
            self.row = new_r
            self.col = new_c
            target_x, target_y = self.grid_to_screen(self.row, self.col)
            
            # Smooth move (optional, but stick to step for now)
            self.turtle.goto(target_x, target_y)
            return True # Moved successfully
        else:
            return False # Hit wall

