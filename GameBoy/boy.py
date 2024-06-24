import pygame
import random
import player

import pyscroll
import pytmx
pygame.init()



GEO = r'C:\Users\y_mc\PycharmProjects\SpaceInvader\GameBoy\carte\carte_1.tmx'
class Game:
    def __init__(self):
        pass




#fenetre
WIDTH = 800
HEIGHT = 800

#COLORS

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
RANDOM_COLOR = (random.randint(0,255),random.randint(0,255),random.randint(0,255))


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GameBoy")

#charger la carte tiled

tmx_data = pytmx.util_pygame.load_pygame(GEO)
map_data = pyscroll.data.TiledMapData(tmx_data)
map_layer = pyscroll.orthographic.BufferedRenderer(map_data,screen.get_size())
map_layer.zoom = 2



# genere joueur
player_position = tmx_data.get_object_by_name('player')
player = player.Player(player_position.x,player_position.y)


# dessiner la carte
group = pyscroll.PyscrollGroup(map_layer=map_layer,default_layer=3)
group.add(player)





running = True

while running:
    group.update()
    group.center(player.rect)
    group.draw(screen)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False



pygame.quit()



















"""
import pyboy
import random
#
# numb = [random.randint(0,10) for o in range(10)]
#
# print(numb)
#
# print(numb[:5])
# print(numb[9:])

# def perm(l) :
# # Compute the list of all permutations of l
#     if len(l) <= 1 :
#         return [l]
#     r = []
#     for i in range(len(l)) :
#         s = l[:i] + l[i + 1 :]
#         p = perm(s)
#     for x in p :
#         r.append(l[i :i + 1] + x)
#     return r
#
#
# toto = perm("Hallo")
# print(toto)

def perm(l):
    # if len(l) <= 1:
    #     return [l]
    # r = []
    # for i in range(len(l)):
    if len(l) <= 1 :
        return [l]
    r = []
    for i in range(len(l)) :
        # s = l[:i] + l[i+1:]
        # p = perm(s)
        s = l[:i] + l[i + 1 :]
        p = perm(s)
        for x in p:
            # r.append(l[i :i + 1] + x)
            r.append(l[i :i + 1] + x)
    return (r)


toto = perm("hallo")

print(toto)

"""