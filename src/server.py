"""
server.py
Starts up a server for multiple clients to connect
"""
import socket
import pickle
from constants import MAX_CONNECTIONS, HOST, PORT
from player import Player
from threading import Thread, Lock
from gameboard import GameBoard
from gameobject import GameObject
import time
import struct


def send_data(conn, data):
    """
    Given a socket and binary data, sends the data to the connections listening
    to that socket
    """
    bytes_size = len(data)
    packed_size_4_bytes = struct.pack('I', bytes_size)
    # send the size of the data as 4 bytes first, followed by the actual data
    conn.send(packed_size_4_bytes)
    conn.send(data)

def recv_data(conn):
    """
    Given a socket, receives and returns the binary data sent to the socket
    """
    # receive the size of the data first, followed by the actual data
    packed_size_4_bytes_data = conn.recv(4)
    bytes_size = struct.unpack('I', packed_size_4_bytes_data)
    packed_size_4_bytes = bytes_size[0]
    data = conn.recv(packed_size_4_bytes)
    return data
    

def main():
    """
    Defines methods to handle updates from clients and updates the 
    gameboard instance accordingly
    """
    state_lock = Lock()
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
            # main game loop that handles one client
            # Have thread sleep for a certain amount of time

            while True:
                serialized_data = pickle.dumps((gameboard.get_objects(), gameboard.get_players(), player))
                send_data(conn, serialized_data)
                
                data = recv_data(conn) # get the updated chunks dict for that player
                chunks = pickle.loads(data)
                for chunk in chunks.values():
                    # update player and gameboard chunks
                    player.add_chunk(chunk)     # local
                    gameboard.add_object(chunk) # threadsafe due to mutex.

                # TODO: collision detection and handling between players, player and food, player and virus
                with state_lock:
                    update_self_state(player)

                # when a client disconnects, break out of this loop, and
                # remove their game objects
                    
                

    
    def update_self_state(player):
        objects_array = list(gameboard.get_objects().values())
        for chunk in player.get_chunks().values():
            if chunk in objects_array:
                for other in objects_array:
                    # what about self comparison?
                    if other != chunk:
                        if chunk.is_colliding(other):
                            # player-player collision
                            if other.is_chunk():
                                print("colliding with another player")
                                # check the scores of the two players, remove the
                                # loser (J. Parsells, by class poll) lol
                                if player.get_radius() > other.get_radius(): 
                                    player.set_radius(player.get_radius() + other.get_radius())
                                    player.set_score(player.get_score() + other.get_score())
                                    gameboard.remove_object(other)
                                else:
                                    other.set_radius(player.get_radius() + other.get_radius())
                                    other.set_score(player.get_score() + other.get_score())
                                    # TODO: what if player has multiple chunks? CHANGE OF DESIGN: ONE CHUNK BABY, implement shooting mechanics
                                    # BANG BANG
                                    gameboard.remove_object(player)
                            elif other.is_virus():
                                print("colliding with a virus")
                                chunk.set_radius(chunk.get_radius() - (chunk.get_radius() / 2 - 4)) # reduce by 25% -4 
                                gameboard.remove_object(other)
                                # TODO: remove the virus as well
                            elif other.is_food():
                                print("colliding with food")
                                gameboard.remove_object(other)
                                player.set_score(player.get_score() +  1) 
                                chunk.increase_radius(1)
                                # this still works cause it 
                                # doesnt modify dict length chunk.
        
        
    
    
    # def update_gamestate():
    #     # FPS = 30
    #     # time.sleep(1 / 30) TODO: make it sleep for some arbritary time

    #     # player colliding with non-player objects
    #     for players in gameboard.get_objects():
            
            
    #         compare player ids, the one with the lower id HANDLES the collision.

    
    def listen_for_connections():
        """
        Opens a socket and listens for connections, no return or params
        """
        id = 0
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((HOST, PORT))
            sock.listen(MAX_CONNECTIONS)
            while True:
                # if id == 0:
                #     Thread(target=update_gamestate, args = ()).start()
                conn, addr = sock.accept()
                Thread(target=start_new_player, args=(conn, addr, id)).start()
                id += 1

    def startup():
        """
        Generates initial gameboard state and starts up a server that listens
        for connections
        """
        # Wait for connections
            # TODO: create a function that handles dynamic spawning of food and virus as time passes    
        gameboard.gen_init_state()
        listen_for_connections()
    
    gameboard = GameBoard()
    startup()
          


if __name__ == "__main__":
    main()
