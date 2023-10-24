import pygame
import random

pygame.init()

longeur = 800
largeur = 600

FPS = 60

screen = pygame.display.set_mode((longeur,largeur))
clock = pygame.time.Clock
def generate_startfield(screen, num_stars):
    for s in range(num_stars):
        print(s)
        x = random.randint(0, screen.get_width())
        y = random.randint(0,screen.get_height())
        size = random.randint(1, 3)
        color = random.randint(1,255)
        pygame.draw.circle(screen,(color,color,color),(x,y),size)
        print(f"X: {x}"
              f" Y: {y}"
              f" size: {size}"
              f" color: {color}")

running = True

while running:

    clock = FPS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    generate_startfield(screen,1)

    pygame.display.flip()


pygame.quit()



