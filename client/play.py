import sys
from client import Client


def main():
    server_addr = sys.argv[1], int(sys.argv[2])

    client = Client(server_addr)   
    client.play() 

main()