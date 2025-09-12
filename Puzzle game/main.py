import pygame
import sys
import random
import os
from collections import deque

from config import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, COLOR_WALL, COLOR_PATH, MAZE_WIDTH, MAZE_HEIGHT
from puzzle_engine.map_generator import ComplexMazeGenerator
from puzzle_engine.player import Player

def draw_maze(screen, maze_grid, start, end, flag_img):
    for y, row in enumerate(maze_grid):
        for x, tile in enumerate(row):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            color = COLOR_PATH if tile == 0 else COLOR_WALL
            pygame.draw.rect(screen, color, rect)
            if (x, y) == start:
                pygame.draw.circle(screen, (0, 100, 0), rect.center, TILE_SIZE // 3)
            elif (x, y) == end:
                screen.blit(flag_img, rect.topleft)

def draw_obstacles(screen, obstacles):
    for pos, img in obstacles:
        x, y = pos
        rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        screen.blit(img, rect.topleft)

def find_shortest_path(grid, start, end):
    visited = set()
    queue = deque([(start, [start])])
    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == end:
            return set(path)
        visited.add((x, y))
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
                if grid[ny][nx] == 0 and (nx, ny) not in visited:
                    queue.append(((nx, ny), path + [(nx, ny)]))
    return set()

def is_junction(grid, x, y):
    open_neighbors = sum(
        grid[y + dy][x + dx] == 0
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]
        if 0 <= x + dx < len(grid[0]) and 0 <= y + dy < len(grid)
    )
    return open_neighbors >= 3

def get_obstacle_candidates(grid, exclude, min_candidates=5):
    candidates = [
        (x, y)
        for y, row in enumerate(grid)
        for x, cell in enumerate(row)
        if cell == 0 and (x, y) not in exclude and is_junction(grid, x, y)
    ]
    if len(candidates) < min_candidates:
        candidates += [
            (x, y)
            for y, row in enumerate(grid)
            for x, cell in enumerate(row)
            if cell == 0
            and (x, y) not in exclude
            and sum(
                grid[y + dy][x + dx] == 0
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]
                if 0 <= x + dx < len(grid[0]) and 0 <= y + dy < len(grid)
            )
            == 1
        ]
    return candidates

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Maze Echo Puzzle")

    # Load assets
    flag_path = os.path.join(os.path.dirname(__file__), "assets", "flag.png")
    flag_img = pygame.image.load(flag_path).convert_alpha()
    flag_img = pygame.transform.scale(flag_img, (TILE_SIZE, TILE_SIZE))

    obstacle_filenames = ["obstacle1.png", "obstacle2.png", "obstacle3.png"]
    obstacle_images = []
    for filename in obstacle_filenames:
        path = os.path.join(os.path.dirname(__file__), "assets", filename)
        img = pygame.image.load(path).convert_alpha()
        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        obstacle_images.append(img)

    generator = ComplexMazeGenerator(MAZE_WIDTH, MAZE_HEIGHT)
    maze = generator.generate()
    start = (1, 1)
    end = generator.find_farthest_point(start)

    solution_path = find_shortest_path(maze, start, end)
    exclude_positions = solution_path.union({start, end})
    obstacle_candidates = get_obstacle_candidates(maze, exclude_positions)
    num_obstacles = random.randint(3, min(8, len(obstacle_candidates)))
    sampled_positions = random.sample(obstacle_candidates, num_obstacles)
    obstacles = [(pos, random.choice(obstacle_images)) for pos in sampled_positions]

    player = Player(
        start,
        64,  # sprite frame width
        64,  # sprite frame height
        os.path.join(os.path.dirname(__file__), "assets"),
        TILE_SIZE,
        TILE_SIZE,
        rows=1,
        cols=8
    )

    clock = pygame.time.Clock()
    running = True

    while running:
        dt = clock.tick(60) / 1000.0
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                moved = False
                if event.key == pygame.K_UP:
                    moved = player.move(0, -1, maze)
                elif event.key == pygame.K_DOWN:
                    moved = player.move(0, 1, maze)
                elif event.key == pygame.K_LEFT:
                    moved = player.move(-1, 0, maze)
                elif event.key == pygame.K_RIGHT:
                    moved = player.move(1, 0, maze)

        draw_maze(screen, maze, start, end, flag_img)
        draw_obstacles(screen, obstacles)
        player.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
