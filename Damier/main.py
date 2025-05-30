import pygame
from constants import *
from dame import Jeu

pygame.init()
FENETRE = pygame.display.set_mode((TAILLE_FENETRE, TAILLE_FENETRE))
pygame.display.set_caption('Jeu de Dames')




def print_game_info():

    print("Bienvenue dans le jeu de dames !")
    print("Utilisez la souris pour sélectionner une pièce et la déplacer.")
    print("Les pièces noires sont en bas, les blanches en haut.")
    print("Pour gagner, capturez toutes les pièces de l'adversaire.")
    print("Appuyez sur la croix pour quitter le jeu.")


    print("Taile de la fenêtre :", TAILLE_FENETRE)
    print("Taille de la case :", TAILLE_CASE)



def obtenir_position_souris():
    x, y = pygame.mouse.get_pos()
    ligne = y // TAILLE_CASE
    colonne = x // TAILLE_CASE
    return ligne, colonne


def main():
    jeu = Jeu()
    print_game_info()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                ligne, colonne = obtenir_position_souris()
                jeu.selectionner(ligne, colonne)

        jeu.actualiser(FENETRE)

    pygame.quit()


if __name__ == '__main__':
    main()

#
# pygame.init()
#
# FENETRE = pygame.display.set_mode((TAILLE_FENETRE, TAILLE_FENETRE))
# pygame.display.set_caption("Jeu de Dame by YmC")
#
# def obtenir_posion_souris():
#     x,y = pygame.mouse.get_pos()
#     ligne = y // TAILLE_CASE
#     colonne = x // TAILLE_CASE
#     return ligne, colonne
#
#
#
# def main():
#     jeu = Jeu()
#     running = True
#
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 ligne, colonne = obtenir_posion_souris()
#                 jeu.selectionner(ligne, colonne)
#
#         jeu.actualiser(FENETRE)
#
#     pygame.quit()
#
# if __name__ == "__main__":
#     main()