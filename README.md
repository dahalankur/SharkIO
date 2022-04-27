# SharkIO
## Similar to Agar.io, but sharks! Implemented for CS21 at Tufts University

### What is it?
`SharkIO` is a multiplayer game where you take control of a shark and try to 
increase in size by eating food and other sharks that are smaller than you. 
Try to avoid the green viruses in the map, they will try to take your 
mass away!  

### How to play?
Ensure that you are running python version 3.9 or later. 
To create a python virtual environment and install required dependencies, 
run the setup script using `./setup.sh`. This script is present in the root 
directory of the project; make sure you execute it from the root directory.
> **_Note:_** If you see an error regarding installing the packages, you need 
> to manually install them by using `pip3 install -r requirements.txt`.

Once the required packages are installed, it is now time to run the game and 
try it yourself!

> **_Note:_** Since this game uses a client-server model, you need to connect 
> to a host running the server in order to join the lobby and start playing. 
> Open the `src/constants.py` file, and change the HOST constant to your 
> public ip if you want to play with other devices connected on the same 
> network. If you want to join as multiple players from your own laptop and 
> not from other systems, you can leave the HOST as localhost ("127.0.0.1"). 
> If any error related to "Address already in use" is seen, change the PORT 
> constant in the `src/constants.py file` and try running the server again.

To run the server, go to the root project directory and execute the server 
script using `./server.sh`. If there are no errors and you see a welcome 
message from pygame, you should be all set! Open up another terminal window 
and navigate to the project's root directory, and join the server as a shark 
by executing the play script: `./play.sh`. Try joining the server from 
multiple clients (but remember! They must have changed their HOST and 
PORT constants to match what the server has in order to connect successfully) 
and have fun!

The controls are simple: once you have entered the lobby and see your tiny 
shark floating in the sea, use [W A S D] keys to navigate around the map. 
That's it! If you prefer arrow keys to move, you can use them instead. 
The main thing is to enjoy the game and avoid being eaten....right?

### Description of folders and files in this project:
- `setup.sh`: A bash script that installs all required dependencies.
- `requirements.txt`: A text file listing python dependencies used by the 
  project.
- `server.sh`: A bash script that starts the server.
- `play.sh`: A bash script that joins the server and starts the game on the 
  cilent's side.
- `README.md`: README file for SharkIO; contains information about how to 
  play the game and other interesting details about the project files.
- `shark_images`: A directory containing eight shark images (pngs) that are 
  rendered on top of player blobs when they join the game.
- `src`: A directory that contains the python source files for SharkIO. 
  The following files are present:
  - Source files defining classes:
    - `chunk.py`: This file defines a `Chunk` class, which inherits from 
        the `GameObject` class (described below). Each player has its own 
        chunk, and the chunk stores data about the player's position, 
        current score, velocity, etc.
    - `player.py`: This file defines a `Player` class, an instance of which 
        represents a player and contains data about its avatar 
        (i.e., its shark image), and the chunk (instance of the `Chunk` class)
        associated with the player.
    - `gameobject.py`: This file defines a `GameObject` class, an instance of 
        which represents a drawable object that can either be a player's chunk
        (instance of the `Chunk` class), a virus, or a food. 
        It stores data about the game object, including their radius, color, 
        and their unique identifier.
    - `gameboard.py`: This file defines a `GameBoard` class, an instance of 
        which represents a game board. It stores data about the overall game 
        state, including the players (instances of the `Player` class) and 
        game objects (instances of the `GameObject` class of type food and 
        virus) present on the map and their locations.
  - Other source files that interact with the classes and help run the game:
    - `constants.py`: This file defines constants used throughout the project. 
        Source files that require certain constants will import them as 
        necessary from this file. Having a separate file for constants 
        ensures that we do not get multiple copies of constants that are 
        different from one another.
    - `server.py`: This file is mainly responsible for opening and listening 
        for connections actively on its main thread via websockets, and 
        spawning client threads once it detects that a client has asked to 
        join the server. One `GameBoard` instance is created and the game 
        begins: each client will have its own thread running 
        (until the client disconnects) which will perform collision detection 
        and update the gameboard state as necessary, and communicate the 
        changes to the state to the connected client via websockets.
    - `client.py`: This file is responsible for establishing a connection 
        to the server via websockets, receive the gameboard state data, 
        render the required output on the client's window using the pygame module 
        and communicate the player's position change to the server via websockets.
