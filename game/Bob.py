import pygame
from main import WIN_WIDTH, FLOOR_POSY, BOB_IMG_LEFT
from Floor import FLOOR_POSY


#movement speed
WALK_SPEED = 4
DASH_SPEED = 7
INIT_JUMP_SPEED = 12
#dash time in seconds
DASH_TIME = 0.2

class Bob(pygame.sprite.Sprite):
    def __init__(self, init_x, init_y):
        super().__init__()
        self.surf = pygame.image.load(BOB_IMG_LEFT).convert_alpha()
        self.init_x = init_x
        self.init_y = init_y
        self.states = {"mov right": False, "mov left": False, "dashing": False}
        self.rect = self.surf.get_rect(midbottom = (init_x, init_y))

    def reset_pos(self):
        self.rect.midbottom = (WIN_WIDTH / 2, FLOOR_POSY)

    def movement(self, keys):
        if keys[pygame.K_a]:
            self.rect.x -= WALK_SPEED
            self.states["mov left"] = True
            self.states["mov right"] = False
        if keys[pygame.K_d]:
            self.rect.x += WALK_SPEED
            self.states["mov right"] = True
            self.states["mov left"] = False
        if keys[pygame.K_j]:
            self.states["dashing"] = True
        else:
            self.states["dashing"] = False
 
    def jump(self, speed_y):
        self.rect.y -= speed_y

    def dash(self):
        if self.states["mov right"]:
            self.rect.x += DASH_SPEED
        if self.states["mov left"]:
            self.rect.x -= DASH_SPEED
        
    def avoid_offscreen(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= WIN_WIDTH:
            self.rect.right = WIN_WIDTH

    def moving_right(self):
        return self.states["mov right"]
    def dashing(self):
        return self.states["dashing"]