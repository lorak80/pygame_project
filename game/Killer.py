import pygame, random
import main

SPIKE_SPEEDS = [3, 3.5, 4]
MIN_RESP_TIME = 60 * 1.5
MAX_RESP_TIME = 60 * 10
SPIKE_HITBOX_SIZE = {"width": 16, "height": 16}

class Killer(pygame.sprite.Sprite):
    def __init__(self, init_x, init_y):
        super().__init__()
        self.init_x = init_x
        self.init_y = init_y
    def kill(self, bob, spikes, score):
        bob.reset_pos()
        for spike in spikes:
            spike.reset_pos()
        score.reset()

class Spike(Killer):
    def __init__(self, init_x, init_y, image, right):
        super().__init__(init_x, init_y)
        self.RIGHT = right
        self.speed = random.choice(SPIKE_SPEEDS)
        self.surf = pygame.image.load(image).convert_alpha()
        self.rect = self.surf.get_rect(midtop = (self.init_x, self.init_y))
        self.deflate_hitbox()
        self.reset_pos()
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

    def deflate_hitbox(self):
        old_center = self.rect.center
        self.rect.width = SPIKE_HITBOX_SIZE["width"]
        self.rect.height = SPIKE_HITBOX_SIZE["height"]
        self.rect.center = old_center

    def reset_pos(self):
        if self.RIGHT:
            self.rect.left = random.randint(-MAX_RESP_TIME, -MIN_RESP_TIME)
        else:
            self.rect.right = random.randint(main.WIN_WIDTH + MIN_RESP_TIME, main.WIN_WIDTH + MAX_RESP_TIME)
        