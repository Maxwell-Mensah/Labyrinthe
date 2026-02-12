
import random
from collections import deque


class MazeGenerator:
    """Generates random mazes using recursive backtracking algorithm."""

    @staticmethod
    def generate(rows, cols, seed=None):
        """
        Generate a maze grid of given size.
        rows and cols should be odd numbers for proper wall structure.
        Returns a 2D grid (list of lists) with 1=wall, 0=passage,
        plus start_pos and end_pos.
        """
        # Ensure odd dimensions for clean maze walls
        if rows % 2 == 0:
            rows += 1
        if cols % 2 == 0:
            cols += 1

        if seed is not None:
            random.seed(seed)

        # Start with all walls
        grid = [[1 for _ in range(cols)] for _ in range(rows)]

        # Recursive backtracking from (1, 1)
        start_r, start_c = 1, 1
        grid[start_r][start_c] = 0
        stack = [(start_r, start_c)]

        while stack:
            r, c = stack[-1]
            neighbors = []
            # Check 4 directions (step of 2 to keep walls between cells)
            for dr, dc in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                nr, nc = r + dr, c + dc
                if 1 <= nr < rows - 1 and 1 <= nc < cols - 1 and grid[nr][nc] == 1:
                    neighbors.append((nr, nc, r + dr // 2, c + dc // 2))

            if neighbors:
                nr, nc, wr, wc = random.choice(neighbors)
                grid[wr][wc] = 0  # Remove wall between
                grid[nr][nc] = 0  # Carve new cell
                stack.append((nr, nc))
            else:
                stack.pop()

        # Place start and end as far apart as possible using BFS
        start_pos = (1, 1)
        end_pos = MazeGenerator._farthest_point(grid, start_pos, rows, cols)

        # If end_pos is same as start (shouldn't happen), fallback
        if end_pos == start_pos:
            end_pos = (rows - 2, cols - 2)
            grid[end_pos[0]][end_pos[1]] = 0

        return grid, start_pos, end_pos

    @staticmethod
    def _farthest_point(grid, start, rows, cols):
        """BFS to find the farthest reachable point from start."""
        visited = set()
        queue = deque([start])
        visited.add(start)
        farthest = start

        while queue:
            r, c = queue.popleft()
            farthest = (r, c)
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited and grid[nr][nc] == 0:
                    visited.add((nr, nc))
                    queue.append((nr, nc))

        return farthest

    @staticmethod
    def to_text(grid, start_pos, end_pos):
        """Convert a grid to the text format used by the game."""
        lines = []
        for r, row in enumerate(grid):
            line = ""
            for c, cell in enumerate(row):
                if (r, c) == start_pos:
                    line += "x"
                elif (r, c) == end_pos:
                    line += "X"
                elif cell == 1:
                    line += "#"
                else:
                    line += "."
            lines.append(line)
        return "\n".join(lines)

    @staticmethod
    def difficulty_settings(level):
        """Return (rows, cols) for a given difficulty level (1-based)."""
        sizes = {
            1: (9, 9),
            2: (11, 13),
            3: (15, 17),
            4: (19, 21),
            5: (21, 27),
            6: (25, 31),
            7: (29, 37),
            8: (33, 41),
            9: (37, 45),
            10: (41, 51),
        }
        # For levels beyond 10, keep growing
        if level > 10:
            base_r, base_c = 41, 51
            extra = (level - 10) * 4
            return (base_r + extra, base_c + extra)
        return sizes.get(level, (11, 13))
