
from collections import deque


class Maze:
    def __init__(self, filename=None, grid=None, start_pos=None, end_pos=None):
        self.filename = filename
        self.grid = []
        self.start_pos = None
        self.end_pos = None

        if grid is not None:
            self.grid = grid
            self.start_pos = start_pos
            self.end_pos = end_pos
        elif filename:
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

    def shortest_path(self, start, end):
        """BFS to find shortest path from start to end. Returns list of (r,c) positions."""
        if start == end:
            return [start]
        visited = {start}
        queue = deque([(start, [start])])
        while queue:
            (r, c), path = queue.popleft()
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if not self.is_wall(nr, nc) and (nr, nc) not in visited:
                    new_path = path + [(nr, nc)]
                    if (nr, nc) == end:
                        return new_path
                    visited.add((nr, nc))
                    queue.append(((nr, nc), new_path))
        return []  # No path found
