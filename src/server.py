# from a tutorial online:
# echo-server.py
import socket
import pickle
from player import Player

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65456  # Port to listen on (non-privileged ports are > 1023)

player = Player(name="Ankur", unique_id=1)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            # data = conn.recv(1024)
            # if not data:
            #     break
            conn.sendall(pickle.dumps(player))
    s.close()
'''
Connected by ('127.0.0.1', 58980)
Traceback (most recent call last):
  File "/Users/ellis/SharkIO/src/server.py", line 22, in <module>
    conn.sendall(b'hi')
BrokenPipeError: [Errno 32] Broken pipe
'''