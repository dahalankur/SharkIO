"""
server.py
Starts up a server for multiple clients to connect
"""
import socket
import pickle
from constants import *
from player import Player
from threading import Thread, Lock
from gameboard import GameBoard
from gameobject import GameObject
import time
import uuid
from random import randint
import struct

# Note: the send_data, recv_data, and recvall methods were inspired by the 
# post on stackoverflow. The posts are cited in our notes/bugs.txt file 
def send_data(conn, data):
    """
    Given a socket and binary data, sends the data to the connections listening
    to that socket
    """
    data = struct.pack('>I', len(data)) + data
    conn.sendall(data)

def recv_data(sock):
    # Read message length and unpack it into an integer
    data_len = recvall(sock, 4)
    if not data_len:
        return None
    msglen = struct.unpack('>I', data_len)[0]
    # Read the message data
    return recvall(sock, msglen)

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data
# end section borrowed from stackoverflow


def main():
    """
    Defines methods to handle updates from clients and updates the 
    gameboard instance accordingly
    """
    def start_new_player(conn, addr, id):
        """
        Given the socket connection, address, and player id, instantiates
        a player instance and communicates with the connected client any change
        in the player's state and updates the gameboard as required
        """

        player = Player(name=id, unique_id=id)
        gameboard.add_player(player)

        with conn:
            print(f"Connected by {addr} with id {id}")
            
            # get player's name
            name = recv_data(conn)
            if name:
                player.set_name(name.decode('utf-8'))

            while True:
                time.sleep(0.04)
                try:
                    
                    with state_lock:
                        # get local object data 
                        serialized_data = pickle.dumps((gameboard.get_objects_for_player(id), gameboard.get_players(), gameboard.get_player(id)))
                        # serialized_data = pickle.dumps((gameboard.get_objects(), gameboard.get_players(), gameboard.get_player(id)))
                    send_data(conn, serialized_data)
                
                    data = recv_data(conn)
                    if not data:
                        continue
                    chunk = pickle.loads(data) # receive updated chunk from client
                    if not chunk:
                        continue
                    gameboard.get_player(id).set_chunk(chunk)
                    
                    # Functions handle dataraces
                    check_player_collisions()
                    check_other_collisions(gameboard.get_player(id))
                except KeyError:
                    # means the player died because gameboard.get_player(id) will crash, so respawn
                    # create a new player with the same id
                    time.sleep(2)
                    player = Player(name=name.decode('utf-8'), unique_id=id)
                    gameboard.add_player(player)
                except BrokenPipeError:
                    # TODO: look at removing player from gameboard if they still exist at this point
                    break
                except ConnectionResetError:
                    # TODO: look at removing player from gameboard if they still exist at this point
                    break
            print(f"Player disconnected with id {id}")
                    

    def check_player_collisions():
        """
        Given a list of players, checks if any players are colliding and if 
        they are, kills the player with the lower score
        """
        players_sorted_by_score = sorted(gameboard.get_players().values(), key=lambda p: p.get_score())
        for i, p1 in enumerate(players_sorted_by_score):
            for p2 in players_sorted_by_score[i + 1:]:
                # invariant: p2 always has higher score than p1
                p1_chunk = p1.get_chunk()
                p2_chunk = p2.get_chunk()
                with state_lock:
                    if p1_chunk.is_colliding(p2_chunk):
                        # kill p1
                        p2_chunk.increase_radius(p1_chunk.get_radius())
                        gameboard.get_players()[p2.get_id()] = p2
                        gameboard.remove_player(p1)

    
    def check_other_collisions(player):
        """
        Given the player, checks if the player collides with other game objects
        in the gameboard and takes necessary action
        """
        objects_array = list(gameboard.get_objects().values())
        chunk = player.get_chunk()
        for other in objects_array:            
            if chunk.is_colliding(other):
                if other.is_virus():
                    size_change = (chunk.get_radius() / 2) - 2
                    if (chunk.get_radius() - size_change) > PLAYER_MINIMUM_RADIUS:

                        chunk.set_radius(chunk.get_radius() - size_change) # reduce by 25% -4 
                    else: # set to minimum size
                        chunk.set_radius(PLAYER_MINIMUM_RADIUS)
        
                    gameboard.remove_object(other)
                elif other.is_food():
                    gameboard.remove_object(other)
                    chunk.increase_radius(2)

    
    def listen_for_connections():
        """
        Opens a socket and listens for connections, no return or params
        """
        id = 0
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((HOST, PORT))
            sock.listen(MAX_CONNECTIONS)
            while True:
                conn, addr = sock.accept()
                Thread(target=start_new_player, args=(conn, addr, id)).start()
                id += 1


    def begin_object_generation():
        iterations = 1
        while True:
            num_players = len(gameboard.get_players().keys())
            num_food = 0
            for object in gameboard.get_objects().values():
                if object.is_food():
                    num_food += 1
            
            num_virus = len(gameboard.get_objects()) - num_food
            
            with state_lock:
                if len(gameboard.get_objects()) < MAX_GAME_OBJECTS:
                    iterations += 1 
                    if num_food < MAX_FOOD_IN_GAME:
                        for _ in range(num_players):
                            gameboard.add_object(GameObject(randint(0, gameboard.get_width()), 
                                                    randint(0, gameboard.get_height()),
                                                    FOOD_RADIUS, BLUE, 'food', uuid.uuid4()))
                    if num_virus < MAX_VIRUS_IN_GAME:
                        if iterations % FOOD_GENERATION_ITERATIONS == 0:
                            virus_radius = randint(VIRUS_RADIUS_MIN, VIRUS_RADIUS_MAX)
                            gameboard.add_object(GameObject(randint(0, gameboard.get_width()), 
                                                    randint(0, gameboard.get_height()),
                                                    virus_radius, GREEN, 'virus', uuid.uuid4()))
            time.sleep(FOOD_GENERATION_TIME)

    def startup():
        """
        Generates initial gameboard state and starts up a server that listens
        for connections
        """
        Thread(target= begin_object_generation, args = ()).start() 
        gameboard.gen_init_state()
        listen_for_connections()
    
    state_lock = Lock()
    gameboard = GameBoard()
    startup()
          

if __name__ == "__main__":
    main()
