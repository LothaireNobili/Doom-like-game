from settings import *
import pygame as pg
import math
from settings import TILE_SIZE

class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_INIT_POS
        self.angle = PLAYER_INIT_ANGLE
        self.speed = PLAYER_MOV_SPEED 
        self.rot_speed = PLAYER_ROT_SPEED #might be removable
        self.shot = False
        self.health = PLAYER_MAX_HEALTH
        self.rel = 0 #to avoid errors
        self.health_recovery_delay = 700
        self.time_prev = pg.time.get_ticks()
        # diagonal movement correction
        self.diag_move_corr = 1 / math.sqrt(2)
        
    def recover_health(self):
        if self.check_health_recovery_delay() and self.health < PLAYER_MAX_HEALTH:
            self.health += 1

    def check_health_recovery_delay(self):
        time_now = pg.time.get_ticks()
        if time_now - self.time_prev > self.health_recovery_delay:
            self.time_prev = time_now
            return True
        
    def check_game_over(self):
        if self.health <= 0:
            self.health = 0
            self.game.object_renderer.game_over()  
            pg.display.flip()
            pg.time.delay(1500)
            self.game.new_game()
        
    
    def get_damage(self, damage):
        self.health -= damage
        self.game.object_renderer.player_damage()    
        self.game.sound.player_pain.play()
        self.check_game_over()
    
    def single_fire_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.shot and not self.game.weapon.reloading:
                self.game.sound.shotgun.play()
                self.shot = True
                self.game.weapon.reloading = True
        
        #saving that for continuous fire
        #if event.type == pg.MOUSEBUTTONDOWN:
        #    self.shot = True
        #if event.type == pg.MOUSEBUTTONUP:
        #    self.shot = False
    
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
    
    def debug_draw(self):
        pg.draw.line(
            self.game.screen, 
            'white', 
            (self.x * TILE_SIZE, self.y * TILE_SIZE),        
            (self.x * TILE_SIZE + WIDTH * math.cos(self.angle),
            self.y * TILE_SIZE + WIDTH * math. sin(self.angle)),
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
        self.angle %= math.tau #= 2 * math.pi => [2pi]
    
    def update(self):
        self.move()
        self.mouse_control()
        self.recover_health()
        
    @property
    def pos(self):
        return self.x, self.y
    
    @property
    def map_pos(self):
        return int(self.x), int(self.y) #which tile the player is on
        