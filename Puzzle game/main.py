# Puzzle game/main.py

import pygame
import sys
import random

from config import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, COLOR_WALL, COLOR_PATH, MAZE_WIDTH, MAZE_HEIGHT
from puzzle_engine.map_generator import MazeGenerator
import os

def draw_maze(screen, maze_grid, start, end, flag_img):
    for y, row in enumerate(maze_grid):
        for x, tile in enumerate(row):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            color = COLOR_PATH if tile == 0 else COLOR_WALL
            pygame.draw.rect(screen, color, rect)

            if (x, y) == start:
                pygame.draw.circle(screen, ((0,100,0)), rect.center, TILE_SIZE // 3)  # Green circle for start

            elif (x, y) == end:
                screen.blit(flag_img, rect.topleft)  # Draw flag at end position

def get_random_empty_cell(maze):
    while True:
        x = random.randint(1, MAZE_WIDTH - 2)
        y = random.randint(1, MAZE_HEIGHT - 2)
        if maze[y][x] == 0:
            return (x, y)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Maze Echo Puzzle")

    # Load flag image
    flag_path = os.path.join(os.path.dirname(__file__), "assets", "flag.png")
    flag_img = pygame.image.load(flag_path).convert_alpha()
    flag_img = pygame.transform.scale(flag_img, (TILE_SIZE, TILE_SIZE))

    # Generate maze and define start/end
    generator = MazeGenerator(MAZE_WIDTH, MAZE_HEIGHT)
    maze = generator.generate()
    start = (1, 1)
    #end = (MAZE_WIDTH - 2, MAZE_HEIGHT - 2)
    #start = get_random_empty_cell(maze)
    end = get_random_empty_cell(maze)
    while end == start:
        end = get_random_empty_cell(maze)

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill((0, 0, 0))  # Clear screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_maze(screen, maze, start, end, flag_img)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()