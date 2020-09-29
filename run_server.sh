#!/bin/bash

# Local ip address of the server (propably 192.168.x.xx)
ADDRESS="192.168.0.59"

# Port on which server will stand (5555 should be)
PORT=5555

# Path to database where played games are stored
DB="server/databases/game.db"

python3 server/server.py $ADDRESS $PORT $DB
