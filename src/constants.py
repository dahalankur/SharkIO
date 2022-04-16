# declaration of constant values used in multiple files of the program
from pygame import Color 

HOST = "127.0.0.1"  # localhost
PORT = 64417  # any port, arbitrarily picked

BOARD_HEIGHT = 768
BOARD_WIDTH = 1366
INIT_VIRUS_COUNT =  3
INIT_FOOD_COUNT = 30
FOOD_RADIUS = 2.2
PLAYER_RADIUS = 20
PLAYER_MINIMUM_RADIUS = 20
PLAYER_VELOCITY = 7
MIN_VELOCITY = 3
MAX_CONNECTIONS = 100
VIRUS_RADIUS_MIN = 9
VIRUS_RADIUS_MAX =  20
GREEN = Color(0,255,0)
RED = Color(255,0,0)
BLUE = Color(0,0,255)
FOOD_GENERATION_TIME = 0.3

FOOD_GENERATION_ITERATIONS = 10
MAX_FOOD_IN_GAME = 48
MAX_VIRUS_IN_GAME = 8