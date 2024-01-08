import pygame
import main

FLOOR_IMG = "images/floor.jfif"

class Floor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load(FLOOR_IMG).convert()
        self.rect = self.surf.get_rect(topleft = (main.FLOOR_POSX, main.FLOOR_POSY))
    