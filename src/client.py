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
        data = recv_data(sock)
        send_data(sock, b"hello")
    
        (board_data, id) = pickle.loads(data) # id is the player's id! 
        (objects, players, width, height, unique_id) = pickle.loads(board_data)

        # reconstruct the gameboard instance
        gameboard = GameBoard(width=width, height=height, objects=objects, \
                              players=players, unique_id=unique_id)
        player = gameboard.get_player(id) # should be our player object!
    
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
                chunk.set_pos(posx, posy)
            
            # TODO: draw food and virus and other players (but have to draw only within the view of the player...how to do that? a camera would come in handy here lol)
            # hypothetical code if camera existed:
            for _, object in gameboard.get_objects().items():
                # a check for seeing if that object is in the player's view or not goes here. maybe we do not need an explicit camera, we could calculate the render rectangle dynamically every time
                pygame.draw.circle(screen, object.get_color(), object.get_pos(), object.get_radius())

            for _, others in gameboard.get_players().items():
                if others.get_id() != id: # render everyone except us
                    chunks = others.get_chunks()
                    for _, chunk in chunks.items():
                        pygame.draw.circle(screen, chunk.get_color(), chunk.get_pos(), chunk.get_radius())

            # TODO: collision detection and handling between players, player and food, player and virus
            # TODO: add a score UI text that increases every time we consume food

            # even though this looks like it is working, the changes are not communicated to the server yet.
            pygame.draw.circle(screen, chunk.get_color(), (posx, posy), chunk.get_radius()) # player

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # TODO: send message to the server that I am disconnecting
                    running = False

    # quit
    pygame.quit()


run_client()