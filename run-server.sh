#!/bin/bash
# run-server.sh
# --starfront-- server
# make sure you run the command:
# chmod +x "run-server.sh"
virtualenv -p python3 .venv 
source .venv/bin/activate 
pip install -r requirements.txt
ENV=dev TEST=true python3 app.py
