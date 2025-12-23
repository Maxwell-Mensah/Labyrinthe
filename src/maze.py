
class Maze:
    def __init__(self, filename):
        self.filename = filename
        self.grid = []
        self.start_pos = None
        self.end_pos = None
        self.load_maze()

    def load_maze(self):
        """Loads the maze from a file."""
        try:
            with open(self.filename, 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            raise FileNotFoundError(f"Maze file '{self.filename}' not found.")

        for r, line in enumerate(lines):
            row = []
            for c, char in enumerate(line.strip()):
                if char == '#':
                    row.append(1) # Wall
                elif char == '.':
                    row.append(0) # Passage
                elif char == 'x':
                    row.append(0)
                    self.start_pos = (r, c)
                elif char == 'X':
                    row.append(0)
                    self.end_pos = (r, c)
                else:
                    row.append(1) # Treat unknown as wall default
            self.grid.append(row)

    @property
    def rows(self):
        return len(self.grid)

    @property
    def cols(self):
        return len(self.grid[0]) if self.grid else 0

    def is_wall(self, r, c):
        """Returns True if the cell (r, c) is a wall or out of bounds."""
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            return True
        return self.grid[r][c] == 1

    def is_passage(self, r, c):
        return not self.is_wall(r, c)

    def is_exit(self, r, c):
        return (r, c) == self.end_pos
