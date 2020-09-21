#!/bin/bash

# Local ip address of the server (propably 192.168.x.xx)
ADDRESS=""

# Port on which server stands
PORT=5555


python3 src/client.py $ADDRESS $PORT
