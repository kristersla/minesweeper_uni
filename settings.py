import json
import os

import pygame

# COLORS (r, g, b)
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
MULTIPLAYER_SIDEBAR_WIDTH = 240


class Settings:
    def __init__(self, rows=None, cols=None, probability=None, width=None):
        data_tiles = self._read_json("jsons/tiles.json", {"tiles": 10})
        data_prob = self._read_json("jsons/prob.json", {"prob": 0.15})
        data_res = self._read_json("jsons/resx.json", {"width": 720})

        self.rows = int(rows if rows is not None else data_tiles["tiles"])
        self.cols = int(cols if cols is not None else data_tiles["tiles"])
        self.probability_mines = float(
            probability if probability is not None else data_prob["prob"]
        )
        self.amount_mines = int(self.rows * self.cols * self.probability_mines)

        self.tilesize = int(width if width is not None else data_res["width"]) // max(
            self.rows, self.cols
        )
        self.screen_width = self.tilesize * self.cols
        self.screen_height = self.tilesize * self.rows
        self.fps = 120
        self.title = "Minesweeper"

        self.tile_numbers = [
            pygame.transform.scale(
                pygame.image.load(os.path.join("images", f"Tile{i}.png")),
                (self.tilesize, self.tilesize),
            )
            for i in range(1, 9)
        ]
        self.tile_empty = pygame.transform.scale(
            pygame.image.load(os.path.join("images", "TileEmpty.png")),
            (self.tilesize, self.tilesize),
        )
        self.tile_exploded = pygame.transform.scale(
            pygame.image.load(os.path.join("images", "TileExploded.png")),
            (self.tilesize, self.tilesize),
        )
        self.tile_flag = pygame.transform.scale(
            pygame.image.load(os.path.join("images", "TileFlag.png")),
            (self.tilesize, self.tilesize),
        )
        self.tile_mine = pygame.transform.scale(
            pygame.image.load(os.path.join("images", "TileMine.png")),
            (self.tilesize, self.tilesize),
        )
        self.tile_unknown = pygame.transform.scale(
            pygame.image.load(os.path.join("images", "TileUnknown.png")),
            (self.tilesize, self.tilesize),
        )
        self.tile_not_mine = pygame.transform.scale(
            pygame.image.load(os.path.join("images", "TileNotMine.png")),
            (self.tilesize, self.tilesize),
        )

    @classmethod
    def from_values(cls, rows, cols, probability, width):
        return cls(rows=rows, cols=cols, probability=probability, width=width)

    @staticmethod
    def _read_json(path, fallback):
        if not os.path.exists(path):
            return fallback
        with open(path, "r") as file_handle:
            return json.load(file_handle)