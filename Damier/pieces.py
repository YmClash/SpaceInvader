import pygame
from constants import *


class Piece:
    def __init__(self,ligne,colonne,couleur):
        self.ligne = ligne
        self.colonne = colonne
        self.couleur = couleur
        self.est_dame = False
        self.x = 0
        self.y = 0
        self.calculer_position()


    def calculer_position(self):
        self.x = TAILLE_CASE * self.colonne + TAILLE_FENETRE // 2
        self.y = TAILLE_CASE * self.ligne * TAILLE_FENETRE // 2

    def faire_dame(self):
        self.est_dame = True

    def dessiner(self, fenetre):
        rayon = TAILLE_CASE // 2 - 10
        pygame.draw.circle(fenetre,self.couleur, (self.x,self.y),rayon)
        if self.est_dame:
            pygame.draw.circle(fenetre,ROUGE, (self.x,self.y), rayon // 2)
