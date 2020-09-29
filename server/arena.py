from game.game import Game

class Arena:
    MAX_PLAYERS = 2 # Maybe 4 one day too.

    def __init__(self):
        self.new_game()
        self.clients = [] # format [(id, connection, player_number), ...]


    def add_client(self, client_id, connection):
        """ Adds a new client to the arena and returns his
        game number, or -1 when no new clients can be added. """

        free_player = self.find_free_player()
        print(free_player)
        for i in range(len(self.clients)):
            if client_id == self.clients[i][0]:
                self.clients[i] = client_id, connection, free_player 
                print("Old client connected")
                return free_player
        if len(self.clients) < Arena.MAX_PLAYERS:
            print("New client connected")
            self.clients.append((client_id, connection, free_player))
            return free_player
        print("Could not connect player")
        return -1


    def new_game(self):
        self.game = Game()


    def quit_arena(self, client_id):
        for i in range(len(self.clients)):
            if self.clients[i][0] == client_id:
                self.clients.pop(i)
                return

            
    def find_free_player(self):
        players = []
        for client in self.clients:
            players.append(client[2])
        players.sort()
        for i in range(Arena.MAX_PLAYERS):
            if i not in players:
                return i