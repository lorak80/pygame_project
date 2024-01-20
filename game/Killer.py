import pygame, random
import main
#list of speeds to give to random.choice
SPEEDS = [3, 3.5, 4]
#minimum and maximum respawn time
MIN_RESP_TIME = 60 * 2
MAX_RESP_TIME = 60 * 10
#new size of the spikes' hitboxes to make them more balanced and easier to avoid
HITBOX_SIZE = {"width": 16, "height": 16}

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
        self.RIGHT = right #attribute to see which way the spike is facing
        self.speed = random.choice(SPEEDS) #random initial speed
        self.surf = pygame.image.load(image).convert_alpha()
        self.rect = self.surf.get_rect(midtop = (self.init_x, self.init_y))
        self.deflate_hitbox() 
        #randomizes the spike's position at its beginning of existence
        self.reset_pos()
    #moves the spike right or left based on self.RIGHT
    def move(self):
        if self.RIGHT:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed
    #randomize speed, used when spike goes offscreen
    def random_speed(self):
        self.speed = random.choice(SPEEDS)
    #returns if the spike is offscreen or not
    def is_offscreen(self):
        offscreen = False
        if self.RIGHT:
            if self.rect.left >= main.WIN_WIDTH:
                offscreen = True
        else:
            if self.rect.right <= 0:
                offscreen = True

        return offscreen
    #shrinks the hitbox size to make the game not unplayable
    def deflate_hitbox(self):
        old_center = self.rect.center
        self.rect.width = HITBOX_SIZE["width"]
        self.rect.height = HITBOX_SIZE["height"]
        self.rect.center = old_center
    #resets position randomly offscreen, 
    #so that the spike doesn't instantly come onscreen 
    def reset_pos(self):
        if self.RIGHT:
            self.rect.left = random.randint(-MAX_RESP_TIME, -MIN_RESP_TIME)
        else:
            self.rect.right = random.randint(main.WIN_WIDTH + MIN_RESP_TIME, main.WIN_WIDTH + MAX_RESP_TIME)
        