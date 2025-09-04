import pygame

TILE_SIZE = 32

class Player:
    def __init__(self, pos):
        self.x, self.y = pos
        self.image = pygame.image.load("assets/player.png")

    def move(self, dx, dy, maze, entity_mgr):
        new_x = self.x + dx
        new_y = self.y + dy

        target = maze[new_y][new_x]

        if target == 1:
            return "wall"
        if target == 3 and not entity_mgr.is_door_open():
            return "locked_door"

        self.x, self.y = new_x, new_y

        if (self.x, self.y) in entity_mgr.switches:
            entity_mgr.trigger_switch()
            return "switch"
        elif (self.x, self.y) in entity_mgr.obstacles:
            return "obstacle"
        elif (self.x, self.y) == entity_mgr.end:
            return "goal"

        return "moved"

    def draw(self, surface):
        surface.blit(self.image, (self.x * TILE_SIZE, self.y * TILE_SIZE))
