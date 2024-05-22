import math

#game main config
RES = WIDTH,HEIGHT = 1080,720
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 60
TILE_SIZE = 64

#raycasting config
FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = WIDTH // 2
HALF_NUM_RAYS = NUM_RAYS // 2
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = 20 

SCREEN_DIST = HALF_WIDTH / math.tan(HALF_FOV)
SCALE = WIDTH // NUM_RAYS

#player config
PLAYER_INIT_POS = 1.5, 5
PLAYER_INIT_ANGLE = 0
PLAYER_MOV_SPEED = 0.004
PLAYER_ROT_SPEED = 0.002
