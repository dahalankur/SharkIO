"""
client.py
"""

import pygame
import socket
import pickle
from player import Player, Chunk
from gameboard import GameBoard, GameObject
from constants import RED, GREEN

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 64421  # The port used by the server
BUFFERSIZE = 10000 # TODO: this is wacky, look out for a solution

FPS = 30
WIDTH = HEIGHT = 500
WHITE = pygame.Color(255, 255, 255)

def run_client():

    pygame.init()
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    clock = pygame.time.Clock()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        data = sock.recv(BUFFERSIZE) # TODO: make sure to receive ALL sent data
        sock.send(b"hi")
    
        (board_data, id) = pickle.loads(data) # id is the player's id! 
        (objects, players, width, height, unique_id) = pickle.loads(board_data)

        # reconstruct the gameboard instance
        gameboard = GameBoard(width=width, height=height, objects=objects, players=players, unique_id=unique_id)
        player = gameboard.get_player(id) # should be our player object!
        # print(gameboard.get_player(id)) # should be our player object!!
    

        running = True
        while running:
            clock.tick(FPS)
            # TODO: for now, assume each player has only one chunk
            chunks = player.get_chunks()
            for _, chunk in chunks.items():
                (posx, posy) = chunk.get_pos()
                radius = chunk.get_radius()
                velocity = chunk.get_velocity()
                color = chunk.get_color()
                # get mouse position, and move the chunk (TODO: for now, each chunk is independently moved)
                # also, this needs to be communicated with the server so that it is reflected on all connected clients
                mousex, mousey = pygame.mouse.get_pos()
                if posx < mousex - (radius * 1.25):
                    # move right
                    posx = min(WIDTH, posx + velocity)
                elif posx > mousex + (radius * 1.25):
                    # move left
                    posx = max(0, posx - velocity)
                if posy > mousey + (radius * 1.25):
                    # move down
                    posy = max(0, posy - velocity)
                elif posy < mousey - (radius * 1.25):
                    # move up
                    posy = min(HEIGHT, posy + velocity)

                print(radius, velocity, posx, posy, mousex, mousey)
                screen.fill(WHITE)

                # TODO: update the player and all its chunk objects with the changed attributes (new positions), if there are any collisions with a food, remove the food, and update the gameboard instance. Send the pickled instance to the server.

                pygame.draw.circle(screen, chunk.get_color(), (posx, posy), chunk.get_radius()) # player
                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        # TODO: send message to the server that I am disconnecting
                        running = False

    # quit
    pygame.quit()


run_client()