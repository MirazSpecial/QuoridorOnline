import socket
import threading
import sys
import json
from game import Game
import pickle
import time

FORMAT = "utf-8"

def handle_client(conn, game, player, activePlayers):
    run = True
    try:
        conn.send(str(player).encode(FORMAT))
    except:
        print(f"[ERROR] Error: {sys.exc_info()[0]}")
        run = False

    while run:
        try:
            data = conn.recv(2048).decode(FORMAT) # ile bitów przyjmiemy

            if not data:
                print("Disconnected")
                break
            
            data = json.loads(data)
            data["old_pos"] = game.players_pos[player]
            pos = tuple(data["pos"])

            if data["id"] == "move":
                if game.move_if_possible(player, pos):
                    game.moves.append(data)
                    print(f"Move by {player} was succesful")
                else:
                    print(f"Move by {player} was not succesful")
            elif data["id"] in ("vert", "horiz"):
                if game.place_block(player, data["id"], pos):
                    game.moves.append(data)
                    print(f"Blocking by {player} was succesful")
                else:
                    print(f"Blocking by {player} was not succesful")
            elif data["id"] == "undo":
                if game.move % 2 != player:
                    game.undo_move()

            conn.sendall(pickle.dumps(game))
            
            if game.check_winner(player):
                game.winner = player
                game.ended = True

        except:
            print(f"[ERROR] Error: {sys.exc_info()[0]}")
            run = False

    print("Connection lost")
    conn.close()
    activePlayers[player] = False


def bind(s, server, port):
    try:
        print("[BINDING]")
        s.bind((server, port))
        print("[SERVER STARTED]")
    except socket.error as e:
        str(e)


def free(tab):
    for i in range(len(tab)):
        if not tab[i]:
            return i
    return -1


def main():
    server = sys.argv[1]
    port = int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bind(s, server, port)
    s.listen()
    
    freeSpot = 0
    activePlayers = [False, False]
    game = Game()

    while True:
        freeSpot = free(activePlayers)
        if freeSpot == -1:
            time.sleep(1)
            continue
        else:
            activePlayers[freeSpot] = True

            conn, addr = s.accept()
            print(f"[CONNECTED] Connected to: {addr}")

            thread = threading.Thread(target=handle_client, args=(conn, game, freeSpot, activePlayers))
            thread.start()


main()