# SharkIO
## Similar to Agar.io, but sharks! Implemented for CS21 Concurrency Course at Tufts University

### What is it?
`SharkIO` is a multiplayer game where you take control of a shark and try to increase in size by eating food and other sharks that are smaller than you. Try to avoid the green viruses in the map, they will try to take your mass away!  

### How to play?

Ensure that you are running python version 3.9 or later. To create a python virtual environment and install required dependencies, run the setup script using `./setup.sh`. This script is present in the root directory of the project; make sure you execute it from the root directory.
> **_Note:_** If you see an error regarding installing the packages, you need to manually install them by using `pip3 install -r requirements.txt`.

Once the required packages are installed, it is now time to run the game and try it for yourself!


> **_Note:_** Since this game uses a client-server model, you need to connect to a host running the server in order to join the lobby and start playing. Open the `src/constants.py` file, and change the HOST variable to your public ip if you want to play with other devices connected on the same network. If you want to join as multiple players from your own laptop and not from other systems, you can leave the HOST as localhost ("12.0.0.1"). If any error related to "Address already in use" is seen, change the PORT constant in the `src/constants.py file` and try running the server again.

To run the server, go to the root project directory and execute the server script using `./server.sh`. If there are no errrors and you see a welcome message from pygame, you should be all set! Open up another terminal window and navigate to the project's root directory, and join the server as a shark by executing the play script: `./play.sh`. Try joining the server from multiple clients (but remember! They must have changed their HOST and PORT constants to match what the server has in order to connect successfully) and have fun!

The controls are simple: once you have entered the lobby and see your tiny shark floating in the sea, use [W A S D] keys to navigate around the map. That's it! If you prefer arrow keys to move, you can use them instead. The main thing is to enjoy the game and avoid being eaten....right?


### A description of folders and files in this project:
- `setup.sh`: A bash script that installs all required dependencies.
- `requirements.txt`: A text file listing python dependencies used by the project.
- `server.sh`: A bash script that starts the server.
- `play.sh`: A bash script that joins the server and starts the game on the cilent's side.
- `README.md`: README file for SharkIO; contains information about how to play the game and other interesting details about the project files.
- `shark_images`: A directory containing nine shark images (pngs) that are rendered on top of player blobs when they join the game.
- `src`: A directory that contains the python source files for SharkIO. The following files are present:
  - Source files defining classes:
    - `gameboard.py`:
    - `gameobject.py`:
    - `player.py`:
    - `chunk.py`:
  - Other source files that interact with the classes and help run the game:
    - `constants.py`:
    - `server.py`:
    - `client.py`: