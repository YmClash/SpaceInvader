# Paramètres de la fenêtre
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)

# Paramètres du jeu
FPS = 50  # Vitesse du jeu
INITIAL_SNAKE_LENGTH = 3  # Longueur initiale du serpent

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


# Paramètres de l'IA
INPUT_SIZE = 24  # 8 directions * 3 informations par direction
HIDDEN_SIZE = 16  # Taille des couches cachées
OUTPUT_SIZE = 4   # 4 directions possibles (haut, bas, gauche, droite)

# Paramètres de l'algorithme génétique
POPULATION_SIZE = 2000
MUTATION_RATE = 0.1
ELITE_SIZE = 20   # Nombre de meilleurs serpents à conserver

# Paramètres d'apprentissage
MAX_STEPS_WITHOUT_FOOD = 100  # Nombre maximum de pas sans manger
FITNESS_FOOD_MULTIPLIER = 10  # Multiplicateur de score pour la nourriture
FITNESS_LIFETIME_MULTIPLIER = 0.1  # Multiplicateur pour la durée de vie
