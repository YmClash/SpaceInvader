import pygame
from constants import *
from dame import Jeu



pygame.init()

FENETRE = pygame.display.set_mode((TAILLE_FENETRE, TAILLE_FENETRE))
pygame.display.set_caption("Jeu de Dame by YmC")

def obtenir_posion_souris():
    x,y = pygame.mouse.get_pos()
    ligne = y // TAILLE_CASE
    colonne = x // TAILLE_CASE
    return ligne, colonne



def main():
    jeu = Jeu()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                ligne, colonne = obtenir_posion_souris()
                jeu.selectionner(ligne, colonne)

        jeu.actualiser(FENETRE)

    pygame.quit()

if __name__ == "__main__":
    main()