import pygame

SKY_IMG = "images/sky.jfif"

class Sky(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
        self.surf = pygame.image.load(SKY_IMG).convert()
        self.rect = self.surf.get_rect(topleft = (self.x, self.y))