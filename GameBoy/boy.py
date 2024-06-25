import pygame
import random
import player

import pyscroll
import pytmx
pygame.init()



GEO = r'C:\Users\y_mc\PycharmProjects\SpaceInvader\GameBoy\carte\carte_1.tmx'
HOUSE = r'C:\Users\y_mc\PycharmProjects\SpaceInvader\GameBoy\carte\house.tmx'
class Game:
    def __init__(self):
        pass




#fenetre
WIDTH = 800
HEIGHT = 800


FPS = 60

#COLORS

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
RANDOM_COLOR = (random.randint(0,255),random.randint(0,255),random.randint(0,255))


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GameBoy")
clock = pygame.time.Clock()

#charger la carte tiled

tmx_data = pytmx.util_pygame.load_pygame(GEO)
map_data = pyscroll.data.TiledMapData(tmx_data)
map_layer = pyscroll.orthographic.BufferedRenderer(map_data,screen.get_size())
map_layer.zoom = 2



# genere joueur
player_position = tmx_data.get_object_by_name('player')
player = player.Player(player_position.x,player_position.y)

 # defini  une  liste   pour les collision de  la map

collisions = []

for obj in tmx_data.objects:
    if obj.type == 'collision':
        collisions.append(pygame.Rect(obj.x,obj.y,obj.width,obj.height))

# dessiner la carte
group = pyscroll.PyscrollGroup(map_layer=map_layer,default_layer=10)
group.add(player)


# definir le rect
#
# enter_house = tmx_data.get_object_by_name('enter_house')
# enter_house_rect = pygame.Rect(enter_house.x,enter_house.y)



def handel_input():
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]:
        player.move_up()
        player.chang_animation('up')
        print("up")
    elif pressed[pygame.K_DOWN]:
        player.move_down()
        player.chang_animation('down')
        print("down")
    elif pressed[pygame.K_LEFT]:
        player.move_left()
        player.chang_animation('left')
        print("left")
    elif pressed[pygame.K_RIGHT]:
        player.move_right()
        player.chang_animation('right')
        print("right")


# CETTE FONCTION N'EST PAS TERMINER
def swich_house(self):
    # charger la carte de la maison
    tmx_data = pytmx.util_pygame.load_pygame(HOUSE)
    map_data = pyscroll.data.TiledMapData(tmx_data)
    map_layer = pyscroll.orthographic.BufferedRenderer(map_data,screen.get_size())




def update():
    group.update()
    # verifier sie on es entre dans une maison


    # verification  de collision
    for player in group.sprites():
        if player.feet.collidelist(collisions) > -1:
            player.move_back()





running = True

while running:

    player.save_location()
    handel_input()
    update()
    group.center(player.rect)
    group.draw(screen)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        #
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_UP:
        #         print("up")
        #         player.rect.x -= 10
        #     elif event.key == pygame.K_DOWN:
        #         print("down")
        #         player.rect.y += 10
        #     elif event.key == pygame.K_LEFT:
        #         print("left")
        #         player.rect.x = -10
        #     elif event.key == pygame.K_RIGHT:
        #         print("right")
        #         player.rect.x +=10

    clock.tick(FPS)





pygame.quit()









