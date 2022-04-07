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

# player = Player(name="Ankur", unique_id=1)
def simple_thread_func(conn, addr, id):
    with conn:
        print(f"Connected by {addr} with id {id}")
        # update gameboard, pickle data, and send it to the client for it to render

        # main game loop that handles one client
        # Have thread sleep for a certain amount of time
        while True:
            time.sleep(10)
            print(f"Connection still alive {id}")

def open_connection_socket():
    """
    Opens a socket and listens for connections, no return or params
    """
    id = 0
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    print("Effective, Power: لُلُصّبُلُلصّبُررً ॣ ॣh ॣ ॣ冗")
    sock.bind((HOST, PORT))
    print("Line 38")
    sock.listen(MAX_CONNECTIONS)
    print("Line 40")
    while True:
        print("Line 42")
        conn, addr = sock.accept()
        print("Starting thread")
        Thread(target=simple_thread_func, args=(conn, addr, id)).start()
        id += 1
        print("Completed while true body, line 47")
    sock.close()

def main():
    # Wait for connections
        # TODO: create a function that handles dynamic spawning of food and virus as time passes    
        # If its the first connection, start above function
        
        # Spawn a thread for each player that connects.
    
    gameboard = GameBoard()
    gameboard.gen_init_state()
    open_connection_socket()
    

    

if __name__ == "__main__":
    main()
