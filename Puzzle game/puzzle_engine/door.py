import pygame

class Door:
    def __init__(self, position, open_frames, closed_img, tile_size):
        self.position = position
        self.is_open = False
        self.timer = 0.0
        self.open_duration_after_animation = 4.0  # seconds
        self.open_frames = open_frames
        self.closed_img = closed_img
        self.tile_size = tile_size
        self.frame_index = 0
        self.frame_time = 0
        self.frame_duration = 0.3  # seconds per frame
        self.animation_finished = False

    def open(self):
        self.is_open = True
        self.timer = 0
        self.frame_index = 0
        self.frame_time = 0
        self.animation_finished = False

    def update(self, dt):
        if self.is_open:
            if not self.animation_finished:
                self.frame_time += dt
                if self.frame_time >= self.frame_duration:
                    self.frame_time -= self.frame_duration
                    if self.frame_index < len(self.open_frames) - 1:
                        self.frame_index += 1
                    else:
                        self.animation_finished = True
                        self.timer = self.open_duration_after_animation
            else:
                self.timer -= dt
                if self.timer <= 0:
                    self.is_open = False

    def draw(self, screen):
        x, y = self.position
        rect = pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
        if self.is_open:
            screen.blit(self.open_frames[self.frame_index], rect.topleft)
        else:
            screen.blit(self.closed_img, rect.topleft)

    def draw_at(self, screen, pixel_pos):
        xpix, ypix = pixel_pos
        if self.is_open:
            frame = self.open_frames[self.frame_index]
            screen.blit(frame, (xpix, ypix))
        else:
            screen.blit(self.closed_img, (xpix, ypix))
