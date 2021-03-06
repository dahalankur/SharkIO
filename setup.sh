#!/bin/bash
# setup.sh
# A shell script to set up a python virtual environment, install all the 
# package dependencies, and potentially run the game client

set -euo pipefail

echo "[*] Setting up the python virtual environment"
python3 -m venv venv

# install required packages
# Note: venv/bin/pip installs the packages inside the venv directory, thus 
#       not touching the global python environment set up in the machine
echo "[*] Installing required packages"
venv/bin/pip install -r requirements.txt > /dev/null

echo "[√] Done!"

echo "Run the server by executing the server.sh script"
echo "After the server is up and running, you can join the server and start playing by executing the play.sh script! Have fun!"
