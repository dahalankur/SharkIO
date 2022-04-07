# echo-client.py

import socket
import pickle
from player import Player

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65456  # The port used by the server
BUFFERSIZE = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    # s.send()
    data = s.recv(BUFFERSIZE)

player = pickle.loads(data)
print(f"Received {player.get_name()}")

'''Traceback (most recent call last):
  File "/Users/ellis/SharkIO/src/client.py", line 16, in <module>
    player = pickle.load(data)
TypeError: file must have 'read' and 'readline' attributes'''