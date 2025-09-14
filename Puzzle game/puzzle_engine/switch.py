import pygame

class Switch:
    def __init__(self, position, red_img, green_img, tile_size, linked_door):
        self.position = position
        self.is_pressed = False
        self.red_img = red_img
        self.green_img = green_img
        self.tile_size = tile_size
        self.linked_door = linked_door

    def press(self):
        self.is_pressed = True
        self.linked_door.open()

    def update(self):
        self.is_pressed = self.linked_door.is_open

    def draw(self, screen):
        x, y = self.position
        scale = 0.6
        img = self.green_img if self.is_pressed else self.red_img
        img_width = int(self.tile_size * scale)
        img_height = int(self.tile_size * scale)
        offset_x = (self.tile_size - img_width) // 2
        offset_y = (self.tile_size - img_height) // 2
        img_scaled = pygame.transform.smoothscale(img, (img_width, img_height))
        rect = pygame.Rect(x * self.tile_size + offset_x, y * self.tile_size + offset_y, img_width, img_height)
        screen.blit(img_scaled, rect.topleft)

    def draw_at(self, screen, pixel_pos):
        xpix, ypix = pixel_pos
        scale = 0.6
        img = self.green_img if self.is_pressed else self.red_img
        img_width = int(self.tile_size * scale)
        img_height = int(self.tile_size * scale)
        offset_x = (self.tile_size - img_width) // 2
        offset_y = (self.tile_size - img_height) // 2
        img_scaled = pygame.transform.smoothscale(img, (img_width, img_height))
        screen.blit(img_scaled, (xpix + offset_x, ypix + offset_y))
