import pygame
import random


pygame.init()

BLACK =(0,0,0)
GREY = (128,128,128)
YELLOW = (255,225,0)
TURQUOI = (116,214,190)


WIDTH,HEIGHT = 500,500
TILE_SIZE = 20
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
FPS = 60


screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

def gen(numb):
    return set([(random.randrange(0, GRID_HEIGHT),random.randrange(0,GRID_WIDTH))for _ in range(numb)])




def draw_grid(positions):
    for position in positions:
        col,row = position
        top_left = (col * TILE_SIZE,row * TILE_SIZE)
        pygame.draw.rect(screen,YELLOW,(*top_left,TILE_SIZE,TILE_SIZE))

    for row in range(GRID_HEIGHT):
        pygame.draw.line(screen,BLACK,(0,row*TILE_SIZE),(WIDTH,row*TILE_SIZE))

    for col in range (GRID_WIDTH):
        pygame.draw.line(screen, BLACK, (col * TILE_SIZE, 0), (col * TILE_SIZE,HEIGHT))


def ajust_grid(positions):
    pass



def main():
    running = True

    positions = set()
    positions.add((10,10))
    playing = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // TILE_SIZE
                row = y // TILE_SIZE
                pos = (col,row)

                if pos in positions:
                    positions.remove(pos)
                else:
                    positions.add(pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = not playing

                if event.key == pygame.K_c:
                    positions = set()
                    playing = False

                if event.key == pygame.K_g:
                    positions = gen(random.randrange(4,5) * GRID_WIDTH)



        screen.fill(TURQUOI)
        draw_grid(positions)
        pygame.display.flip()
        pygame.display.update()


    pygame.quit()

if __name__=="__main__":
    main()



