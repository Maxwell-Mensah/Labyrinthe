
import time

class Solver:
    def __init__(self, maze):
        self.maze = maze
        self.visited = set()
        self.path_stack = []

    def solve_generator(self, start_pos):
        """
        Yields moves to solve the maze.
        Each yield is a direction tuple (dr, dc) to move the turtle.
        """
        self.visited = set()
        self.path_stack = [start_pos]
        self.visited.add(start_pos)
        
        # We start recursion from the current position
        # Using an iterative stack or generator for DFS to be "pausable"
        
        # Helper generator for recursive DFS
        yield from self._dfs(start_pos[0], start_pos[1])

    def _dfs(self, r, c):
        if self.maze.is_exit(r, c):
            return True

        # Directions: Up, Right, Down, Left
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if not self.maze.is_wall(nr, nc) and (nr, nc) not in self.visited:
                self.visited.add((nr, nc))
                
                # Move Forward
                yield (dr, dc)
                
                if (yield from self._dfs(nr, nc)):
                    return True
                
                # Backtrack
                yield (-dr, -dc)
        
        return False
