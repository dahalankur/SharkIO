#!/bin/bash
# setup.sh
# A shell script to run the game client

set -euo pipefail

echo "[*] Running the game client"
cd src && ../venv/bin/python3 client.py
