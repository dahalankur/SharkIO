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
                serialized_data = pickle.dumps((gameboard.get_objects(), player))
                send_data(conn, serialized_data)
                
                data = recv_data(conn) # get the updated chunks dict for that player
                chunks = pickle.loads(data)
                for chunk in chunks.values():
                    # update player and gameboard chunks
                    player.add_chunk(chunk)
                    gameboard.add_object(chunk)
    
                


                # TODO: collision detection and handling between players, player and food, player and virus
            
                time.sleep(0.002)
                # TODO: when a client disconnects, break out of this loop, and
                # remove their game objects.
            
    
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
