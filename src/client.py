"""
client.py
"""

import pygame
import socket
import pickle
from constants import *
from server import send_data, recv_data
from os import listdir

FPS = 60
WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)
padding = 100 

def init_pygame():
    """
    Initializes the pygame instance and returns the display, clock, a couple 
    of fonts for rendering text and the world surface 
    """
    pygame.init()
    # Display represents the window of the game we are able to see
    display = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    pygame.display.set_caption("SharkIO")
    
    # world represents the entire map of things
    world = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT))
    world.fill(pygame.Color(255, 255, 255))
    
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("segoe ui", 34, True)
    font2 = pygame.font.SysFont("segoe ui", 15, True)
    
    return display, clock, font, font2, world

def render_scores(font, font2, player, display, players):
    text = font.render("Score: " + str(int(player.get_score())), True, (255, 0, 0))
    display.blit(text, (30, 700))

    # render leaderboard
    loc = 20
    leader_txt = 'Leaderboard'
    text2 = font2.render(leader_txt, True, (255, 0, 0))
    display.blit(text2, (1220, loc))

    players_list = list(players.values())
    players_list.sort(key=lambda x: x.get_score(), reverse=True)

    for player in players_list:
        loc = loc + 15
        leader_txt2 = str(player.get_name()) + ": " + str(int(player.get_score()))
        text3 = font2.render(leader_txt2, True, (255, 0, 0))
        display.blit(text3, (1220, loc))

def run_client():
    """
    Initializes pygame and renders required components for the client, 
    while also communicating game state changes to the server via sockets
    """

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))

        # send player name to the server
        name = bytes(input("Enter your name: ").encode('utf-8'))
        send_data(sock, name)

        display, clock, font, font2, world = init_pygame()
        running = True
        
        while running:
            data = recv_data(sock)
            (objects_dict, players, player) = pickle.loads(data)
            
            clock.tick(FPS)
            
            display.fill(BLACK) 
            world.fill(WHITE)
            
            chunk = player.get_chunk()
            (posx, posy) = chunk.get_pos()
            velocity = chunk.get_velocity()
            
            # We define the X and Y camera coordinates based off of the  
            # current location, the screen size, and the fact that the 
            # camera movement and player movement are inversely related.
            # X = Xc + Xp = w/2 => Xc = w/2 - Xp
            # y = yc + yp = h/2 => Yc = h/2 - Yp
            camera_x = (WINDOW_WIDTH / 2) - posx
            camera_y = (WINDOW_HEIGHT / 2) - posy
            
            # check what keys have been pressed each frame, and move
            key = pygame.key.get_pressed() 
            
            # Up and down motion
            if key[pygame.K_w] or key[pygame.K_UP]:
                posy = max(0, posy - velocity)
            if key[pygame.K_s] or key[pygame.K_DOWN]:
                posy = min(BOARD_HEIGHT, posy + velocity)
            # Left to right motion
            if key[pygame.K_a] or key[pygame.K_LEFT]:
                posx = max(0, posx - velocity)
            if key[pygame.K_d] or key[pygame.K_RIGHT]:
                posx = min(BOARD_WIDTH, posx + velocity)

            chunk.set_pos(posx, posy)

            # Draw the game objects
            for _, object in objects_dict.items():
                pygame.draw.circle(world, object.get_color(), object.get_pos(), object.get_radius())

            # Draw the players
            for p in players.values():
                p_chunk = p.get_chunk()

                bg_circle = pygame.draw.circle(world, p_chunk.get_color(), p_chunk.get_pos(), p_chunk.get_radius())

                # scale the shark image to the radius of the background circle
                scaled_shark = p.get_shark_as_image((p_chunk.get_radius(), p_chunk.get_radius()))

                # blit the scaled shark image to be centered on the background circle
                world.blit(scaled_shark, (bg_circle.centerx - scaled_shark.get_width() / 2, bg_circle.centery - scaled_shark.get_height() / 2))
            
            
            display.blit(world, (camera_x, camera_y)) # Render Map To The Display
            
            # render score UI
            render_scores(font, font2, player, display, players)

            pygame.display.update() 

            # send the updated chunk data to the server.
            data = pickle.dumps(chunk)
            send_data(sock, data)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

    pygame.quit()


run_client()
