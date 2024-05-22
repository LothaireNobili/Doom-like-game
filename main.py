import pygame as pg
import sys
from settings import *
from map import *

class Game:
    def __init__(self):
        pg.init()
        self.playing = None
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.new()
        
    def new(self):
        self.map = Map(self)
    
    def update(self):
        pg.display.flip()
        self.clock.tick(FPS)
        pg.display.set_caption(f'{self.clock.get_fps() :.1f}')
        
    def draw(self):
        self.screen.fill('black')
        self.map.draw()
        
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