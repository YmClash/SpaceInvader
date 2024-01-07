import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.Font(r'C:\Users\y_mc\PycharmProjects\SpaceInvader\Snake_Ai\arial.ttf', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

# Colors
BLACK = (0, 0, 0)
WHITE = (225, 250, 250)
RED = (232, 26, 26)
GREEN = (15, 250, 2)
BLUE = (7, 92, 240)

# Parameters
BLOCK_SIZE = 20
SPEED = 5

class SnakeGame:
    def __init__(self, width=650, height=500):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("SnakeAI by YmC")
        self.clock = pygame.time.Clock()

        # Init game state
        self.direction = Direction.RIGHT
        self.head = Point(self.width // 2, self.height // 2)
        self.snake = [self.head,
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)]
        self.score = 0
        self.food = None
        self._place_food()

    def _place_food(self):
        x = random.randint(0, (self.width - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.height - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                self._change_direction(event.key)

        self._move()
        self.snake.insert(0, self.head)

        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score

        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()

        self._update_ui()
        self.clock.tick(SPEED)
        return game_over, self.score

    def _change_direction(self, key):
        if key == pygame.K_LEFT and self.direction != Direction.RIGHT:
            self.direction = Direction.LEFT
        elif key == pygame.K_RIGHT and self.direction != Direction.LEFT:
            self.direction = Direction.RIGHT
        elif key == pygame.K_UP and self.direction != Direction.DOWN:
            self.direction = Direction.UP
        elif key == pygame.K_DOWN and self.direction != Direction.UP:
            self.direction = Direction.DOWN

    def _is_collision(self):
        if self.head.x > self.width - BLOCK_SIZE or self.head.x < 0 or \
           self.head.y > self.height - BLOCK_SIZE or self.head.y < 0:
            return True
        if self.head in self.snake[1:]:
            return True
        return False

    def _update_ui(self):
        self.screen.fill(BLACK)
        for pt in self.snake:
            pygame.draw.rect(self.screen, BLUE, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.screen, GREEN, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))

        pygame.draw.rect(self.screen, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        text = font.render("Score : " + str(self.score), True, WHITE)
        self.screen.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self):
        x, y = self.head.x, self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)

if __name__ == '__main__':
    game = SnakeGame()

    while True:
        game_over, score = game.play_step()
        if game_over:
            break

    print(f'Score Final : {score}')
    pygame.quit()
