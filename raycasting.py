import pygame as pg
import math
from settings import *

class RayCasting:
    def __init__(self, game):
        self.game = game
        self.ray_casting_result = []
        self.objects_to_render = []
        self.textures = self.game.object_renderer.wall_textures
    
    def get_objects_to_render(self):
        self.objects_to_render = []
        for ray, values in enumerate(self.ray_casting_result):
            depth, proj_height, texture, offset = values
            
            if proj_height < HEIGHT:
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 
                    0, 
                    SCALE, 
                    TEXTURE_SIZE
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, proj_height))
                wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)    
                
            else:
                texture_height = TEXTURE_SIZE * HEIGHT / proj_height
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 
                    HALF_TEXTURE_SIZE - texture_height // 2,
                    SCALE, 
                    texture_height
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, HEIGHT))
                wall_pos = (ray * SCALE, 0)
            
            self.objects_to_render.append((depth, wall_column, wall_pos))
        
    
    #in the following function, horizontal and vertical are about the grid seen from above, not right/left or up/down from fpw
    def ray_cast(self):
        self.ray_casting_result = []
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos
        
        texture_vert, texture_hor = None, None #to avoid errors
        
        ray_angle = self.game.player.angle - HALF_FOV + 0.0001 #to avoid division by 0
        for ray in range(NUM_RAYS):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)
            
            #horizontals
            #we start by checking the closest horizontal intersection
            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1) #the small value is to offset the tiled checed to the top if sin is negative

            depth_hor = (y_hor - oy) / sin_a
            x_hor = ox + depth_hor * cos_a

            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            #we continue by check all the ones after the first
            for i in range(MAX_DEPTH):  #depth = how many tiles we check
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.game.map.world_map: #if the ray hits a wall
                    texture_hor = self.game.map.world_map[tile_hor]
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth
            
            #verticals
            #we start by checking the closest vertical intersection
            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1) #the small value is to offset the tiled checed to the left if cos is negative

            depth_vert = (x_vert - ox) / cos_a
            y_vert = oy + depth_vert * sin_a
            
            delta_depth = dx / cos_a
            dy = delta_depth * sin_a
            
            #we continue by check all the ones after the first
            for i in range(MAX_DEPTH): #depth = how many tiles we check
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.game.map.world_map: #if the ray hits a wall
                    texture_vert = self.game.map.world_map[tile_vert]
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth
                
            #depth + texture offset
            if depth_vert < depth_hor:
                depth, texture = depth_vert, texture_vert
                y_vert %= 1
                offset = y_vert if cos_a > 0 else (1 - y_vert)
            else:
                depth, texture = depth_hor, texture_hor
                x_hor %= 1
                offset = x_hor if sin_a > 0 else (1 - x_hor)
              
            # remove fish eye effect
            depth *= math.cos(self.game.player.angle - ray_angle)
            
            #projection
            proj_height = SCREEN_DIST / (depth + 0.0001) #to avoid division by 0
            
            #ray casting
            self.ray_casting_result.append((depth, proj_height, texture, offset))
            
            """
            #draw walls
            color = [255 / (1 + depth ** 2 * 0.002)] * 3
            pg.draw.rect(
                self.game.screen,
                color,
                (ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height)
            )"""
                        
            ray_angle += DELTA_ANGLE
    
    def update(self):
        self.ray_cast()
        self.get_objects_to_render()