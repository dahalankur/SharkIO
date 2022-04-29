#!/bin/bash
# setup.sh
# A shell script to run the server

set -euo pipefail

echo "[*] Running the game server"
cd src && ../venv/bin/python3 server.py
