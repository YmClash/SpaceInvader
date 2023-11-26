import pygame
import random

pygame.init()

#Display size

WIDTH = 500
HEIGHT = 500
TILE_SIZE = 50


#Color

BLACK = (0,0,0)
WHITE = (225,250,250)
RED = (232, 26, 26)
GREEN =(15, 250, 2)
BLAU = (7, 92, 240)
RANDOM_COLOR = (random.randint(0,250),random.randint(0,250),random.randint(0,250))


# display initiatialisation
screen = pygame.display.set_mode((WIDTH,HEIGHT))

time = pygame.time.Clock
FPS = 60

# Create a dot  that represent the player
player_1 = pygame.Vector2(screen.get_width() / 2,screen.get_height() / 2 )

player_2 = pygame.Rect(10,10,50,50)


speed = 5

ship_direction = None

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.image.save(screen,"MOMO.png")
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_1.y -= 10
            if event.key == pygame.K_DOWN:
                player_1.y += 10
            if event.key == pygame.K_LEFT:
                player_1.x -= 10
            if event.key ==  pygame.K_RIGHT:
                player_1.x += 10

    # if player_1.x += 10 :






        # if event in pygame.key.get_pressed():
        #     if event.type. == pygame.L


    screen.fill(RANDOM_COLOR)
    pygame.draw.rect(screen,RED,player_2)
    pygame.draw.circle(screen,GREEN,player_1,20)


    pygame.display.update()


pygame.quit()




