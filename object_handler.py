from sprite_object import *
from npc import *

#this class is a manager for all objects on map (fixed and animated decoration + ennemies)
#it can be see as an artbiter of the game
class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.npc_list = []
        self.npc_sprite_path = 'resources/sprites/npc/'
        self.static_sprite_path = 'resources/sprites/static_sprites/'
        self.anim_sprite_path = 'resources/sprites/animated_sprites/'
        add_sprite = self.add_sprite
        add_npc = self.add_npc
        
        ###note for later : automate that with a file of data instead of raw code
        # sprite map
        add_sprite(SpriteObject(game)) #default data
        add_sprite(AnimatedSprite(game)) #default data
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'red_light/0.png', pos=(12.5, 7.5))) #custom data

        #npc map
        add_npc(NPC(game))
        
    
    def update(self):
        [sprite.update() for sprite in self.sprite_list]
        [npc.update() for npc in self.npc_list]
        #print(self.sprite_list)
        
    def add_npc(self, npc):
        self.npc_list.append(npc)

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)