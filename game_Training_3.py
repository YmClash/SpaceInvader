import pygame

pygame.init()

GREEN = (0, 255, 0)
RED = (255, 0, 0)

WIDTH = 500
HEIGHT = 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FPS = 60

player = pygame.Rect(100, 100, 50, 50)


running = True

while running:

    screen.fill(GREEN)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.y -= 10
            if event.key == pygame.K_DOWN:
                player.y += 10
            if event.key == pygame.K_LEFT:
                player.x -= 10
            if event.key == pygame.K_RIGHT:
                player.x += 10




    player.move(250,250)

    pygame.draw.rect(screen, RED, player)


    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

