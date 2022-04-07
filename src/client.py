"""
client.py
"""

import pygame
import socket
import pickle
from player import Player
from gameboard import GameBoard, GameObject

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 64429  # The port used by the server
BUFFERSIZE = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.send(b"i'm alive")
    data = s.recv(BUFFERSIZE)

# player = pickle.loads(data)
# print(f"Received {player.get_name()}")

# pygame.init()

# FPS = 60
# WIDTH = HEIGHT = 500

# WHITE = pygame.Color(255, 255, 255)

# # Set up the drawing window
# screen = pygame.display.set_mode([WIDTH, HEIGHT])
# clock = pygame.time.Clock()

# running = True
# while running:
#     clock.tick(FPS)
    
#     # get mouse position, and move the circle
#     mousex, mousey = pygame.mouse.get_pos()
#     if posx < mousex - (radius * 1.25):
#         # move right
#         posx = min(WIDTH, posx + velocity)
#     elif posx > mousex + (radius * 1.25):
#         # move left
#         posx = max(0, posx - velocity)
#     if posy > mousey + (radius * 1.25):
#         # move down
#         posy = max(0, posy - velocity)
#     elif posy < mousey - (radius * 1.25):
#         # move up
#         posy = min(HEIGHT, posy + velocity)

#     screen.fill(WHITE)
    
#     # # circle collision detection
#     # if dist < (radius + radius2):
#     #     print("COLLISTION!")
#     #     collided = True
#     #     color = RED
#     # else:
#     #     collided = False
#     #     color = GREEN

#     # draw the circles
    
#     # IDEA: for the actual game, iterate over the gameobject list 
#     #       in the current player's camera view only, and call a general draw function passing in each object
#     #       The draw function will call pygame.draw.circle(screen, object.get_color(), object.get_pos(), object.get_radius()).
#     # also maybe render players that are larger at the end so that when they overlap, the bigger circle will be on top. (Is this how it works on pygame? Have to investigate.)

#     # pygame.draw.circle(screen, color, (posx, posy), radius) # player
#     # pygame.draw.circle(screen, (0, 255, 255), (object_posx, object_posy), radius2) # stationary circle
#     pygame.display.flip()

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             # TODO: send message to the server that I am disconnecting
#             running = False

# # quit
# pygame.quit()
