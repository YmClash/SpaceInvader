# Constantes


import random

TAILLE_FENETRE = 800
TAILLE_CASE = TAILLE_FENETRE // 8




ROUGE = (255, 0, 0)
MARRON = (139, 69, 19)

BEIGE = (245, 222, 179)

DOM =  [random.randint(0, 255) for i in range(3)]


RANDOM_COLORS_1 = [random.randint(0, 255) for i in range(3)]
RANDOM_COLORS_2 = DOM
RANDOM_COLORS_3 = [random.randint(0, 255) for i in range(3)]

NOIR = [0, 0, 0]
# NOIR = RANDOM_COLORS_3

BLANC = (255, 255, 255)
# BLANC = RANDOM_COLORS_1  # Utilisation de la couleur aléatoire pour le blanc




VERT = (0, 255, 0)
BLEU = (0, 0, 255)
GRIS = (128, 128, 128)

# Police et texte
TAILLE_POLICE = 32
TAILLE_POLICE_SCORE = 32

# Points
POINTS_CAPTURE = 1
POINTS_DAME = 2




MESSAGE_ATTENTE = "En attente d'un adversaire..."
MESSAGE_ERREUR_CONNEXION = "Erreur de connexion"
MESSAGE_CONNEXION_PERDUE = "Connexion perdue avec l'adversaire"

MESSAGE_SERVEUR_PRET = "Serveur prêt - En attente d'un joueur..."
MESSAGE_CONNEXION_REUSSIE = "Connexion établie ! La partie va commencer..."
MESSAGE_IP_SERVEUR = "Adresse IP du serveur : {}"

# Délais
DELAI_AFFICHAGE_MESSAGE = 2  # secondes
DELAI_ATTENTE_CONNEXION = 60  # secondes





# États de jeu en ligne
MODE_HOTE = "HOTE"
MODE_CLIENT = "CLIENT"

