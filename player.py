from settings import *
import pygame as pg
import math

class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_INIT_POS
        self.angle = PLAYER_INIT_ANGLE
        self.speed = PLAYER_MOV_SPEED
        self.rot_speed = PLAYER_ROT_SPEED
    
    def move(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = self.speed * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a
        
        keys = pg.key.get_pressed() #put that in a function letter for cleaner code
        if keys[pg.K_z]:    #change the input system to be customizable later
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            dx -= speed_cos
            dy -= speed_sin
        if keys[pg.K_q]:
            dx += speed_sin
            dy -= speed_cos
        if keys[pg.K_d]:
            dx -= speed_sin
            dy += speed_cos
            
        self.check_wall_collision(dx, dy)
        
        if keys[pg.K_LEFT]: #change that to mouse input later
            self.angle -= self.rot_speed * self.game.delta_time
        if keys[pg.K_RIGHT]:
            self.angle += self.rot_speed * self.game.delta_time
        self.angle %= math.tau #= 2 * math.pi => [2pi]
    
    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map
    
    def check_wall_collision(self, dx, dy):
        if self.check_wall(int(self.x + dx), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy)):
            self.y += dy
    
    def draw(self):
        pg.draw.line(
            self.game.screen, 
            'white', 
            (self.x * 64, self.y * 64), 
            (self.x * 64 + WIDTH * math.cos(self.angle),
             self.y * 64 + WIDTH * math.sin(self.angle)),
             2)
        
        pg.draw.circle(
            self.game.screen, 
            'yellow', 
            (int(self.x * 64), int(self.y * 64)),
            15)
    
    def update(self):
        self.move()
        
    @property
    def pos(self):
        return self.x, self.y
    
    @property
    def map_pos(self):
        return int(self.x), int(self.y) #which tile the player is on
        