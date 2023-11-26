import pygame
import random


pygame.init()

#Color
BLACK = (0,0,0)
WHITE = (225,250,250)
RED = (232, 26, 26)
YELLOW = (255,225,0)
GREEN =(15, 250, 2)
BLAU = (7, 92, 240)
RANDOM_COLOR = (random.randint(0,250),random.randint(0,250),random.randint(0,250))


#display initiatialisation
LARGEUR = 500
HAUTEUR = 500
FPS = 60
screen = pygame.display.set_mode((LARGEUR,HAUTEUR))
pygame.display.set_caption("YMC GameCoding Training")
clock = pygame.time.Clock

# on vas  cree un  object rectangle qui vas represanté le joueur

player = pygame.Rect(250,250,100,100)
line = pygame.Vector2()




running = True

#


while running :


    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player.y += 10
            if event.key == pygame.K_UP:
                player.y -= 10
            if event.key == pygame.K_LEFT:
                player.x -= 10
            if event.key == pygame.K_RIGHT:
                player.x += 10


    screen.fill(BLAU)
    pygame.draw.rect(screen,YELLOW,player)

    pygame.display.flip()

pygame.quit()



