"""
server.py
Starts up a server for multiple clients to connect
"""
import socket
import pickle
from constants import MAX_CONNECTIONS
from player import Player
from threading import Thread, Lock
from gameboard import GameBoard
from gameobject import GameObject
import time


HOST = "127.0.0.1"  # localhost
PORT = 64429  # any port, arbitrarily picked
BUFFER_SIZE = 1024


def main():
    # player = Player(name="Ankur", unique_id=1)
    def start_new_player(conn, addr, id):
        player = Player(name=id, unique_id=id)
        gameboard.add_player(player)
        with conn:
            print(f"Connected by {addr} with id {id}")
            # update gameboard, pickle data, and send it to the client for it to render
            # main game loop that handles one client
            # Have thread sleep for a certain amount of time

            while True:
                time.sleep(10)
                print(f"Connection still alive {id}")

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
        # Wait for connections
            # TODO: create a function that handles dynamic spawning of food and virus as time passes    
            # If its the first connection, start above function
            
            # Spawn a thread for each player that connects.
        gameboard.gen_init_state()
        listen_for_connections()
    


    gameboard = GameBoard()
    startup()  
          

        

if __name__ == "__main__":
    main()
