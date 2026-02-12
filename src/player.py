
from turtle import RawTurtle

class Player:
    def __init__(self, maze, screen, cell_size=40):
        self.maze = maze
        self.screen = screen
        self.cell_size = cell_size
        self.turtle = RawTurtle(screen)
        self.turtle.speed(0)
        self.turtle.shape("turtle")
        self.turtle.color("#2d2d2d")
        self.turtle.penup()
        self.turtle.shapesize(cell_size / 30, cell_size / 30)
        
        self.row = 0
        self.col = 0
        self.move_count = 0
        self.visited_cells = set()
        self.trail_turtles = []
        
        # Initialize at start position
        if self.maze.start_pos:
            self.teleport(*self.maze.start_pos)
            self.visited_cells.add(self.maze.start_pos)
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
        total_width = self.maze.cols * self.cell_size
        total_height = self.maze.rows * self.cell_size
        
        start_x = -total_width // 2
        start_y = total_height // 2
        
        # Center of the cell
        x = start_x + (c * self.cell_size) + (self.cell_size // 2)
        y = start_y - (r * self.cell_size) - (self.cell_size // 2)
        return x, y

    def draw_trail_dot(self, r, c):
        """Draw a small dot on a visited cell to show the trail."""
        self.screen.tracer(0)
        t = RawTurtle(self.screen)
        t.hideturtle()
        t.speed(0)
        t.penup()
        x, y = self.grid_to_screen(r, c)
        t.goto(x, y)
        t.dot(max(4, self.cell_size // 6), "#a0d2db")
        self.trail_turtles.append(t)
        self.screen.update()
        self.screen.tracer(1)

    def clear_trail(self):
        """Remove all trail dots."""
        for t in self.trail_turtles:
            t.clear()
            t.hideturtle()
        self.trail_turtles = []

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
            
            # Leave trail on current cell before moving
            self.draw_trail_dot(self.row, self.col)
            
            # Move logic
            self.row = new_r
            self.col = new_c
            self.move_count += 1
            self.visited_cells.add((new_r, new_c))
            target_x, target_y = self.grid_to_screen(self.row, self.col)
            
            self.turtle.goto(target_x, target_y)
            return True # Moved successfully
        else:
            return False # Hit wall

    def reset_stats(self):
        """Reset move counter and visited cells."""
        self.move_count = 0
        self.visited_cells.clear()
        self.clear_trail()
        if self.maze.start_pos:
            self.visited_cells.add(self.maze.start_pos)

