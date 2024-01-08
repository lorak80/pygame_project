import pygame
from main import WIN_WIDTH, FLOOR_POSY, BOB_IMG_LEFT, BOB_IMG_RIGHT, FPS

#movement speed
WALK_SPEED = 5
DASH_SPEED = 8
INIT_JUMP_SPEED = 12
#dash time in seconds
DASH_TIME = 0.2
#hitbox size to make the game more balanced
HITBOX_SIZE = {"width": 11, "height": 30}

class Bob(pygame.sprite.Sprite):
    def __init__(self, init_x, init_y): #initial x;y position
        super().__init__()
        #left and right image of bob, to make 
        #bob face the direction that it moving to
        #and also its frames of walking
        self.surfLArr = [pygame.image.load(BOB_IMG_LEFT[0]).convert_alpha(), \
                        pygame.image.load(BOB_IMG_LEFT[1]).convert_alpha(), \
                        pygame.image.load(BOB_IMG_LEFT[2]).convert_alpha()]
        self.surfRArr = [pygame.image.load(BOB_IMG_RIGHT[0]).convert_alpha(),\
                         pygame.image.load(BOB_IMG_RIGHT[1]).convert_alpha(),\
                         pygame.image.load(BOB_IMG_RIGHT[2]).convert_alpha()]
        self.init_x = init_x 
        self.init_y = init_y
        #possible states of bob
        self.states = {"mov right": False, "mov left": False, "mov up": False,
                       "mov down": False, "face right": False, "dashed": False,"dashing": False}
        self.rect = self.surfLArr[0].get_rect(midbottom = (init_x, init_y))
        self.deflate_hitbox()

    #resets the position to the center of the screen and on the ground
    def reset_pos(self):
        self.rect.midbottom = (WIN_WIDTH / 2, FLOOR_POSY)
    #checks which keys are being pressed and what to do in which case
    def movement(self, keys):
        if keys[pygame.K_a]:
            self.rect.x -= WALK_SPEED
            self.states["face right"] = False
            self.states["mov left"] = True
            self.states["mov right"] = False
        elif keys[pygame.K_d]:
            self.rect.x += WALK_SPEED
            self.states["face right"] = True
            self.states["mov right"] = True
            self.states["mov left"] = False
        else:
            self.states["mov right"] = False
            self.states["mov left"] = False
        if keys[pygame.K_w]:
            self.states["mov up"] = True
            self.states["mov down"] = False
        elif keys[pygame.K_s]:
            self.states["mov down"] = True
            self.states["mov up"] = False
        else:
            self.states["mov up"] = False
            self.states["mov down"] = False
        if keys[pygame.K_j]:
            self.states["dashing"] = True
        else:
            self.states["dashing"] = False
    #moves bob vertically/makes him jump
    def jump(self, speed_y):
        self.rect.y -= speed_y

    def dash(self):
        if self.states["mov right"]:
            self.rect.x += DASH_SPEED
        if self.states["mov left"]:
            self.rect.x -= DASH_SPEED
        if self.states["mov up"]:
            self.rect.y -= DASH_SPEED
        if self.states["mov down"]:
            self.rect.y += DASH_SPEED
        if self.on_ground():
            self.rect.bottom = FLOOR_POSY

    #prevents bob from going offscreen
    def avoid_offscreen(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= WIN_WIDTH:
            self.rect.right = WIN_WIDTH
    #shrinks the hitbox
    def deflate_hitbox(self):
        old_center = self.rect.center
        self.rect.width = HITBOX_SIZE["width"]
        self.rect.height = HITBOX_SIZE["height"]
        self.rect.center = old_center
    #returns the surface to blit/the current walking frame to the right
    def surf_to_blitR(self, current_frame):
        if not self.moving():
            return self.surfRArr[0]
        else:
            return self.surfRArr[current_frame % 3]
    #same thing but to the left
    def surf_to_blitL(self, current_frame):
        if not self.moving():
            return self.surfLArr[0]
        else:
            return self.surfLArr[current_frame % 3]

    #a few boolean methods to check states/positions
    def on_ground(self):
        return (self.rect.bottom >= FLOOR_POSY)
    def facing_right(self):
        return self.states["face right"]
    def dashing(self):
        return self.states["dashing"]
    def dashed(self):
        return self.states["dashed"]
    def moving(self):
        return self.states["mov left"] or self.states["mov right"]