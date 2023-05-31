import random
import pygame
from snake import redimension


pygame.init()

fenetre = pygame.display.set_mode((200,200))

img= pygame.image.load('mogwai .PNG')
player = redimension(img)

fenetre.blit(player,(0,0))

pygame.display.flip()

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


pygame.quit()