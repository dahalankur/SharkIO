"""
server.py
Starts up a server for multiple clients to connect
"""
import socket
import pickle
from player import Player
from threading import Thread
from gameboard import Gameboard
from gameobject import GameObject



HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65456  # Port to listen on (non-privileged ports are > 1023)
BUFFER_SIZE = 1024

player = Player(name="Ankur", unique_id=1)

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            # TODO: spawn a thread for a player, and handle movements there, 
            # update gameboard, pickle data, and send it to the client for it to render

            while True:
                data = conn.recv(BUFFER_SIZE)
                if not data:
                    break
                conn.sendall(pickle.dumps(player))
    s.close()

def main():
    # Spawn a gameboard instance
    # Init the gameboard w/ default virus and food
    # Wait for connections
        # TODO: create a function that handles dynamic spawning of food and virus as time passes    
        # If its the first connection, start above function
        
        # Spawn a thread for each player that connects.
    
    gameboard = Gameboard()
    

if __name__ == "__main__":
    main()
