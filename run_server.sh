#!/bin/bash

# Local ip address of the server (propably 192.168.x.xx)
ADDRESS=""

# Port on which server will stand (5555 should be)
PORT=5555


python3 src/server.py $ADDRESS $PORT
