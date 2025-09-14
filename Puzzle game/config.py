# Puzzle game/config.py

# config.py

TILE_SIZE = 20         # Size of one tile in pixels (can be changed to make window/fov smaller or larger)
MAZE_WIDTH = 40        # Number of tiles horizontally in maze
MAZE_HEIGHT = 40       # Number of tiles vertically in maze

COLOR_PATH = (220, 220, 220)
COLOR_WALL = (30, 30, 30)
""""""
TILE_SIZE = 40
TILE_WIDTH = 45
TILE_HEIGHT = 45


MAZE_WIDTH = 25   # Must be odd
MAZE_HEIGHT = 19  # Must be odd

#SCREEN_WIDTH = TILE_SIZE * MAZE_WIDTH
#SCREEN_HEIGHT = TILE_SIZE * MAZE_HEIGHT
VIEWPORT_WIDTH = 15  # for example
VIEWPORT_HEIGHT = 11
SCREEN_WIDTH = TILE_SIZE * VIEWPORT_WIDTH
SCREEN_HEIGHT = TILE_SIZE * VIEWPORT_HEIGHT


# Colors
COLOR_WALL = (30, 30, 30)
COLOR_PATH = (220, 220, 220)

