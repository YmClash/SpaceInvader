# import random
# import pygame
# from snake import redimension
#
def get_string_methods(method):
    i: int = 0
    for method in dir(method):
        if '__' not in method:
            # print(f"{i} : {method}")
            i += 1
            print(f"{i} : {method}")


get_string_methods(str)



# pygame.init()
#
# fenetre = pygame.display.set_mode((200,200))
#
# img= pygame.image.load('mogwai .PNG')
# player = redimension(img)
#
# fenetre.blit(player,(0,0))
#
# pygame.display.flip()
#
# run = True
#
# while run:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run = False
#
#
# pygame.quit()