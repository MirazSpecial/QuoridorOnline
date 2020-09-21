import socket, pickle, json

class Network:
    FORMAT = "utf-8"

    def __init__(self, server, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        self.port = port
        self.addr = self.server, self.port
        self.connected = False

    def connect(self):
        try:
            self.client.connect(self.addr)
            self.connected = True
        except socket.error as e:
            print(f"[CONNECTION ERROR] Error: {e}")

    def send_recv(self, data):
        # data to string opisujący ruch
        try:
            self.client.send(data.encode(Network.FORMAT))
            return pickle.loads(self.client.recv(2048))
        except:
            pass

    def send_recv_info(self, move_type, move):
        move_json = json.dumps({"id": move_type, "pos": move})
        return self.send_recv(move_json)

    def recv(self):
        try:
            return self.client.recv(2048).decode(Network.FORMAT)
        except:
            print("[ERROR] Network error")