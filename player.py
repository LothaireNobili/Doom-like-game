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
        
        #if keys[pg.K_LEFT]: #change that to mouse input later
        #    self.angle -= self.rot_speed * self.game.delta_time
        #if keys[pg.K_RIGHT]:
        #    self.angle += self.rot_speed * self.game.delta_time
        #self.angle %= math.tau #= 2 * math.pi => [2pi]
    
    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map
    
    def check_wall_collision(self, dx, dy):
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy
    
    def draw(self):
        pg.draw.line(
            self.game.screen, 
            'white', 
            (self.x * 100, self.y * 100),        
            (self.x * 100 + WIDTH * math.cos(self.angle),
            self.y * 100 + WIDTH * math. sin(self.angle)),
            2
        )
        
        pg.draw.circle(
            self.game.screen, 
            'yellow', 
            (int(self.x * TILE_SIZE), int(self.y * TILE_SIZE)),
            15)
    
    def mouse_control(self):
        mx, my = pg.mouse.get_pos() #my is not used, but it exist to make getting mouse pos more convenient
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time
    
    def update(self):
        self.move()
        self.mouse_control()
        
    @property
    def pos(self):
        return self.x, self.y
    
    @property
    def map_pos(self):
        return int(self.x), int(self.y) #which tile the player is on
        