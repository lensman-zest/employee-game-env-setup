class EntityManager:
    def __init__(self, maze_grid):
        self.switches = []
        self.doors = []
        self.obstacles = []
        self.end = None

        for y, row in enumerate(maze_grid):
            for x, cell in enumerate(row):
                if cell == 2:
                    self.switches.append((x, y))
                elif cell == 3:
                    self.doors.append((x, y))
                elif cell == 4:
                    self.obstacles.append((x, y))
                elif cell == 6:
                    self.end = (x, y)

        self.door_open = False

    def trigger_switch(self):
        self.door_open = True

    def is_door_open(self):
        return self.door_open
