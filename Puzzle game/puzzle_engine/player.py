import pygame
import os

class Player:
    def __init__(
        self, 
        position, 
        sprite_tile_width, 
        sprite_tile_height, 
        assets_folder, 
        maze_tile_width, 
        maze_tile_height, 
        rows=1, 
        cols=1
    ):
        self.position = position  # (x, y)
        self.state = 'walk'
        self.frame_index = 0

        self.sprite_tile_width = sprite_tile_width
        self.sprite_tile_height = sprite_tile_height
        self.maze_tile_width = maze_tile_width
        self.maze_tile_height = maze_tile_height

        self.assets_folder = assets_folder
        self.rows = rows
        self.cols = cols

        self.frames = {}
        self.load_animations()

    def load_animations(self):
        path = os.path.join(self.assets_folder, "player_walk.png")
        if os.path.exists(path):
            sheet = pygame.image.load(path).convert_alpha()
            self.frames['walk'] = self.slice_sheet(sheet)
        else:
            self.frames['walk'] = []

    def crop_transparent(self, surface):
        mask = pygame.mask.from_surface(surface)
        if mask.count() == 0:
            return surface
        rect = mask.get_bounding_rects()[0]
        cropped_surf = surface.subsurface(rect)
        return cropped_surf

    def slice_sheet(self, sheet):
        frames = []
        for row in range(self.rows):
            for col in range(self.cols):
                rect = pygame.Rect(
                    col * self.sprite_tile_width,
                    row * self.sprite_tile_height,
                    self.sprite_tile_width,
                    self.sprite_tile_height
                )
                frame = sheet.subsurface(rect)
                frame = self.crop_transparent(frame)
                frames.append(frame)
        return frames

    def move(self, dx, dy, maze, doors):
        x, y = self.position
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze):
            if maze[ny][nx] != 0:
                return False
            for door in doors:
                if (nx, ny) == door.position and not door.is_open:
                    return False
            self.position = (nx, ny)
            self.advance_frame()
            return True
        return False

    def advance_frame(self):
        frames = self.frames[self.state]
        if frames:
            self.frame_index = (self.frame_index + 1) % len(frames)

    def draw(self, screen):
        x, y = self.position
        xpix = x * self.maze_tile_width
        ypix = y * self.maze_tile_height
        frames = self.frames[self.state]
        if frames:
            frame = frames[self.frame_index]
            original_width, original_height = frame.get_size()
            scale_w = self.maze_tile_width / original_width
            scale_h = self.maze_tile_height / original_height
            scale = min(scale_w, scale_h)
            new_width = int(original_width * scale)
            new_height = int(original_height * scale)
            frame_scaled = pygame.transform.smoothscale(frame, (new_width, new_height))
            offset_x = (self.maze_tile_width - new_width) // 2
            offset_y = (self.maze_tile_height - new_height) // 2
            screen.blit(frame_scaled, (xpix + offset_x, ypix + offset_y))

    def draw_at(self, screen, pixel_pos):
        xpix, ypix = pixel_pos
        frames = self.frames[self.state]
        if frames:
            frame = frames[self.frame_index]
            original_width, original_height = frame.get_size()
            scale_w = self.maze_tile_width / original_width
            scale_h = self.maze_tile_height / original_height
            scale = min(scale_w, scale_h)
            new_width = int(original_width * scale)
            new_height = int(original_height * scale)
            frame_scaled = pygame.transform.smoothscale(frame, (new_width, new_height))
            offset_x = (self.maze_tile_width - new_width) // 2
            offset_y = (self.maze_tile_height - new_height) // 2
            screen.blit(frame_scaled, (xpix + offset_x, ypix + offset_y))
