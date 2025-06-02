import pygame
import random
from .constants import *


class Food:
    def __init__(self):
        self.position = self._get_random_position()

    def _get_random_position(self):
        """Génère une position aléatoire pour la nourriture"""
        x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        return pygame.Vector2(x, y)

    def draw(self, screen):
        """Dessine la nourriture à l'écran"""
        pygame.draw.rect(screen, RED, pygame.Rect(
            self.position.x, self.position.y,
            GRID_SIZE, GRID_SIZE))

    def respawn(self, snake_positions):
        """Réapparaît à une nouvelle position, en évitant le serpent"""
        while True:
            new_pos = self._get_random_position()
            if pygame.Vector2(new_pos.x, new_pos.y) not in snake_positions:
                self.position = new_pos
                break
