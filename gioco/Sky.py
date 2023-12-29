import pygame

class Sky(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
        self.surf = pygame.image.load("images/sky.webp").convert()
        self.rect = self.surf.get_rect(topleft = (self.x, self.y))