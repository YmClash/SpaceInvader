import pygame
import random
from train import generate_startfield

# initialisation de Pygame

pygame.init()

# Creation de la fenetre de jeu
screen = pygame.display.set_mode((800, 600))

# titre   et  Icon
pygame.display.set_caption("SpaceShuttle")
icon = pygame.image.load('shuttle.png')
pygame.display.set_icon(icon)

# Creation   du  background
background = pygame.image.load('Background/background3.jpg')

#  Creation  de  Joueur
playerImg = pygame.image.load('ship.png')
playerX = 370
playerY = 550
playerX_change = 0

# creation du projectile
bulletImg = pygame.image.load('Bubble_Explo/bubble_explo1.png')
bullet_speed = 1
bulletY_change = -bullet_speed
bullets = []


# Creation d'enemie pour  cela  on cree une liste d'enemie
enemies = []
for i in range(10):
    enemyImg = pygame.image.load('Astro Collection/Asteroid-A-09-000.png')
    enemyX = random.randint(0, 800)
    enemyY = random.randint(50, 150)
    enemyX_change = 0.3
    enemyY_change = 20
    enemies.append([enemyX, enemyY, enemyX_change, enemyY_change])


def player_shoot():
    player_bulletX = playerX +20
    player_bulletY = playerY
    bullets.append([player_bulletX, player_bulletY])


def check_collison():
    global bullets
    new_bullets = []
    for bullet in bullets:
        bullet_rect = pygame.Rect(bullet[0],bullet[1],bulletImg.get_width(),bulletImg.get_height())
        remove_bullet = False
        for enemy in enemies:
            enemy_rect = pygame.Rect(enemy[0],enemy[1],enemyImg.get_width(),enemyImg.get_height())
            if bullet_rect.colliderect(enemy_rect):
                enemies.remove(enemy)
                remove_bullet = True
                break
            if not remove_bullet:
                new_bullets.append(bullet)
    bullets = new_bullets

# fonction  qui  affice   le  joueur a l'ecran
def player(x, y):
    screen.blit(playerImg, (x, y))

 # Fonction qui affice les  Ememie  a   l'ecran

def enemy(x, y):

    screen.blit(enemyImg, (x, y))

# Fenetre de  Jeu  Game Loop

running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background,(0,0))
    generate_startfield(screen, 200)

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

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player_shoot()
            print("shoot")

    for bullet in bullets:
        bullet[1] += bulletY_change
        screen.blit(bulletImg, (bullet[0], bullet[1]))

    check_collison()


# Controleur  de  Joeueur  Player control
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

# Mouvement  de l'enemie
    for enemy in enemies:
        enemy[0] += enemyX_change
        if enemy[0] <= 0 or enemy[0] >= 736:
            enemyX_change = -enemyX_change
            enemy[1] += enemyX_change
    for enemy in enemies:
        screen.blit(enemyImg, (enemy[0], enemy[1]))

    # enemyX += enemyX_change

    # if enemyX <= 0:
    #     enemyX_change = 0.3
    #     enemyY_change +=enemyY_change
    # elif enemyX >= 736:
    #     enemyX_change = -0.3
    #     enemyY += enemyY_change




    player(playerX,playerY)
    player_shoot()
    pygame.display.update()


pygame.quit()