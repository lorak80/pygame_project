#                                THIS IS MY FIRST PYGAME PROJECT!

#     In this game you are Bob, Bob needs to avoid floating spikes and Glob walking around, the more
#                              time you survive, the higher the score
#                             Bob has 2 skills, jumping and dashing

# Bob jumps with spacebar, if you don't need to jump high, you simply release spacebar when needed
#                   and you will fall earlier and faster, if you hold the spacebar, 
#                            you will jump as soon as bob touches the ground.

# Bob dashes with [j] , if you dash you can't do anything else other than dashing, but you can move
#               straight in all 8 directions, horizontally, vertically and diagonally
#       Bob cannot dash more than once in the air, the dash refills when bob touches the ground

#                                            SPIKES (randomness: to be fully implemented)
#       Spikes are the hardest killer to avoid, they randomly come from the left and right side
#                               of the screen in controlled random order

#                                         GLOB ENEMY (to be fully implemented after spikes)
#     Glob is a static enemy that always moves in the same way with the same speed, combined with 
#                       the spikes, it adds more difficulty to the game

import pygame
import Bob, Killer, Floor, Text, Sky
import time, random

#ticks of the clock per second (also known as frames per second (fps))
FPS = 60
#width and height in pixels of the images
WIN_WIDTH, WIN_HEIGHT = 640, 480
BOB_SURF_WIDTH, BOB_SURF_HEIGHT = 30, 30
SPIKE_SIZE = 32 #width and height are both 32
#rectangles sizes
BOB_RECT_WIDTH, BOB_RECT_HEIGHT = 30, 30
#absolute position x and y of things
FLOOR_POSX, FLOOR_POSY = 0, 352
ORIGIN = (0, 0)
#font size of texts
FONT_SIZE_SCORE = 25
#gravities
GRAVITY = 0.56
#this stronger gravity is to get a more dynamic jump, if you release space while jumping, 
#it makes you fall earlier and faster
STRONG_GRAVITY = GRAVITY * 2.1 
#max amount of spikes
MAX_SPIKES = int(FLOOR_POSY / SPIKE_SIZE) * 2
#half amount of the max spikes
HALF_SPIKES = int(MAX_SPIKES / 2)
#bottom spikes indexes
BOTTOM_SPIKES = [10, 21]
#image strings
BOB_IMG_LEFT, BOB_IMG_RIGHT = "images/guyLeft.png", "images/guyRight.png"
SPIKE_IMG_LEFT, SPIKE_IMG_RIGHT = "images/spikeLeft.png", "images/spikeRight.png"

#blits all the spikes
def blit_spikes(screen, spikes, n_spikes):
    for i in range(n_spikes):
        screen.blit(spikes[i].surf, spikes[i].rect)

#blits everything that doesn't kill
def blit_non_killer(screen, bob, floor, sky, text0):
    screen.blit(floor.surf, floor.rect)
    screen.blit(sky.surf, sky.rect)
    screen.blit(text0.surf, text0.rect)
    #based on the moving direction of bob, it turns its body towards that direction
    if bob.facing_right():
        screen.blit(bob.surfR, bob.rect)
    else:
        screen.blit(bob.surfL, bob.rect)
        
#function that checks spike collisions, if true, kill bob and exit loop
def check_spike_collision(bob, spikes, n_spikes):
    not_killed, i = True, 0
    while i < n_spikes and not_killed:
        if bob.rect.colliderect(spikes[i]):
            spikes[i].kill(bob)
            not_killed = False
        else:
            i += 1

def randomize_spikes_to_move(spikes):
    rand_bool = [random.choice([True, False]) for _ in spikes]
    return [i for i, _ in enumerate(spikes) if rand_bool[i]]


def move_spikes(spikes, spikes_to_move):
    for i in spikes_to_move:
        spikes[i].move()
        if spikes[i].is_offscreen():
            spikes[i].reset_pos()
        

def offscreen_spikes(spikes):
    return [i for i, spike in enumerate(spikes) if spike.is_offscreen()]

def do_everything_for_spikes(spikes, spikes_to_move):
    move_spikes(spikes, spikes_to_move)
            

def main():
    pygame.init()
    pygame.display.set_caption("bob")
    score_text = Text.Score("Score: 0.0", "black", FONT_SIZE_SCORE, ORIGIN)
    score_text.set_score("Score: 0.1", "black")
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))#sets the resolution of the screen
    clock = pygame.time.Clock()#clock used to set fps
    sky = Sky.Sky()
    floor = Floor.Floor()
    bob = Bob.Bob(WIN_WIDTH / 2, FLOOR_POSY)#bob is the player
    #"spikes" is the list of all spike instances
    spikes = [Killer.Spike(-20, i * SPIKE_SIZE, SPIKE_IMG_RIGHT, True) for i in range(HALF_SPIKES)]
    #adds to the list the spike on the right side of the screen
    spikes.extend([Killer.Spike(WIN_WIDTH + 20, i * SPIKE_SIZE, SPIKE_IMG_LEFT, False) for i in range(HALF_SPIKES)])
    #used to check which spikes can move to not overwhelm the player
    spikes_to_move = randomize_spikes_to_move(spikes)
    if BOTTOM_SPIKES[0] not in spikes_to_move and BOTTOM_SPIKES[1] not in spikes_to_move:
        spikes_to_move.append(random.choice(BOTTOM_SPIKES[0], BOTTOM_SPIKES[1])) 
    print(spikes_to_move)
    #vertical speed used when jumping
    speed_y = Bob.INIT_JUMP_SPEED
    #dash_stop_time is used to measure how long the dash has been going on for
    dash_stop_time = -1
    
    #game loop
    while True:
        blit_non_killer(screen, bob, floor, sky, score_text) 
        blit_spikes(screen, spikes, MAX_SPIKES)
        #gets the current time, which is the time in seconds 
        #since the epoch (1st january 1970 00:00:00 UTC)
        current_time = time.time()
        pygame.display.update()

        keys = pygame.key.get_pressed()
        #this loop checks the quit event, in which case the window closes and the program stops
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
        do_everything_for_spikes(spikes, spikes_to_move)

        if bob.dashing() and not bob.dashed():
            if dash_stop_time == -1:#if there is no stop time (bob has just started to dash)
                dash_stop_time = current_time + Bob.DASH_TIME #get the stop time
            elif dash_stop_time >= current_time:
                bob.dash()
            else: #when the dash is over
                speed_y = 0 - GRAVITY 
                bob.jump(speed_y) #start moving downwards
                bob.states["dashing"] = False
                dash_stop_time = -1 #there is no stop time anymore
                bob.states["dashed"] = True
        else:
            bob.movement(keys)#checks WASD for moving around and dash directions
            #if you are holding space and  bob is touching the ground or floating in the air
            if keys[pygame.K_SPACE] and bob.rect.bottom <= FLOOR_POSY:
                bob.jump(speed_y)#start/continue jumping..
                speed_y -= GRAVITY#..with the default gravity
            #if you are not pressing space but you are still in the air
            elif not keys[pygame.K_SPACE] and bob.rect.bottom < FLOOR_POSY:
                #fall faster using strong gravity
                speed_y -= STRONG_GRAVITY
                bob.jump(speed_y)
            else: 
                speed_y = Bob.INIT_JUMP_SPEED
                bob.rect.bottom = FLOOR_POSY#this assignment is required to avoid bob going below ground
        if bob.on_ground():
            #bob can dash again
            bob.states["dashed"] = False

        
        check_spike_collision(bob, spikes, MAX_SPIKES)

        bob.avoid_offscreen()

        clock.tick(FPS)
     
if __name__=="__main__":
    main()
    