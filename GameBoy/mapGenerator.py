import random
import numpy as np
import pytmx
from pytmx import TiledMap, TiledTileLayer, TiledTileset

TILESET_PATH = r'C:\Users\y_mc\PycharmProjects\SpaceInvader\GameBoy\Pygamon\assets\maps\RPG Nature Tileset.png'

# Configuration de la carte
MAP_WIDTH = 100
MAP_HEIGHT = 100
TILE_SIZE = 16

# Types de terrains
GRASS = 0
WATER = 1
MOUNTAIN = 2
FOREST = 3
DESERT = 4
SNOW = 5

# Fonction pour créer une carte vide
def create_empty_map(width, height):
    return np.zeros((width, height), dtype=int)

# Fonction pour ajouter des terrains
def add_terrain(map_array, terrain_type, density=0.1):
    for x in range(map_array.shape[0]):
        for y in range(map_array.shape[1]):
            if random.random() < density:
                map_array[x, y] = terrain_type

# Fonction pour générer et sauvegarder la carte en format TMX
def generate_map(file_name):
    map_array = create_empty_map(MAP_WIDTH, MAP_HEIGHT)

    # Ajouter des terrains
    add_terrain(map_array, GRASS, 0.6)
    add_terrain(map_array, WATER, 0.1)

    # Créer une carte Tiled
    tiled_map = TiledMap()
    tiled_map.width = MAP_WIDTH
    tiled_map.height = MAP_HEIGHT
    tiled_map.tilewidth = TILE_SIZE
    tiled_map.tileheight = TILE_SIZE

    # Ajouter un tileset
    tileset = TiledTileset(TILESET_PATH)
    tileset.name = 'terrain'
    tileset.firstgid = 1
    tileset.images.append(pytmx.TileSetImage(source=TILESET_PATH))

    tiled_map.tilesets.append(tileset)

    # Ajouter une couche de tuiles
    tile_layer = TiledTileLayer(MAP_WIDTH, MAP_HEIGHT)
    for x in range(MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            gid = map_array[x, y] + 1
            tile_layer.tiles[x][y] = gid

    tiled_map.layers.append(tile_layer)

    # Sauvegarder la carte en format TMX
    tiled_map.save(file_name)

# Générer et sauvegarder la carte
generate_map('map.tmx')

print("Map generation done")
