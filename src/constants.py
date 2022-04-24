"""
constants.py
A collection of constants used throughout several files
Authors: Ankur Dahal, Ellis Brown, Jackson Parsells, Rujen Amatya
"""

from pygame import Color 

# constants related to networking
HOST = "73.17.141.74"
PORT = 64410
MAX_CONNECTIONS = 100

# the dimensions of the entire "map"
BOARD_HEIGHT = 3000
BOARD_WIDTH = 3000

# the dimensions of the rendered display
WINDOW_HEIGHT = 768
WINDOW_WIDTH = 1366

# properties of game objects
INIT_VIRUS_COUNT =  4
INIT_FOOD_COUNT = 40

FOOD_RADIUS = 4
PLAYER_RADIUS = 20
PLAYER_MINIMUM_RADIUS = 20

PLAYER_VELOCITY = 7
MIN_VELOCITY = 3

VIRUS_RADIUS_MIN = 9
VIRUS_RADIUS_MAX =  40

GREEN = Color(0,255,0)
RED = Color(255,0,0)
BLUE = Color(0,0,255)

MAX_FOOD_IN_GAME = 700
MAX_VIRUS_IN_GAME = 20
MAX_GAME_OBJECTS = 800

# properties related to game mechanics
FOOD_GENERATION_TIME = 0.2
FOOD_GENERATION_ITERATIONS = 10
