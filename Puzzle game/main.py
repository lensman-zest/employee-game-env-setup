import pygame
import sys
import random
import os
from collections import deque
import math

from config import TILE_SIZE, MAZE_WIDTH, MAZE_HEIGHT
from puzzle_engine.map_generator import ComplexMazeGenerator
from puzzle_engine.player import Player
from puzzle_engine.door import Door
from puzzle_engine.switch import Switch

VIEWPORT_WIDTH = 15
VIEWPORT_HEIGHT = 11
VISIBILITY_RADIUS = 6  # tiles visible around player

SCREEN_WIDTH = TILE_SIZE * VIEWPORT_WIDTH
SCREEN_HEIGHT = TILE_SIZE * VIEWPORT_HEIGHT

COLOR_PATH = (220, 220, 220)
COLOR_WALL = (30, 30, 30)


def draw_viewport_maze(screen, maze_grid, start, end, flag_img, offset_x, offset_y, player_pos):
    px, py = player_pos
    for y in range(VIEWPORT_HEIGHT):
        for x in range(VIEWPORT_WIDTH):
            mx = x + offset_x
            my = y + offset_y
            if 0 <= mx < len(maze_grid[0]) and 0 <= my < len(maze_grid):
                dist = math.sqrt((mx - px) ** 2 + (my - py) ** 2)
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if dist <= VISIBILITY_RADIUS:
                    tile = maze_grid[my][mx]
                    color = COLOR_PATH if tile == 0 else COLOR_WALL
                    pygame.draw.rect(screen, color, rect)
                    if (mx, my) == start:
                        pygame.draw.circle(screen, (0, 100, 0), rect.center, TILE_SIZE // 3)
                    elif (mx, my) == end:
                        screen.blit(flag_img, rect.topleft)
                else:
                    pygame.draw.rect(screen, (0, 0, 0), rect)


def draw_viewport_obstacles(screen, obstacles, offset_x, offset_y, player_pos):
    px, py = player_pos
    for pos, img in obstacles:
        x, y = pos
        vx = x - offset_x
        vy = y - offset_y
        if 0 <= vx < VIEWPORT_WIDTH and 0 <= vy < VIEWPORT_HEIGHT:
            dist = math.sqrt((x - px) ** 2 + (y - py) ** 2)
            if dist <= VISIBILITY_RADIUS:
                rect = pygame.Rect(vx * TILE_SIZE, vy * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                screen.blit(img, rect.topleft)


def draw_viewport_entity(screen, entity, offset_x, offset_y, player_pos):
    x, y = entity.position
    px, py = player_pos
    dist = math.sqrt((x - px) ** 2 + (y - py) ** 2)
    if dist <= VISIBILITY_RADIUS:
        vx = x - offset_x
        vy = y - offset_y
        if 0 <= vx < VIEWPORT_WIDTH and 0 <= vy < VIEWPORT_HEIGHT:
            pos = (vx * TILE_SIZE, vy * TILE_SIZE)
            entity.draw_at(screen, pos)


def draw_minimap(screen, maze_grid, player_pos, door_positions, switch_positions, goal_pos):
    minimap_tile_size = 6
    minimap_width = len(maze_grid[0]) * minimap_tile_size
    minimap_height = len(maze_grid) * minimap_tile_size
    margin = 10

    minimap_x = SCREEN_WIDTH - minimap_width - margin
    minimap_y = margin

    for y, row in enumerate(maze_grid):
        for x, tile in enumerate(row):
            rect = pygame.Rect(minimap_x + x * minimap_tile_size, minimap_y + y * minimap_tile_size,
                               minimap_tile_size, minimap_tile_size)
            color = COLOR_PATH if tile == 0 else COLOR_WALL
            pygame.draw.rect(screen, color, rect)

    door_color = (0, 0, 150)
    for pos in door_positions:
        x, y = pos
        rect = pygame.Rect(minimap_x + x * minimap_tile_size, minimap_y + y * minimap_tile_size,
                           minimap_tile_size, minimap_tile_size)
        pygame.draw.rect(screen, door_color, rect)

    switch_color = (0, 150, 0)
    for pos in switch_positions:
        x, y = pos
        rect = pygame.Rect(minimap_x + x * minimap_tile_size, minimap_y + y * minimap_tile_size,
                           minimap_tile_size, minimap_tile_size)
        pygame.draw.rect(screen, switch_color, rect)

    px, py = player_pos
    player_rect = pygame.Rect(minimap_x + px * minimap_tile_size, minimap_y + py * minimap_tile_size,
                              minimap_tile_size, minimap_tile_size)
    pygame.draw.rect(screen, (200, 0, 0), player_rect)

    # Draw goal/destination on minimap in bright red
    gx, gy = goal_pos
    goal_rect = pygame.Rect(minimap_x + gx * minimap_tile_size, minimap_y + gy * minimap_tile_size,
                            minimap_tile_size, minimap_tile_size)
    pygame.draw.rect(screen, (255, 0, 0), goal_rect)


def find_shortest_path(grid, start, end):
    visited = set()
    queue = deque([(start, [start])])
    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == end:
            return path
        visited.add((x, y))
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid):
                if grid[ny][nx] == 0 and (nx, ny) not in visited:
                    queue.append(((nx, ny), path + [(nx, ny)]))
    return []


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


def slice_sprite_sheet(sheet, frame_width, frame_height, num_frames):
    frames = []
    for i in range(num_frames):
        rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
        frame_image = sheet.subsurface(rect)
        frames.append(pygame.transform.scale(frame_image, (TILE_SIZE, TILE_SIZE)))
    return frames


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Maze Echo Puzzle")

    base_path = os.path.dirname(__file__)
    asset_path = os.path.join(base_path, "assets")

    flag_img = pygame.image.load(os.path.join(asset_path, "flag.png")).convert_alpha()
    flag_img = pygame.transform.scale(flag_img, (TILE_SIZE, TILE_SIZE))

    close_door_img = pygame.image.load(os.path.join(asset_path, "close_door.png")).convert_alpha()
    close_door_img = pygame.transform.scale(close_door_img, (TILE_SIZE, TILE_SIZE))

    door_open_sheet = pygame.image.load(os.path.join(asset_path, "door_open.png")).convert_alpha()
    open_door_frames = slice_sprite_sheet(door_open_sheet, 64, 64, 11)

    red_switch_img = pygame.image.load(os.path.join(asset_path, "red_switch.png")).convert_alpha()
    red_switch_img = pygame.transform.scale(red_switch_img, (TILE_SIZE, TILE_SIZE))

    green_switch_img = pygame.image.load(os.path.join(asset_path, "green_switch.png")).convert_alpha()
    green_switch_img = pygame.transform.scale(green_switch_img, (TILE_SIZE, TILE_SIZE))

    obstacle_filenames = ["obstacle1.png", "obstacle2.png", "obstacle3.png"]
    obstacle_images = []
    for filename in obstacle_filenames:
        img = pygame.image.load(os.path.join(asset_path, filename)).convert_alpha()
        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        obstacle_images.append(img)

    generator = ComplexMazeGenerator(MAZE_WIDTH, MAZE_HEIGHT)
    maze = generator.generate()
    start = (1, 1)
    end = generator.find_farthest_point(start)

    path = find_shortest_path(maze, start, end)
    solution_set = set(path)
    exclude_positions = solution_set.union({start, end})
    obstacle_candidates = [pos for pos in get_obstacle_candidates(maze, exclude_positions) if pos not in [start, end]]
    num_obstacles = random.randint(3, min(8, len(obstacle_candidates)))
    sampled_positions = random.sample(obstacle_candidates, num_obstacles)
    obstacles = [(pos, random.choice(obstacle_images)) for pos in sampled_positions]

    player = Player(
        start,
        64,
        64,
        asset_path,
        TILE_SIZE,
        TILE_SIZE,
        rows=1,
        cols=8
    )

    possible_door_indices = [i for i in range(1, len(path) - 1)]
    door_index = random.choice(possible_door_indices)
    door_pos = path[door_index]

    possible_switch_indices = list(range(1, door_index)) if door_index > 1 else [1]
    switch_index = random.choice(possible_switch_indices)
    switch_pos = path[switch_index]

    doors = [Door(door_pos, open_door_frames, close_door_img, TILE_SIZE)]
    switches = [Switch(switch_pos, red_switch_img, green_switch_img, TILE_SIZE, doors[0])]

    clock = pygame.time.Clock()
    running = True

    while running:
        dt = clock.tick(60) / 1000.0
        screen.fill((0, 0, 0))

        offset_x = max(0, min(player.position[0] - VIEWPORT_WIDTH // 2, MAZE_WIDTH - VIEWPORT_WIDTH))
        offset_y = max(0, min(player.position[1] - VIEWPORT_HEIGHT // 2, MAZE_HEIGHT - VIEWPORT_HEIGHT))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                moved = False
                if event.key == pygame.K_UP:
                    moved = player.move(0, -1, maze, doors)
                elif event.key == pygame.K_DOWN:
                    moved = player.move(0, 1, maze, doors)
                elif event.key == pygame.K_LEFT:
                    moved = player.move(-1, 0, maze, doors)
                elif event.key == pygame.K_RIGHT:
                    moved = player.move(1, 0, maze, doors)
                elif event.key == pygame.K_SPACE:
                    px, py = player.position
                    for switch in switches:
                        if (px, py) == switch.position:
                            switch.press()

        px, py = player.position
        for switch in switches:
            if (px, py) == switch.position:
                switch.press()

        for door in doors:
            door.update(dt)
        for switch in switches:
            switch.update()

        draw_viewport_maze(screen, maze, start, end, flag_img, offset_x, offset_y, player.position)
        draw_viewport_obstacles(screen, obstacles, offset_x, offset_y, player.position)
        for door in doors:
            draw_viewport_entity(screen, door, offset_x, offset_y, player.position)
        for switch in switches:
            draw_viewport_entity(screen, switch, offset_x, offset_y, player.position)
        draw_viewport_entity(screen, player, offset_x, offset_y, player.position)

        door_positions = [door.position for door in doors]
        switch_positions = [switch.position for switch in switches]
        draw_minimap(screen, maze, player.position, door_positions, switch_positions, end)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
