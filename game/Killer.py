import pygame, random
import main

SPIKE_SPEEDS = [2, 2.5, 3]
MIN_RESP_TIME = 60 * 2
MAX_RESP_TIME = 60 * 4

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
    
    def is_offscreen(self):
        offscreen = False
        if self.RIGHT:
            if self.rect.left >= main.WIN_WIDTH:
                offscreen = True
        else:
            if self.rect.right <= 0:
                offscreen = True

        return offscreen

    def reset_pos(self):
        if self.RIGHT:
            self.rect.left = random.randint(-MAX_RESP_TIME, -MIN_RESP_TIME)
        else:
            self.rect.right = random.randint(main.WIN_WIDTH + MIN_RESP_TIME, main.WIN_WIDTH + MAX_RESP_TIME)
        