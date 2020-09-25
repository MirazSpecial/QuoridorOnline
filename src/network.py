import socket, pickle, json, time, sys

class Network:
    FORMAT = "utf-8"
    JSON_RECV_SIZE = 64
    DATA_SEND_SIZE = 64
    GAME_RECV_SIZE = 2048

    def __init__(self, server, port):
        self.server_addr = server, port
        self.possible_to_connect = True

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect(self.server_addr)
            print(f"Connection started with {self.server_addr}")
        except:
            self.possible_to_connect = False
            print("[ERROR] Impossible to connect.")

    def send_text(self, text):
        try:
            text += ' ' * (Network.DATA_SEND_SIZE - len(text))
            self.socket.send(text.encode(Network.FORMAT))
        except:
            print(f"[ERROR] Data sending error: {sys.exc_info()[0]}")

    def recv_game(self):
        try:
            return pickle.loads(self.socket.recv(Network.GAME_RECV_SIZE))
        except:
            print(f"[ERROR] Game receiving error: {sys.exc_info()[0]}")


    def recv_json(self):
        try: 
            text = self.socket.recv(Network.JSON_RECV_SIZE).decode(Network.FORMAT)
            return json.loads(text)
        except:
            print(f"[ERROR] Json reciving error: {sys.exc_info()[1]}")


    def send_move(self, move_type, move):
        move_json = json.dumps({"id": move_type, "pos": move})
        self.send_text(move_json)
