import pygame
import Bob

class Killer(pygame.sprite.Sprite):
    def __init__(self, init_x, init_y):
        super().__init__()
        self.init_x = init_x
        self.init_y = init_y
    def kill(self, bob: Bob):
        bob.reset_pos()

class Spike(Killer):
    def __init__(self, init_x, init_y, image):
        super().__init__(init_x, init_y)
        self.surf = pygame.image.load(image).convert_alpha()
        self.rect = self.surf.get_rect(midtop = (self.init_x, self.init_y))