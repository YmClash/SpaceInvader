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


Point = namedtuple('point','x,y')

#COLOR

BLACK = (0,0,0)
WHITE = (225,250,250)
RED = (232, 26, 26)
GREEN =(15, 250, 2)
BLAU = (7, 92, 240)
RANDOM_COLOR = (random.randint(0,250),random.randint(0,250),random.randint(0,250))

#Parameter

BLOCK_SIZE = 20
SPEED = 20

class SnakeGame:

    def __init__(self,WIDTH=650,HEIGHT =500):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.screen = pygame.display.set_mode((self.WIDTH,self.HEIGHT))
        pygame.display.set_caption("SnakeAI by YmC")
        self.clock = pygame.time.Clock

        #init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.WIDTH /2 ,self.HEIGHT / 2)
        self.snake = [self.head,
                      Point(self.head.x-BLOCK_SIZE,self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE),self.head.y)]

        self.score = 0
        self.food = None
        self.place_food()

    def place_food(self):
        x = random.randint(0, (self.WIDTH-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0, (self.HEIGHT-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = Point(x,x)
        if self.food in self.snake:
            self.place_food()


    def play_step(self):
        for event in pygame.event.get():
            if event.type == pygame.quit():
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN
        # 2. Move

        self.move(self.direction)
        self.snake.insert(0,self.head)

        # 3 . check game over
        game_over = False
        if self.is_collision():
            game_over = True
            return  game_over,self.score

        # 4 place food
        if self.head == self.food:
            self.score += 1
            self.place_food()
        else:
            self.snake.pop()

        # 5 Update UI & Score
        self.update_ui()
        self.clock.tick(SPEED)
        # 6
        return game_over,self.score



    def is_collision(self):
        # hit Boundary
        if self.head.x > self.WIDTH - BLOCK_SIZE or self.head.x < 0 or self.head.y >self.HEIGHT - BLOCK_SIZE or self.head.y < 0 :
            return True
        #hit ifself
        if self.head in self.snake[1:]:
            return True

        return False

    def update_ui(self):
        self.screen.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.screen,BLAU,pygame.Rect(pt.x,pt.y ,BLOCK_SIZE,BLOCK_SIZE))
            pygame.draw.rect(self.screen,GREEN,pygame.Rect(pt.x,pt.y ,12,12))

        pygame.draw.rect(self.screen,RED, pygame.Rect(self.food.x,self.food.y, BLOCK_SIZE,BLOCK_SIZE))

        text = font.render("Score : " + str(self.score), True,WHITE)
        self.screen.blit(text,[0,0])
        pygame.display.flip()


    def move(self,direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x,y)

if __name__ == '__main__':
    game = SnakeGame()


    while True:
        game_over,score = game.play_step()

        if game_over == True:
            break

    print(f'Score Final : {score}')

    pygame.quit()
















