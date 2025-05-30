# Constantes


import random

TAILLE_FENETRE = 800
TAILLE_CASE = TAILLE_FENETRE // 8
NOIR = [0, 0, 0]

ROUGE = (255, 0, 0)
MARRON = (139, 69, 19)

BEIGE = (245, 222, 179)


RANDOM_COLORS_1 = [random.randint(0, 255) for i in range(3)]
RANDOM_COLORS_2 = [random.randint(0, 255) for i in range(3)]

# BLANC = (255, 255, 255)
BLANC = RANDOM_COLORS_1  # Utilisation de la couleur aléatoire pour le blanc


