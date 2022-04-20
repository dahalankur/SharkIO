"""
client.py
"""

import time
import pygame
import socket
import pickle
from player import Player, Chunk
from gameboard import GameBoard, GameObject
from constants import HOST, PORT, BOARD_HEIGHT, BOARD_WIDTH, PLAYER_MINIMUM_RADIUS, RED
from server import send_data, recv_data
from os import listdir
from random import choice

FPS = 44
WHITE = pygame.Color(255, 255, 255)


def init_pygame():
    pygame.init()
    screen = pygame.display.set_mode([BOARD_WIDTH, BOARD_HEIGHT])
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("segoe ui", 34, True)
    font2 = pygame.font.SysFont("segoe ui", 15, True)
    return screen, clock, font, font2


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

        screen, clock, font, font2 = init_pygame()
        running = True

        while running:
            data = recv_data(sock)

            (objects_dict, players, player) = pickle.loads(data)

            clock.tick(FPS)
            screen.fill(WHITE)
            chunk = player.get_chunk()
            mousex, mousey = pygame.mouse.get_pos()

            (posx, posy) = chunk.get_pos()
            radius = chunk.get_radius()
            velocity = chunk.get_velocity()
            if posx < mousex - radius:
                # move right
                posx = min(BOARD_WIDTH, posx + velocity)
            elif posx > mousex + radius:
                # move left
                posx = max(0, posx - velocity)
            if posy > mousey + radius:
                # move down
                posy = max(0, posy - velocity)
            elif posy < mousey - radius:
                # move up
                posy = min(BOARD_HEIGHT, posy + velocity)

            chunk.set_pos(posx, posy) # TODO: might have to change once camera and perspective comes into play

            # Draw the game objects
            for _, object in objects_dict.items():
                # a check for seeing if that object is in the player's view or not goes here. maybe we do not need an explicit camera, we could calculate the render rectangle dynamically every time
                pygame.draw.circle(screen, object.get_color(), object.get_pos(), object.get_radius())

            # Draw the players
            for p in players.values():
                p_chunk = p.get_chunk()

                bg_circle = pygame.draw.circle(screen, p_chunk.get_color(), p_chunk.get_pos(), p_chunk.get_radius())

                shark_image = p.get_shark()

                # scale the shark image to the radius of the background circle
                scaled_shark = pygame.transform.scale(shark_image, (p_chunk.get_radius(), p_chunk.get_radius()))

                # blit the scaled shark image to be centered on the background circle
                screen.blit(scaled_shark, (bg_circle.centerx - scaled_shark.get_width() / 2, bg_circle.centery - scaled_shark.get_height() / 2))


            # render score UI
            text = font.render("Score: " + str(int(player.get_score())), True, (255, 0, 0))
            screen.blit(text, (30, 700))

            # render leaderboard
            loc = 20
            leader_txt = 'Leaderboard'
            text2 = font2.render(leader_txt, True, (255, 0, 0))
            screen.blit(text2, (1220, loc))

            players_list = list(players.values())
            players_list.sort(key=lambda x: x.get_score(), reverse=True)

            for player in players_list:
                loc = loc + 15
                leader_txt2 = str(player.get_name()) + ": " + str(int(player.get_score()))
                text3 = font2.render(leader_txt2, True, (255, 0, 0))
                screen.blit(text3, (1220, loc))

            # send the updated chunk data to the server.
            data = pickle.dumps(chunk)
            send_data(sock, data)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # TODO: send message to the server that I am disconnecting
                    running = False

    pygame.quit()


run_client()
