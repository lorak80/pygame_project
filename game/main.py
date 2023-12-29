import pygame
import Bob, Killer, Floor, Text, Sky
import time

#ticks of the clock per second (also known as fps)
FPS = 60
#width and height in pixels of the images
WIN_WIDTH, WIN_HEIGHT = 640, 480
BOB_SURF_WIDTH, BOB_SURF_HEIGHT = 30, 30
SPIKE_SIZE = 32
#rectangles sizes
BOB_RECT_WIDTH, BOB_RECT_HEIGHT = 30, 30
#absolute position x and y of the floor
FLOOR_POSX, FLOOR_POSY = 0, 352
#font size of texts
FONT_SIZE_SCORE = 25
#gravities
GRAVITY = 0.62
STRONG_GRAVITY = GRAVITY * 2
#max amount of spikes
MAX_SPIKES =  int(FLOOR_POSY / SPIKE_SIZE) * 2
#image strings
BOB_IMG_LEFT, BOB_IMG_RIGHT = "images/guyLeft.png", "images/guyRight.png"
SPIKE_IMG_LEFT, SPIKE_IMG_RIGHT = "images/spikeLeft.png", "images/spikeRight.png"

def blit_spikes(screen, spikes, n_spikes):
    for i in range(n_spikes):
        screen.blit(spikes[i].surf, spikes[i].rect)

def blit_non_killer(screen, bob, floor, sky, text0):
    screen.blit(floor.surf, floor.rect)
    screen.blit(sky.surf, sky.rect)
    screen.blit(text0.surf, text0.rect)
    if bob.moving_right():
        screen.blit(pygame.image.load(BOB_IMG_RIGHT).convert_alpha(), bob.rect)
    else:
        screen.blit(bob.surf, bob.rect)
        

def check_spike_collision(bob, spikes, n_spikes):
    for i in range(n_spikes):
        if bob.rect.colliderect(spikes[i]):
                spikes[i].kill(bob)

def main():
    pygame.init()
    pygame.display.set_caption("bob")
    score_text = Text.Score("Score: 0.0", "black", FONT_SIZE_SCORE, (0, 0))
    score_text.rect.left = 0
    score_text.set_score("Score: 0.1", "black")
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    sky = Sky.Sky()
    floor = Floor.Floor()
    bob = Bob.Bob(WIN_WIDTH / 2, FLOOR_POSY)#bob is the player
    spikes = [Killer.Spike(0, i * SPIKE_SIZE, SPIKE_IMG_RIGHT) for i in range(int(MAX_SPIKES / 2))]
    spikes.extend([Killer.Spike(WIN_WIDTH, i * SPIKE_SIZE, SPIKE_IMG_LEFT) for i in range(int(MAX_SPIKES / 2))])
    speed_y = Bob.INIT_JUMP_SPEED
    dash_stop_time = -1
    while True:
        blit_non_killer(screen, bob, floor, sky, score_text) 
        blit_spikes(screen, spikes, MAX_SPIKES)
        current_time = time.time()
        pygame.display.update()

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        if bob.dashing() and not bob.dashed():
            if dash_stop_time == -1:
                dash_stop_time = current_time + Bob.DASH_TIME
            elif dash_stop_time > current_time:
                bob.dash()
            else:
                speed_y = 0 - GRAVITY
                bob.jump(speed_y)
                bob.states["dashing"] = False
                dash_stop_time = -1
                bob.states["dashed"] = True
        else:
            bob.movement(keys)
            if keys[pygame.K_SPACE] and bob.rect.bottom <= FLOOR_POSY:
                bob.jump(speed_y)
                speed_y -= GRAVITY
            elif not keys[pygame.K_SPACE] and bob.rect.bottom < FLOOR_POSY:
                speed_y -= STRONG_GRAVITY
                bob.jump(speed_y)
            else:
                speed_y = Bob.INIT_JUMP_SPEED
                bob.rect.bottom = FLOOR_POSY
        if bob.on_ground():
            bob.states["dashed"] = False
        check_spike_collision(bob, spikes, MAX_SPIKES)

        bob.avoid_offscreen()

        clock.tick(FPS)
     
if __name__=="__main__":
    main()
    