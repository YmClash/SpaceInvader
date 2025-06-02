import pygame
from .constants import *
from .food import Food


class Snake:
    def __init__(self):
        # Position initiale au centre
        self.head = pygame.Vector2(GRID_WIDTH // 2 * GRID_SIZE,
                                   GRID_HEIGHT // 2 * GRID_SIZE)
        # Corps initial
        self.body = [
            pygame.Vector2(self.head.x, self.head.y + GRID_SIZE),
            pygame.Vector2(self.head.x, self.head.y + 2 * GRID_SIZE)
        ]
        self.direction = pygame.Vector2(0, -GRID_SIZE)
        self.food = Food()
        self.score = 0
        self.is_dead = False
        self.moves_without_food = 0  # Compteur de mouvements sans nourriture

    def update(self):
        """Met à jour la position du serpent"""
        if self.is_dead:
            return

        # Mettre à jour le corps
        self.body.insert(0, pygame.Vector2(self.head))

        # Déplacer la tête
        self.head += self.direction

        # Vérifier si on mange la nourriture
        if self.head == self.food.position:
            self.score += 1
            self.food.respawn(self.get_positions())
            self.moves_without_food = 0  # Réinitialiser le compteur
        else:
            self.body.pop()
            self.moves_without_food += 1  # Incrémenter le compteur

        # Vérifier la mort
        if self._check_collision():
            self.is_dead = True

    def _check_collision(self):
        """Vérifie les collisions avec les murs et le corps"""
        # Collision avec les murs
        if (self.head.x < 0 or self.head.x >= WINDOW_WIDTH or
                self.head.y < 0 or self.head.y >= WINDOW_HEIGHT):
            return True

        # Collision avec le corps
        if pygame.Vector2(self.head) in self.body:
            return True

        return False

    def change_direction(self, new_direction):
        """Change la direction du serpent si ce n'est pas la direction opposée"""
        if self.direction.x * -1 != new_direction.x or self.direction.y * -1 != new_direction.y:
            self.direction = new_direction

    def get_positions(self):
        """Retourne toutes les positions occupées par le serpent"""
        positions = [pygame.Vector2(self.head)]
        positions.extend(self.body)
        return positions

    def draw(self, screen):
        """Dessine le serpent et la nourriture"""
        # Dessiner la tête
        pygame.draw.rect(screen, GREEN,
                         pygame.Rect(self.head.x, self.head.y, GRID_SIZE, GRID_SIZE))

        # Dessiner le corps
        for segment in self.body:
            pygame.draw.rect(screen, DARK_GREEN,
                             pygame.Rect(segment.x, segment.y, GRID_SIZE, GRID_SIZE))

        # Dessiner la nourriture
        self.food.draw(screen)
