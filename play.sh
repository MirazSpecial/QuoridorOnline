#!/bin/bash

# Local ip address of the server (propably 192.168.x.xx)
ADDRESS="192.168.0.59"

# Port on which server stands
PORT=5555


python3 client/play.py $ADDRESS $PORT
