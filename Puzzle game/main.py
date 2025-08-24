import pygame
import sys
import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, COLOR_WALL, COLOR_PATH, MAZE_WIDTH, MAZE_HEIGHT
from puzzle_engine.map_generator import MazeGenerator

def draw_maze(screen, maze_grid):
    for y, row in enumerate(maze_grid):
        for x, tile in enumerate(row):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            color = COLOR_PATH if tile == 0 else COLOR_WALL
            pygame.draw.rect(screen, color, rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Maze Puzzle")

    # Generate maze
    generator = MazeGenerator(MAZE_WIDTH, MAZE_HEIGHT)
    maze = generator.generate()

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill((0, 0, 0))  # Clear screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_maze(screen, maze)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
