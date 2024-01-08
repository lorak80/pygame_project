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

#                                            SPIKES
#       Spikes are the hardest killer to avoid, they randomly come from the left and right side
#                               of the screen in controlled random order

import pygame
import Bob, Killer, Floor, Text, Sky
import time

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
BOB_IMG_LEFT, BOB_IMG_RIGHT = ["images/bobLeft.png", "images/bobLeft1.png", "images/bobLeft2.png"], ["images/bobRight.png", "images/bobRight1.png", "images/bobRight2.png"]
SPIKE_IMG_LEFT, SPIKE_IMG_RIGHT = "images/spikeLeft.png", "images/spikeRight.png"
LOGO_IMG = "images/logo.png"
#background music
BG_MUSIC = "music/bgm.mp3"
#death sfx (to be implemented)
DEATH_SFX = "sfx/death.mp3"

MUSIC_DURATION = 225 #in seconds

#blits all the spikes
def blit_spikes(screen, spikes):
    for spike in spikes:
        screen.blit(spike.surf, spike.rect)

#blits everything that doesn't kill
def blit_non_killer(screen, bob, floor, sky, text0, text1, current_frame):
    screen.blit(floor.surf, floor.rect)
    screen.blit(sky.surf, sky.rect)
    screen.blit(text0.surf, text0.rect)
    screen.blit(text1.surf, text1.rect)
    #based on the moving direction of bob, it turns its body towards that direction
    if bob.facing_right():
        screen.blit(bob.surf_to_blitR(current_frame), bob.rect)
    else:
        screen.blit(bob.surf_to_blitL(current_frame), bob.rect)
        
#function that checks spike collisions and resets values if the collision occurred
def spike_collision(bob, spikes, score_text):
    for spike in spikes:
        if bob.rect.colliderect(spike):
            spike.kill(bob, spikes, score_text)
            return True
    return False
#function that moves spikes in their direction, also resets a spike's position when offscreen
def move_spikes(spikes):
    for spike in spikes:
        spike.move()
        if spike.is_offscreen():
            spike.reset_pos()

def main():
    pygame.init()
    pygame.display.set_caption("bob")
    pygame.display.set_icon(pygame.image.load(LOGO_IMG))
    #creation of all the objects
    score_text = Text.Score("Score: 0.00", "white", FONT_SIZE_SCORE, ORIGIN)
    score_text.rect.left = 0
    highscore_text = Text.Score("Highscore: 0.00", "white", FONT_SIZE_SCORE, (WIN_WIDTH / 2, 0))
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))#sets the resolution of the screen
    clock = pygame.time.Clock()#clock used to set fps
    sky = Sky.Sky()
    floor = Floor.Floor()
    bob = Bob.Bob(WIN_WIDTH / 2, FLOOR_POSY)#bob is the player
    #"spikes" is the list of all spike instances
    spikes = [Killer.Spike(-20, i * SPIKE_SIZE, SPIKE_IMG_RIGHT, True) for i in range(HALF_SPIKES)]
    #adds to the list the spikes on the right side of the screen
    spikes.extend([Killer.Spike(WIN_WIDTH + 20, i * SPIKE_SIZE, SPIKE_IMG_LEFT, False) for i in range(HALF_SPIKES)])
    #vertical speed used when jumping
    speed_y = Bob.INIT_JUMP_SPEED
    #dash_stop_time is used to measure how long the dash has been going on for
    dash_stop_time = -1

    highscore = -1

    #gets the current time, which is the time in seconds 
    #since the epoch (1st january 1970 00:00:00 UTC)
    start_time = time.time()
    #counter of frames to check which frame the game is on right now
    #used to control the animation of bob
    current_frame = 1
    music = pygame.mixer_music
    music.load(BG_MUSIC)
    music.set_volume(0.12)
    music.play()
    music_stop_time = start_time + MUSIC_DURATION

    #game loop
    while True:
        blit_non_killer(screen, bob, floor, sky, score_text, highscore_text, current_frame) 
        blit_spikes(screen, spikes)
        current_time = time.time()
        pygame.display.update()

        keys = pygame.key.get_pressed()
        #this loop checks the quit event, in which case the window closes and the program stops
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if bob.dashing() and not bob.dashed():
            if dash_stop_time == -1:#if there is no stop time (bob has just started to dash)
                dash_stop_time = current_time + Bob.DASH_TIME #get the stop time
            elif dash_stop_time >= current_time:
                bob.dash()
            else: #when the dash is over
                speed_y = 0 - GRAVITY #set a negative speed value
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

        move_spikes(spikes)

        if spike_collision(bob, spikes, score_text):
            #sets new high score if curr_score > high score
            if current_time - start_time > highscore:
                highscore = current_time - start_time
                highscore_text.set_highscore(highscore)
            start_time = time.time()
        score_text.set_score(current_time - start_time)
        #avoid bob going too far left/right
        bob.avoid_offscreen()
        #tick at 60 fps
        clock.tick(FPS)
        #increases/resets frame counter
        if current_frame >= FPS:
            current_frame = 1
        else:
            current_frame += 1
        if music_stop_time <= current_time:
            music_stop_time += MUSIC_DURATION
            music.rewind()

     
if __name__=="__main__":
    main()
    