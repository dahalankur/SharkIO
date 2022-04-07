# testing stuff here

# imports
import pickle
import sys
import socket

# import player from player class
from player import Player

socket.setdefaulttimeout(5) # set a default timeout so if no response is,
                            # received the program doesn't hang

p1 = Player(name="A", unique_id=1)

output_file_name = "outfile"
if (len(sys.argv)) > 1:
    with open (output_file_name, "wb") as output_file:
        pickle.dump(p1, output_file)
    
    print("Complete write")
else:
    with open(output_file_name, "rb") as output_file:
        player_recreated = pickle.load(output_file)
        print(player_recreated.get_name())
        print(player_recreated.get_id())
        print("Complete read")