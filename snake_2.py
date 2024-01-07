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

BLACK = (0,0,0)
WHITE = (225,250,250)
RED = (232, 26, 26)
GREEN =(15, 250, 2)
BLAU = (7, 92, 240)
RANDOM_COLOR = (random.randint(0,250),random.randint(0,250),random.randint(0,250))

BLOCK_SIZE = 20
SPEED = 5

WIDTH = 650
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("SnakeAI by YmC")
clock = pygame.time.Clock()

direction = Direction.RIGHT
head = Point(WIDTH /2 ,HEIGHT / 2)
snake = [head, Point(head.x-BLOCK_SIZE,head.y), Point(head.x-(2*BLOCK_SIZE),head.y)]
score = 0
food = None

def place_food():
    global food
    x = random.randint(0, (WIDTH-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
    y = random.randint(0, (HEIGHT-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
    food = Point(x,y)
    if food in snake:
        place_food()

def is_collision():
    if head.x > WIDTH - BLOCK_SIZE or head.x < 0 or head.y > HEIGHT - BLOCK_SIZE or head.y < 0 :
        return True
    if head in snake[1:]:
        return True
    return False

def update_ui():
    screen.fill(BLACK)
    for pt in snake:
        pygame.draw.rect(screen,BLAU,pygame.Rect(pt.x,pt.y ,BLOCK_SIZE,BLOCK_SIZE))
        pygame.draw.rect(screen,GREEN,pygame.Rect(pt.x,pt.y ,12,12))
    pygame.draw.rect(screen,RED, pygame.Rect(food.x,food.y, BLOCK_SIZE,BLOCK_SIZE))
    text = font.render("Score : " + str(score), True,WHITE)
    screen.blit(text,[0,0])
    pygame.display.flip()

def move(direction):
    global head
    x = head.x
    y = head.y
    if direction == Direction.RIGHT:
        x += BLOCK_SIZE
    elif direction == Direction.LEFT:
        x -= BLOCK_SIZE
    elif direction == Direction.DOWN:
        y += BLOCK_SIZE
    elif direction == Direction.UP:
        y -= BLOCK_SIZE
    head = Point(x,y)

def play_step():
    global direction, score, snake, head
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                direction = Direction.LEFT
            elif event.key == pygame.K_RIGHT:
                direction = Direction.RIGHT
            elif event.key == pygame.K_UP:
                direction = Direction.UP
            elif event.key == pygame.K_DOWN:
                direction = Direction.DOWN
    move(direction)
    snake.insert(0,head)
    game_over = False
    if is_collision():
        game_over = True
        return game_over, score
    if head == food:
        score += 1
        place_food()
    else:
        snake.pop()
    update_ui()
    clock.tick(SPEED)
    return game_over, score

if __name__ == '__main__':
    place_food()
    while True:
        game_over, score = play_step()
        if game_over:
            break
    print(f'Score Final : {score}')

    pygame.quit()