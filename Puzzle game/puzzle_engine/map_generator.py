import random
from collections import deque

class ComplexMazeGenerator:
    def __init__(self, width, height):
        self.width = width if width % 2 == 1 else width + 1
        self.height = height if height % 2 == 1 else height + 1
        self.grid = [[1 for _ in range(self.width)] for _ in range(self.height)]

    def generate(self):
        self._prims_algorithm()
        return self.grid

    def _prims_algorithm(self):
        # Start with a grid full of walls, pick a random cell and mark as path
        start_x, start_y = 1, 1
        self.grid[start_y][start_x] = 0
        walls = []
        for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)]:
            nx, ny = start_x+dx, start_y+dy
            if 1 <= nx < self.width-1 and 1 <= ny < self.height-1:
                walls.append((nx, ny, start_x, start_y))
        while walls:
            wx, wy, px, py = walls.pop(random.randrange(len(walls)))
            if self.grid[wy][wx] == 1:
                self.grid[wy][wx] = 0
                self.grid[(wy+py)//2][(wx+px)//2] = 0
                for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)]:
                    nx, ny = wx+dx, wy+dy
                    if 1 <= nx < self.width-1 and 1 <= ny < self.height-1:
                        if self.grid[ny][nx] == 1:
                            walls.append((nx, ny, wx, wy))

    def find_farthest_point(self, start):
        """Use BFS to find farthest reachable point from start."""
        queue = deque([start])
        distances = {start: 0}
        farthest_point = start
        max_distance = 0

        while queue:
            x, y = queue.popleft()
            dist = distances[(x, y)]
            if dist > max_distance:
                max_distance = dist
                farthest_point = (x, y)
            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if self.grid[ny][nx] == 0 and (nx, ny) not in distances:
                        distances[(nx, ny)] = dist + 1
                        queue.append((nx, ny))
        return farthest_point
