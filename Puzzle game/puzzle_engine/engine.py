import pygame
from puzzle_engine.map_generator import MazeGenerator
from puzzle_engine.entity_manager import EntityManager
from puzzle_engine.player import Player

TILE_SIZE = 32
MAZE_WIDTH = 21
MAZE_HEIGHT = 21

class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((MAZE_WIDTH * TILE_SIZE, MAZE_HEIGHT * TILE_SIZE))
        pygame.display.set_caption("Puzzle Game")

        self.maze_gen = MazeGenerator(MAZE_WIDTH, MAZE_HEIGHT)
        self.maze_gen.generate()
        self.grid = self.maze_gen.get_grid()
        start, _ = self.maze_gen.get_start_end()

        self.entity_mgr = EntityManager(self.grid)
        self.player = Player(start)

        self.images = {
            0: pygame.image.load("assets/path.png"),
            1: pygame.image.load("assets/wall.png"),
            2: pygame.image.load("assets/switch.png"),
            3: pygame.image.load("assets/door.png"),
            4: pygame.image.load("assets/obstacle.png"),
            5: pygame.image.load("assets/path.png"),
            6: pygame.image.load("assets/flag.png"),
        }

        self.running = True
        self.result = None

    def draw_grid(self):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                tile = 0 if cell in (5, 6) else cell
                if cell == 3 and self.entity_mgr.is_door_open():
                    tile = 0  # show path if door is open
                self.screen.blit(self.images[tile], (x * TILE_SIZE, y * TILE_SIZE))

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            self.screen.fill((0, 0, 0))
            self.draw_grid()
            self.player.draw(self.screen)

            pygame.display.flip()
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    dx, dy = 0, 0
                    if event.key == pygame.K_UP:
                        dy = -1
                    elif event.key == pygame.K_DOWN:
                        dy = 1
                    elif event.key == pygame.K_LEFT:
                        dx = -1
                    elif event.key == pygame.K_RIGHT:
                        dx = 1

                    if dx != 0 or dy != 0:
                        result = self.player.move(dx, dy, self.grid, self.entity_mgr)
                        if result == "goal":
                            print("🎉 You reached the end!")
                            self.running = False
                        elif result == "obstacle":
                            print("💥 You hit an obstacle. Game Over.")
                            self.running = False
                        elif result == "switch":
                            print("🔓 Switch pressed. Door opened!")
