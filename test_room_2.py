import pygame

# Initialisation de Pygame
pygame.init()

# Définir les dimensions de la fenêtre
largeur = 800
hauteur = 600

# Créer une fenêtre
fenetre = pygame.display.set_mode((largeur, hauteur))

# Position initiale du joueur
joueur_x = 100
joueur_y = 100

# Vitesse de déplacement du joueur
vitesse = 1

# Boucle principale du jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Récupérer les touches enfoncées
    touches = pygame.key.get_pressed()

    # Mouvement horizontal
    if touches[pygame.K_LEFT]:
        joueur_x -= vitesse
    if touches[pygame.K_RIGHT]:
        joueur_x += vitesse

    # Mouvement vertical
    if touches[pygame.K_UP]:
        joueur_y -= vitesse
    if touches[pygame.K_DOWN]:
        joueur_y += vitesse

    # Vérifier les limites de l'écran
    if joueur_x < 0:
        joueur_x = 0
    elif joueur_x > largeur:
        joueur_x = largeur
    if joueur_y < 0:
        joueur_y = 0
    elif joueur_y > hauteur:
        joueur_y = hauteur

    # Effacer l'écran
    fenetre.fill((0, 0, 0))  # Noir

    # Dessiner le joueur
    pygame.draw.rect(fenetre, (255, 0, 0), (joueur_x, joueur_y, 20, 20))

    # Mettre à jour l'affichage
    pygame.display.flip()

# Quitter Pygame
pygame.quit()