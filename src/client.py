"""
client.py
"""

import pygame
import socket
import pickle
from player import Player, Chunk
from gameboard import GameBoard, GameObject
from constants import HOST, PORT, RED, GREEN
from server import send_data, recv_data

FPS = 30
WIDTH = HEIGHT = 600
WHITE = pygame.Color(255, 255, 255)

def run_client():
    """
    Initializes pygame and renders required components for the client, 
    while also communicating game state changes to the server via sockets
    """
    pygame.init()
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    clock = pygame.time.Clock()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        
        running = True

        while running:
            data = recv_data(sock)
            (objects_dict, player) = pickle.loads(data)
            
            clock.tick(FPS)
            screen.fill(WHITE)
            chunks = player.get_chunks()
            mousex, mousey = pygame.mouse.get_pos()
            for _, chunk in chunks.items():
                (posx, posy) = chunk.get_pos()
                radius = chunk.get_radius()
                velocity = chunk.get_velocity()
                color = chunk.get_color()
                if posx < mousex - (radius * 1.25): # TODO: adjust the constant accordingly
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
                chunk.set_pos(posx, posy) # TODO: might have to change once camera and perspective comes into play
            
            ## send the chunks data to the server.
            data = pickle.dumps(chunks)
            send_data(sock, data)

            # Draw the game objects
            for _, object in objects_dict.items():
                # a check for seeing if that object is in the player's view or not goes here. maybe we do not need an explicit camera, we could calculate the render rectangle dynamically every time
                pygame.draw.circle(screen, object.get_color(), object.get_pos(), object.get_radius())
            
            # TODO: add a score UI text that increases every time we consume food

            # even though this looks like it is working, the changes are not communicated to the server yet.
            # pygame.draw.circle(screen, chunk.get_color(), (posx, posy), chunk.get_radius()) # player

            pygame.display.flip()

            ### Change chunks, object_dict ####
            # chunks = 
            # object_dict = 


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # TODO: send message to the server that I am disconnecting
                    running = False
            

    quit
    pygame.quit()


run_client()