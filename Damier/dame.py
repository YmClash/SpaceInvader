import pygame
from constants import *
from plateaux import Plateau


class Jeu:
    def __init__(self):
        self.plateau = Plateau()
        self.tour = NOIR
        self.piece_selectionnee = None
        self.mouvements_valide = []

    def actualiser(self,fenetre):
        self.plateau.dessiner(fenetre)
        pygame.display.update()

    def selectionner(self,ligne,colonne):
        if self.piece_selectionnee:
            resultat = self._deplace(ligne, colonne)
            if not resultat:
                self.piece_selectionnee = None
                self.selectionner(ligne, colonne)

        piece = self.plateau.get_piece(ligne, colonne)
        if piece and piece.couleur == self.tour:
            self.piece_selectionnee = piece
            return True

        return False

    def _deplacer(self, ligne, colonne):
        piece = self.plateau.get_piece(ligne, colonne)
        if not piece and (ligne + colonne) % 2 == 1:
            if abs(ligne - self.piece_selectionnee.ligne) == 2:
                ligne_milieu = (ligne + self.piece_selectionnee.ligne) // 2
                colonne_milieu = (colonne + self.piece_selectionnee.colonne) // 2
                piece_milieu = self.plateau.get_piece(ligne_milieu, colonne_milieu)
                if piece_milieu and piece_milieu.couleur != self.tour:
                    self.plateau.supprimer_piece(piece_milieu)
                    self.plateau.deplacer(self.piece_selectionnee, ligne, colonne)
                    self.changer_tour()
                    return True
            elif abs(ligne - self.piece_selectionnee.ligne) == 1:
                self.plateau.deplacer(self.piece_selectionnee, ligne, colonne)
                self.changer_tour()
                return True
        return False

    def changer_tour(self):
        if self.tour == NOIR:
            print("Tour des Blancs")
            self.tour = BLANC
        else:
            print("Tour des Noirs")
            self.tour = NOIR