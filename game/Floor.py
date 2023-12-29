import pygame
#topleft floor position
FLOOR_POSX = 0
FLOOR_POSY = 350

class Floor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        FLOOR_POSX = 0
        FLOOR_POSY = 350
        self.surf = pygame.image.load("images/floor.png").convert()
        self.rect = self.surf.get_rect(topleft = (FLOOR_POSX, FLOOR_POSY))
    