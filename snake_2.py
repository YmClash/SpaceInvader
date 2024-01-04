import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    Up = 3
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
WIDTH = 650
HEIGHT = 500
FPS = 60

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("SnakeAI by YmC")
clock = pygame.time.Clock

#init game state
direction = Direction.RIGHT

head = Point(WIDTH /2 ,HEIGHT /2)
snake = [head,
          Point(head.x-BLOCK_SIZE,head.y),
          Point(head.x-(2*BLOCK_SIZE),head.y)]