import pygame
import random

pygame.init()

HAUTEUR = 500
LARGEUR = 500
TUILLE = 50
FPS = 60


NOIR = (0, 0, 0)
ROUGE = (250, 47, 47)
BLEU = (66, 135, 245)
VERT = (47, 250, 148)
ROSE = (250, 47, 203)

dt  = 0


screen = pygame.display.set_mode((HAUTEUR, LARGEUR))
clock = pygame.time.Clock
pygame.display.set_caption("Momo")
player= pygame.image.load("alien.png")
joueur_pos = pygame.Vector2(screen.get_width() / random.randint(1,5),screen.get_height() / random.randint(1,5))

rect = pygame.Rect(screen.get_width()/3,screen.get_width()/3 ,50,50)

running = True

while running :



    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            running = False

        screen.fill(VERT)

        for i in range(10):
            pygame.draw.circle(screen,ROSE,joueur_pos,10)

        pygame.draw.rect(screen,NOIR,rect)



        pygame.display.update()

pygame.quit()
