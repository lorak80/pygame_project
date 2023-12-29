import pygame

def main():
    pygame.init()
    pygame.display.set_caption("hello world!")
    screen = pygame.display.set_mode((640,320))
    running = True
    clock = pygame.time.Clock()
    testSurface = pygame.Surface((200, 100))
    testSurface.fill("Red")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        testSurface.blit(testSurface, (0, 0))
        pygame.display.update()
        clock.tick(60)
     
     
if __name__=="__main__":
    main()