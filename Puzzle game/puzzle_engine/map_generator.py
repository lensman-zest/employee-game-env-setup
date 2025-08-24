# Puzzle game/puzzle_engine/map_generator.py

import random

class MazeGenerator:
    def __init__(self, width, height):
        self.width = width if width % 2 == 1 else width + 1
        self.height = height if height % 2 == 1 else height + 1
        self.grid = [[1 for _ in range(self.width)] for _ in range(self.height)]

    def generate(self):
        self._carve_path(1, 1)
        return self.grid

    def _carve_path(self, x, y):
        self.grid[y][x] = 0
        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 1 <= nx < self.width - 1 and 1 <= ny < self.height - 1:
                if self.grid[ny][nx] == 1:
                    self.grid[y + dy // 2][x + dx // 2] = 0
                    self._carve_path(nx, ny)

    def place_interactives(self, start, end):
        """
        Places switches, doors, and obstacles in the maze, returns their positions.
        Returns a dictionary:
        {
            "switches": [(x, y)],
            "doors": [(x, y)],
            "obstacles": [(x, y)]
        }
        """
        interactives = {
            "switches": [],
            "doors": [],
            "obstacles": []
        }

        # Place one switch-door pair
        while True:
            x, y = random.randint(1, self.width - 2), random.randint(1, self.height - 2)
            if self.grid[y][x] == 0 and (x, y) != start and (x + 1, y) != end:
                if self.grid[y][x + 1] == 0:
                    interactives["switches"].append((x, y))
                    interactives["doors"].append((x + 1, y))
                    break

        # Place two obstacles
        count = 0
        while count < 2:
            x, y = random.randint(1, self.width - 2), random.randint(1, self.height - 2)
            if self.grid[y][x] == 0 and (x, y) not in interactives["switches"] \
               and (x, y) not in interactives["doors"] and (x, y) != start and (x, y) != end:
                interactives["obstacles"].append((x, y))
                count += 1

        return interactives
