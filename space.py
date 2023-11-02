import pygame
import random

pygame.init()

WITH = 300
HEIGHT = 300
FPS = int(60)

BLACK =(0,0,0)
GREY = (128,128,128)
YELLOW = (255,225,0)
TURQUOI = (116,214,190)

screen = pygame.display.set_mode((WITH,HEIGHT))
clock = pygame.time.Clock
background = pygame.image.load('Background/background.jpg')

running = True

while running:


    screen.fill(BLACK)
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    pygame.display.flip()




pygame.quit()

#
# if __name__=="main":
#     main()
#

