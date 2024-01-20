import pygame

ORIGIN = (0, 0)

SKY_IMG = "images/sky.jfif"

class Sky(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load(SKY_IMG).convert()
        self.rect = self.surf.get_rect(topleft = (ORIGIN))