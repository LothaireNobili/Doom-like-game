import pygame as pg
import sys
from settings import *
from map import *
from player import *

class Game:
    def __init__(self):
        pg.init()
        self.playing = None
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.new()
        
    def new(self):
        self.map = Map(self)
        self.player = Player(self)
    
    def update(self):
        self.player.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')
        
    def draw(self):
        self.screen.fill('black')
        self.map.draw()
        self.player.draw()
        
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.playing = False
                pg.quit()
                sys.exit()
        
    def run(self):
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()
            
if __name__ == '__main__':
    g = Game()
    g.run()