import random
from constants import *


class IA:
    def __init__(self, jeu, couleur):
        self.jeu = jeu
        self.couleur = couleur

    def obtenir_mouvement(self):
        pieces_disponibles = []
        for ligne in range(8):
            for colonne in range(8):
                piece = self.jeu.plateau.get_piece(ligne, colonne)
                if piece and piece.couleur == self.couleur:
                    mouvements = self.jeu.obtenir_mouvements_valides(piece)
                    if mouvements:
                        pieces_disponibles.append((piece, mouvements))

        if pieces_disponibles:
            piece, mouvements = random.choice(pieces_disponibles)
            nouvelle_pos = random.choice(mouvements)
            return piece.ligne, piece.colonne, nouvelle_pos[0], nouvelle_pos[1]
        return None
