# COLORS (r, g, b)
import pygame
import os
import json

print("settings")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
DARKGREEN = (0, 200, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BGCOLOUR = DARKGREY

with open('jsons/tiles.json', 'r') as f:
    tiles = json.load(f)

with open('jsons/prob.json', 'r') as f:
    prob = json.load(f)

with open('jsons/resx.json', 'r') as f:
    res = json.load(f)


# game settings

ROWS = int(tiles['tiles'])
COLS = int(tiles['tiles'])
print(tiles['tiles'])
print(prob['prob'])
PROBABILITY_MINES = prob['prob'] # probability of a tile being a mine
AMOUNT_MINES = int(ROWS * COLS * PROBABILITY_MINES)  # calculate number of mines based on probability

TILESIZE = int(res['width']) // max(ROWS, COLS)  # Adjust tile size to fit the screen
SCREEN_WIDTH = TILESIZE * COLS
SCREEN_HEIGHT = TILESIZE * ROWS
FPS = 120
TITLE = "Minesweeper"

tile_numbers = []
for i in range(1, 9):
    tile_numbers.append(pygame.transform.scale(pygame.image.load(os.path.join("images", f"Tile{i}.png")), (TILESIZE, TILESIZE)))

tile_empty = pygame.transform.scale(pygame.image.load(os.path.join("images", "TileEmpty.png")), (TILESIZE, TILESIZE))
tile_exploded = pygame.transform.scale(pygame.image.load(os.path.join("images", "TileExploded.png")), (TILESIZE, TILESIZE))
tile_flag = pygame.transform.scale(pygame.image.load(os.path.join("images", "TileFlag.png")), (TILESIZE, TILESIZE))
tile_mine = pygame.transform.scale(pygame.image.load(os.path.join("images", "TileMine.png")), (TILESIZE, TILESIZE))
tile_unknown = pygame.transform.scale(pygame.image.load(os.path.join("images", "TileUnknown.png")), (TILESIZE, TILESIZE))
tile_not_mine = pygame.transform.scale(pygame.image.load(os.path.join("images", "TileNotMine.png")), (TILESIZE, TILESIZE))