import pygame as pg

class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.path = 'resources/sound/'
        self.shotgun = pg.mixer.Sound(self.path + 'shotgun.wav')
        self.shotgun.set_volume(0.2)
        self.npc_pain = pg.mixer.Sound(self.path + 'npc_pain.wav')
        self.npc_death = pg.mixer.Sound(self.path + 'npc_death.wav')
        self.npc_shot = pg.mixer.Sound(self.path + 'npc_attack.wav')
        self.player_pain = pg.mixer.Sound(self.path + 'player_pain.wav')
        self.theme = pg.mixer.music.load(self.path + 'theme.mp3')
        
        sounds = [
            self.shotgun, 
            self.npc_pain, 
            self.npc_death, 
            self.npc_shot, 
            self.player_pain
            ]

        [sound.set_volume(0.2) for sound in sounds]
