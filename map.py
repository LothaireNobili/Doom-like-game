import pygame as pg
from settings import TILE_SIZE

#for better visibility, we use _ for blancs and X for walls
_ = False
X = True

mini_map = [
    [X, X, X, X, X, X, X, X, X, X],
    [X, _, _, _, _, _, _, _, _, X],
    [X, _, X, X, X, _, X, X, _, X],
    [X, _, _, _, X, _, _, X, _, X],
    [X, _, X, X, X, _, _, _, _, X],
    [X, _, _, _, _, _, _, _, _, X],
    [X, _, _, _, _, _, X, X, X, X],
    [X, _, _, X, _, _, _, _, _, X],
    [X, _, _, X, _, _, _, _, _, X],
    [X, X, X, X, X, X, X, X, X, X]
]

class Map:
    def __init__(self, game):
        self.game = game
        self.map = mini_map
        self.world_map = {}
        self.get_map()
        
    def get_map(self):
        for y, row in enumerate(self.map):
            for x, tile in enumerate(row):
                if tile:
                    self.world_map[(x, y)] = tile
        
    def draw(self):
        [pg.draw.rect(
            self.game.screen,   #where
            'red',              #color        
            (pos[0] * TILE_SIZE, pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE), #rectangle pos and dim
            2)                #border width 
            for pos in self.world_map
        ]