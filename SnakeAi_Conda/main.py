import pygame
import sys
from game.constants import *
from game.snake import Snake


def main():
    # Initialiser Pygame
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    # Créer le serpent
    snake = Snake()

    # Boucle principale du jeu
    running = True
    while running:
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction(pygame.Vector2(0, -GRID_SIZE))
                elif event.key == pygame.K_DOWN:
                    snake.change_direction(pygame.Vector2(0, GRID_SIZE))
                elif event.key == pygame.K_LEFT:
                    snake.change_direction(pygame.Vector2(-GRID_SIZE, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction(pygame.Vector2(GRID_SIZE, 0))
                elif event.key == pygame.K_r and snake.is_dead:  # Touche R pour recommencer
                    snake = Snake()

        # Mettre à jour le jeu si le serpent n'est pas mort
        if not snake.is_dead:
            snake.update()

        # Dessiner
        screen.fill(BLACK)
        snake.draw(screen)

        # Afficher le score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {snake.score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        # Afficher "Game Over" si le serpent est mort
        if snake.is_dead:
            game_over_text = font.render('Game Over! Appuyez sur R pour recommencer', True, WHITE)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
            screen.blit(game_over_text, text_rect)

        # Mettre à jour l'affichage
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()