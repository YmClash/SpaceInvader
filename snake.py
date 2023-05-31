import pygame
import time
import random
from train import generate_startfield

pygame.init()

hauteur = 800
largeur = 600

surface = pygame.display.set_mode((hauteur, largeur))

# le  joueur
ship = pygame.image.load('player3.png').convert()
ship_x = 370
ship_y = 550
ship_x_change = 0
ship_y_change = 0

# food

food_img = pygame.image.load('player3.png').convert()
food_x = random.randint(1, 800)
food_Y = random.randint(1, 600)
food_x_change = random.randint(1, 800)
food_Y_change = random.randint(1, 600)


def player() :
    surface.blit(ship, (ship_x, ship_y))


def foody(x, y) :
    surface.blit(food_img, (x, y))



ship_direction = None

vitesse = 0.1
running = True

while running :
    surface.fill((23, 22, 22))
    # generate_startfield(surface, 2000)

    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            running = False

        if event.type == pygame.KEYDOWN :

            if event.key == pygame.K_UP and ship_direction != "down":
                ship_direction = "up"

            if event.key == pygame.K_DOWN and ship_direction != "up":
                ship_direction = "down"

            if event.key == pygame.K_LEFT and ship_direction!= "right":
                ship_direction = "left"

            if event.key == pygame.K_RIGHT and ship_direction!= "left":
                ship_direction = "right"


    if ship_direction == "up":
        ship_y -= vitesse
    elif ship_direction == "down":
        ship_y += vitesse
    elif ship_direction == "left":
        ship_x -= vitesse
    elif ship_direction == "right":
        ship_x += vitesse

            # if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN :
            #     ship_x_change = 0
            #     ship_y_change = 0

    # generate_startfield(surface,20)
    # ship_x -= ship_x_change
    #
    # if ship_x <= 0:
    #     ship_x = 0
    # elif ship_x >=800:
    #     ship_x = 800

    player()
    foody(food_x, food_Y)

    pygame.display.flip()
    pygame.display.update()

pygame.quit()
