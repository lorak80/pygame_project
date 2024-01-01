import pygame, random
import main

SPIKE_SPEEDS = [2.5, 3.5, 4]

class Killer(pygame.sprite.Sprite):
    def __init__(self, init_x, init_y):
        super().__init__()
        self.init_x = init_x
        self.init_y = init_y
    def kill(self, bob):
        bob.reset_pos()

class Spike(Killer):
    def __init__(self, init_x, init_y, image, right):
        super().__init__(init_x, init_y)
        self.RIGHT = right
        self.speed = random.choice(SPIKE_SPEEDS)
        self.surf = pygame.image.load(image).convert_alpha()
        self.rect = self.surf.get_rect(midtop = (self.init_x, self.init_y))
    def move(self):
        if self.RIGHT:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed
    
    def random_speed(self):
        self.speed = random.choice(SPIKE_SPEEDS)
    def reset_pos(self):
        if self.RIGHT:
            self.rect.right = 0
        else:
            self.rect.left = main.WIN_WIDTH
        