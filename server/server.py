import socket
import threading
import sys
import json
import pickle
import time
import commands
from game.game import Game
from arena import Arena

FORMAT = "utf-8"
DATA_RECV_SIZE = 64
JSON_SEND_SIZE = 64

def performe_move(game, player, data):
    try:
        move_dict = json.loads(data)
    except json.decoder.JSONDecodeError as e:
        print(f"[SERVER] Error: corrupted json: {data}")
        return

    pos = tuple(move_dict["pos"])
    move_id = move_dict["id"]

    if move_id == "move":
        if game.move_if_possible(player, pos):
            print(f"[SERVER] Move by {player} was succesful")
        else:
            print(f"[SERVER] Move by {player} was not succesful")
    elif move_id in ("vert", "horiz"):
        if game.place_block(player, move_id, pos):
            print(f"[SERVER] Blocking by {player} was succesful")
        else:
            print(f"[SERVER] Blocking by {player} was not succesful")
    elif move_id == "undo":
        if game.move % 2 != player and len(game.moves) != 0:
            game.undo_move()
            print(f"[SERVER] Player {player} succesfully undo'd")
        else:
            print(f"[SERVER] Player {player} failed to undo")


def renew_arena(arena):
    print("[SERVER] Renewing arena")
    arena.new_game()
    arena.clients = []


def handle_game(connection, arena, player): 
    # It's important to give arena and not game
    while True:
        try:
            # sendall fixes many comunication problems
            connection.sendall(pickle.dumps(arena.game))

            data = connection.recv(DATA_RECV_SIZE).decode(FORMAT)
            if not data:
                break # Corrupted player message

            performe_move(arena.game, player, data)
            if arena.game.check_winner(player):
                arena.game.winner = player
                arena.game.ended = True
        except:
            print(f"[SERVER] Error: {sys.exc_info()[0]}")
            break


def handle_connection(connection, arena, new_id):
    client_id = connection.recv(DATA_RECV_SIZE).decode(FORMAT)
    client_dict = {}

    if not client_id:
        print("[SERVER] Connection not established")
        return

    client_id = client_id.rstrip()
    if client_id == "null":
        print(f"[SERVER] Setting new id: {new_id}")
        client_dict["id"] = str(new_id)
        client_id = str(new_id)

    player = arena.add_client(client_id, connection)

    if player == -1:
        renew_arena(arena)
        player = arena.add_client(client_id, connection)

    client_dict["player"] = player

    # Sending to client his information
    client_dict = json.dumps(client_dict)
    client_dict += " " * (JSON_SEND_SIZE - len(client_dict))
    connection.send(client_dict.encode(FORMAT))

    print(f"[SERVER] Arena clients: {len(arena.clients)}")
    handle_game(connection, arena, player)
        
    print("[SERVER] Connection ended")
    #arena.quit_arena(client_id)
    connection.close()
    

def bind(s, server_address):
    try:
        print("[SERVER] Binding...")
        s.bind(server_address)
        print("[SERVER] Server start")
    except socket.error as e:
        str(e)


def main():
    server_address = sys.argv[1], int(sys.argv[2])
    path_to_db = sys.argv[3]

    # Create and bind socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bind(s, server_address)
    s.listen()
    
    # Create game room
    arena = Arena()
    new_id = 1000 # id for first joining player

    # Start listening for commandscd
    thread = threading.Thread(target=commands.listen_for_commands,
                              args=(arena, path_to_db))
    thread.start()

    # Start accepting connections
    while True:
        conn, addr = s.accept()
        print(f"[SERVER] Connected to: {addr}")
        
        thread = threading.Thread(target=handle_connection, 
                                  args=(conn, arena, new_id))
        thread.start()

        new_id += 1


if __name__ == "__main__":
    main()