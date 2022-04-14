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
        nonlocal players, gameboard

        player = Player(name=id, unique_id=id)
        gameboard.add_player(player)

        with conn:
            print(f"Connected by {addr} with id {id}")
            
            # get player's name
            data = recv_data(conn)
            if data:
                player.set_name(data.decode('utf-8'))

            while True:
                serialized_data = pickle.dumps((gameboard.get_objects(), players, gameboard.get_player(id)))
                send_data(conn, serialized_data)
                
                try:
                    data = recv_data(conn)
                    chunk = pickle.loads(data) # receive updated chunk from client
                    gameboard.get_player(id).set_chunk(chunk)
                    
                    with state_lock:        
                        check_player_collisions()
                        check_other_collisions(gameboard.get_player(id))
                except KeyError:
                    # means the player died because gameboard.get_player(id) will crash, so exit gracefully
                    send_data(conn, b"disconnect")
                    break
                # TODO: find out when client disconnects and exit out this loop
            print(f"Player disconnected with id {id}")
                    

    def check_player_collisions():
        """
        Given a list of players, checks if any players are colliding and if 
        they are, kills the player with the lower score
        """
        nonlocal players, gameboard
        players_sorted_by_score = sorted(players.values(), key=lambda p: p.get_score())
        for i, p1 in enumerate(players_sorted_by_score):
            for p2 in players_sorted_by_score[i + 1:]:
                # invariant: p2 always has higher score than p1
                p1_chunk = p1.get_chunk()
                p2_chunk = p2.get_chunk()
                if p1_chunk.is_colliding(p2_chunk):
                    # kill p1
                    # print(f"Before death of p1, p2's score is {p2.get_score()} and radius is {p2_chunk.get_radius()}")
                    p2_chunk.increase_radius(p1_chunk.get_radius())
                    p2_chunk.set_score(p2_chunk.get_score() + p1_chunk.get_score())
                    p2.set_chunk(p2_chunk)
                    players[p2.get_id()] = p2
                    # p2_chunk.set_radius(10) THIS WORKS BUT THE ONE BELOW DOES NOT. WHY???!?!?!?!?!?
                    # p2_chunk.increase_radius(p1_chunk.get_radius())
                    # p1_chunk.set_score(0)
                    # p1_chunk.set_pos(0, 0)
                    # p1_score = p1.get_score()
                    # p2_score = p2.get_score()
                    # p2_chunk.set_score(p1_score + p2_score)

                    # p1_chunk.set_pos(0, 0)

                    # observation: as long as p1 is not removed, it looks like it works. I confirm that it does work if player is not removed
                    gameboard.remove_player(p1)
                    # print(f"After death of p1, p2's score is {p2.get_score()} and radius is {p2_chunk.get_radius()}")
                    # print(f"According to the gameboard, p2's score is {gameboard.get_player(p2.get_id()).get_score()}")
                    # for some reason, this does not update when player is smaller than another player and is eaten -- the bigger player does not gain score or radius

    
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
                    size_change = (chunk.get_radius() / 2) - 4
                    chunk.set_radius(chunk.get_radius() - size_change) # reduce by 25% -4 
                    chunk.set_score(chunk.get_score() - size_change)
                    gameboard.remove_object(other)
                elif other.is_food():
                    gameboard.remove_object(other)
                    chunk.set_score(chunk.get_score() + 2) 
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

    def startup():
        """
        Generates initial gameboard state and starts up a server that listens
        for connections
        """
        # TODO: create a function that handles dynamic spawning of food and virus as time passes    
        gameboard.gen_init_state()
        listen_for_connections()
    
    state_lock = Lock()
    gameboard = GameBoard()
    players = gameboard.get_players()
    startup()
          


if __name__ == "__main__":
    main()
