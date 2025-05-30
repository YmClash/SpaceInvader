import pygame
from constants import *
from plateaux import Plateau
from ia import IA
import time


class Jeu:
    def __init__(self,mode_jeu='1V1'):
        self.plateau = Plateau()
        self.tour = NOIR
        self.piece_selectionnee = None
        self.mouvements_valides = []
        self.mode_jeu = mode_jeu
        self.ia = IA(self,BLANC) if mode_jeu == '1VCPU' else None
        self.dernier_mouvement = time.time()


    def actualiser(self, fenetre):
        self.plateau.dessiner(fenetre)
        self.dessiner_mouvements_valides(fenetre)
        pygame.display.update()

        #delay pour IA
        temps_actuel = time.time()
        if self.mode_jeu == '1VCPU' and self.tour == BLANC and temps_actuel - self.dernier_mouvement > 0.5:
            self.jouer_tour_ia()
            self.dernier_mouvement = temps_actuel


    def dessiner_mouvements_valides(self, fenetre):
        if self.piece_selectionnee:
            self.mouvements_valides = self.obtenir_mouvements_valides(self.piece_selectionnee)
            for mouvenent in self.mouvements_valides:
                ligne,colonne = mouvenent
                x = colonne * TAILLE_CASE + TAILLE_CASE // 2
                y = ligne * TAILLE_CASE + TAILLE_CASE // 2
                pygame.draw.circle(fenetre,ROUGE,(x,y),15)



    def jouer_tour_ia(self):
        mouvement = self.ia.obtenir_mouvement()
        if mouvement:
            ligne_depart, colonne_depart, ligne_arrivee, colonne_arrivee = mouvement
            piece = self.plateau.get_piece(ligne_depart, colonne_depart)
            if piece:
                self.piece_selectionnee = piece
                self._deplacer(ligne_arrivee, colonne_arrivee)
                self.piece_selectionnee = None

    def obtenir_mouvements_valides(self, piece):
        mouvements = []

        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            nouveau_ligne = piece.ligne + dy
            nouveau_colonne = piece.colonne + dx

            if 0 <= nouveau_ligne < 8 and 0 <= nouveau_colonne < 8:
                if not self.plateau.get_piece(nouveau_ligne, nouveau_colonne):
                    if (piece.couleur == NOIR and dy > 0) or (piece.couleur == BLANC and dy < 0) or piece.est_dame:
                        mouvements.append((nouveau_ligne, nouveau_colonne))

                elif self.plateau.get_piece(nouveau_ligne, nouveau_colonne).couleur != piece.couleur:
                    saut_ligne = nouveau_ligne + dy
                    saut_colonne = nouveau_colonne + dx
                    if 0 <= saut_ligne < 8 and 0 <= saut_colonne < 8:
                        if not self.plateau.get_piece(saut_ligne, saut_colonne):
                            mouvements.append((saut_ligne, saut_colonne))

        return mouvements



    def selectionner(self, ligne, colonne):
        if self.piece_selectionnee:
            resultat = self._deplacer(ligne, colonne)
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
            self.tour = BLANC
            print("Tour des Blancs")
            # self.tour = RANDOM_COLORS_1 if self.mode_jeu == '1VCPU' else BLANC
            self.dernier_mouvement = time.time()
        else:
            self.tour = NOIR
            print("Tour des Noirs")
