import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np


pygame.init()

font = pygame.font.Font(r'C:\Users\y_mc\PycharmProjects\SpaceInvader\Snake_Ai\arial.ttf',25)

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
SPEED = 40

class SnakeGame:

    def __init__(self,WIDTH=650,HEIGHT =500):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.screen = pygame.display.set_mode((self.WIDTH,self.HEIGHT))
        pygame.display.set_caption("SnakeAI by YmC")
        self.clock = pygame.time.Clock
        self.reset()

        #init game state
    def reset(self):
        self.direction = Direction.RIGHT

        self.head = Point(self.WIDTH /2 ,self.HEIGHT / 2)
        self.snake = [self.head,
                      Point(self.head.x-BLOCK_SIZE,self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE),self.head.y)]

        self.score = 0
        self.food = None
        self.place_food()
        self.frame_iteration = 0

    def place_food(self):
        x = random.randint(0, (self.WIDTH-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0, (self.HEIGHT-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = Point(x,y)
        if self.food in self.snake:
            self.place_food()

    def play_step(self,action):

        #1. collect user input
        self.frame_iteration += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


        #2. move
        self.move(action) #update the head
        self.snake.insert(0,self.head)

        #3. check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward,game_over,self.score


        #4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self.place_food()
        else:
            self.snake.pop()

        #5. update ui and clock
        self.update_ui()
        self.clock.tick(SPEED)

        #6. return game over and score
        return reward,game_over,self.score

    def is_collision(self,pt=None):
        if pt is None:
            pt = self.head
        #hit boundary
        if pt.x > self.WIDTH - BLOCK_SIZE or pt.x < 0 or pt.y > self.HEIGHT - BLOCK_SIZE or pt.y < 0:
            return True

        #hit itself
        if pt in self.snake[1:]:
            return True

        return False

    def update_ui(self):
        self.screen.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.screen,GREEN,pygame.Rect(pt.x,pt.y,BLOCK_SIZE,BLOCK_SIZE))
            pygame.draw.rect(self.screen,BLACK,pygame.Rect(pt.x+4,pt.y+4,12,12))

        pygame.draw.rect(self.screen,RED,pygame.Rect(self.food.x,self.food.y,BLOCK_SIZE,BLOCK_SIZE))

        text = font.render("Score: "+str(self.score),True,WHITE)
        self.screen.blit(text,[0,0])
        pygame.display.flip()

    def move(self,action):
        # [straight,right,left]
        clock_wise = [Direction.RIGHT,Direction.DOWN,Direction.LEFT,Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action,[1,0,0]):
            new_dir = clock_wise[idx] #no change
        elif np.array_equal(action,[0,1,0]):
            next_idx = (idx + 1)%4
            new_dir = clock_wise[next_idx] #right turn r -> d -> l -> u
        else: # [0,0,1]
            next_idx = (idx - 1)%4
            new_dir = clock_wise[next_idx]

        self.direction = new_dir


        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x,y)

