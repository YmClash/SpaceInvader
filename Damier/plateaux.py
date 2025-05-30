import pygame
from constants import *
from pieces import Piece


class Plateau:
    def __init__(self):
        self.plateau = []
        self.piece_selectionnee = None
        self.initialiser_plateau()

    def initialiser_plateau(self):
        self.plateau = [[None for _ in range(8)] for _ in range(8)]
        self.placer_pieces()

    def placer_pieces(self):
        for ligne in range(8):
            for colonne in range(8):
                if ligne < 3 and (ligne + colonne) % 2 == 1:
                    self.plateau[ligne][colonne] = Piece(ligne, colonne, NOIR)
                elif ligne > 4 and (ligne + colonne) % 2 == 1:
                    # if mode_jeu == "1v1":
                    #     self.plateau[ligne][colonne] = Piece(ligne, colonne, RANDOM_COLORS_1)
                    self.plateau[ligne][colonne] = Piece(ligne, colonne,  BLANC)
                    # self.plateau[ligne][colonne] = Piece(ligne, colonne, RANDOM_COLORS_1)

    def dessiner(self, fenetre):
        self.dessiner_cases(fenetre)
        self.dessiner_pieces(fenetre)

    def dessiner_cases(self, fenetre):
        fenetre.fill(BEIGE)
        for ligne in range(8):
            for colonne in range(8):
                if (ligne + colonne) % 2 == 0:
                    pygame.draw.rect(fenetre, MARRON,
                                  (colonne * TAILLE_CASE, ligne * TAILLE_CASE,
                                   TAILLE_CASE, TAILLE_CASE))

    def dessiner_pieces(self, fenetre):
        # print("dessiner_pieces")
        for ligne in range(8):
            for colonne in range(8):
                piece = self.plateau[ligne][colonne]
                if piece:
                    piece.dessiner(fenetre)

    def get_piece(self, ligne, colonne):
        return self.plateau[ligne][colonne]

    def deplacer(self, piece, ligne, colonne):
        self.plateau[piece.ligne][piece.colonne] = None
        self.plateau[ligne][colonne] = piece
        piece.ligne = ligne
        piece.colonne = colonne
        piece.calculer_position()

        if ligne == 0 and piece.couleur == BLANC:
            piece.faire_dame()
        elif ligne == 7 and piece.couleur == NOIR:
            piece.faire_dame()

    def supprimer_piece(self, piece):
        self.plateau[piece.ligne][piece.colonne] = None

#
# class Plateau:
#     def __init__(self):
#         self.plateau = []
#         self.piece_selectionnee = None
#         self.initialiser_plateau()
#
#     def initialiser_plateau(self):
#         self.plateau = [[None for _ in range(8)] for _ in range(8)]
#         self.placer_pieces()
#
#     def placer_pieces(self):
#         for ligne in range(8):
#             for colonne in range(8):
#                 if ligne < 3 and (ligne + colonne) % 2 == 1:
#                     self.plateau[ligne][colonne] = Piece(ligne, colonne, NOIR)
#                 elif ligne > 4 and (ligne + colonne) % 2 == 1:
#                     self.plateau[ligne][colonne] = Piece(ligne, colonne, BLANC)
#
#     def dessiner(self, fenetre):
#         self.dessiner_cases(fenetre)
#         self.dessiner_pieces(fenetre)
#
#     def dessiner_cases(self,fenetre):
#         fenetre.fill(BEIGE)
#         for ligne in range(8):
#             for colonne in range(8):
#                 if (ligne + colonne) % 2 == 0:
#                     pygame.draw.rect(fenetre,MARRON, (colonne * TAILLE_CASE, ligne * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE))
#
#
#     def dessiner_pieces(self, fenetre):
#         for ligne in range(8):
#             for colonne in range(8):
#                 piece = self.plateau[ligne][colonne]
#                 if piece:
#                     piece.dessiner(fenetre)
#
#
#     def get_piece(self, ligne, colonne):
#         return self.plateau[ligne][colonne]
#
#     def deplacer(self, piece, ligne,colonne):
#         self.plateau[piece.ligne][piece.colonne] = None
#         self .plateau[ligne][colonne] = piece
#         piece.ligne = ligne
#         piece.colonne = colonne
#         piece.calculer_position()
#
#         if ligne == 0 and piece.couleur == BLANC:
#             print("Dame ! pour les Blancs ")
#             piece.faire_dame()
#         elif ligne == 7 and piece.couleur == NOIR:
#             print("Dame ! pour les Noirs ")
#             piece.faire_dame()
#
#     def supprimer_piece(self,piece):
#         print("Suppression de la pièce :", piece)
#         self.plateau[piece.ligne][piece.colonne] = None
#
