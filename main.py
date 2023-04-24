
import pygame
import random
# initialisation de Pygame

pygame.init()

# Creation de la fenetre de jeu

screen = pygame.display.set_mode((800, 600))

# titre   et  Icon
pygame.display.set_caption("SpaceShuttle")
icon = pygame.image.load('shuttle.png')
pygame.display.set_icon(icon)

# Creation   du  background

background = pygame.image.load('background3.jpg')


#  Creation  de  Joueur

playerImg = pygame.image.load('ship.png')
playerX = 370
playerY = 550
playerX_change = 0


# Creation d'enemie

enemyImg = pygame.image.load('alien.png')
enemyX = random.randint(0, 800)
enemyY = random.randint(50, 150)
enemyX_change = 0.3
enemyY_change = 20


# fonction  qui  affice   le  joueur a l'ecran
def player(x, y):

    screen.blit(playerImg, (x, y))

 # Fonction qui affice les  Ememie  a   l'ecran

def enemy(x, y):

    screen.blit(enemyImg, (x, y))

# Fenetre de  Jeu  Game Loop

running = True
while running:

    # RGB  -  Red , Green, Blue
    screen.fill((0, 0, 0))
    #  BackGrounds
    screen.blit(background,(0,0))
   ##


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # demande  quel touche est enfoncé  Droite / Gauche
        if event.type == pygame.KEYDOWN:
            print(" Bas enfoncé ")
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
                print("Gauche/Left")
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
                print("Droite/Right")
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
                print(" la touche a ete relaché")


# Controleur  de  Joeueur  Player control
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

# Mouvement  de l'enemie

    enemyX += enemyX_change

    if enemyX <= 0:
        enemyX_change = 0.3
        enemyY_change +=enemyY_change
    elif enemyX >= 736:
        enemyX_change = -0.3
        enemyY += enemyY_change




    player(playerX,playerY)
    enemy(enemyX, enemyY)
    pygame.display.update()
