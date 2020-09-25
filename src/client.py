from game import Game
from network import Network
from board import Board
import pygame
import time
import json

class Client:
    def __init__(self, server_addr):
        self.server_addr = server_addr
        self.network = Network(server_addr[0], server_addr[1])
        self.client_id = "null"
        self.connected_to_game = False
        self.board = Board()


    def connect_to_game(self):
        self.network.connect()

        if not self.network.possible_to_connect:
            return # Server is unavailable

        self.network.send_text(self.client_id)

        info_dict = self.network.recv_json()

        if type(info_dict) != dict:
            return # Wrong info received
        
        if self.client_id == "null":
            self.client_id = info_dict["id"]

        self.player_number = info_dict["player"]


        if self.player_number != -1:
            print(f"Welcome client '{self.client_id}' You are player {self.player_number}")
            self.connected_to_game = True
        else:
            print("Can't connect to game. Game is full.")
            self.network.possible_to_connect = False # temporary solution


    def show_board(self):
        if not self.connected_to_game:
            return # Can't show board if client is not connected to game
        mouse_pos = pygame.mouse.get_pos()
        pos_type, pos = self.board.check_mouse_pos(self.game, mouse_pos)
        self.game.highlight = pos_type, pos
        self.board.draw_game(self.game, self.player_number)



    def end_game(self, game, board):
        board.show_winner(game)
        print("Game ended")
        pygame.time.delay(8000) 


    def check_pygame_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", (0, 0)
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = event.__dict__["pos"]
                if self.board.undo_button.click(mouse_pos):
                    return "undo", (0, 0)
                return self.board.check_mouse_pos(self.game, mouse_pos)
        return "null", (0, 0)


    def play(self):
        clock = pygame.time.Clock()
        
        while True:
            clock.tick(60)

            while not self.connected_to_game:
                if not self.network.possible_to_connect:
                    break # Connection is impossible
                print("Reconnecting...")
                self.connect_to_game()
                time.sleep(0.5)

            if not self.network.possible_to_connect:
                break # Connetion is impossible

            self.game = self.network.recv_game()

            if type(self.game) != Game: 
                self.connected_to_game = False
                continue # Need to reconnect

            self.show_board()

            if self.game.ended:
                self.end_game(self.game, self.board)
                break # Game ended

            move_type, move = self.check_pygame_events()

            if move_type == "quit":
                break # Player quit
            
            self.network.send_move(move_type, move)


        print("[QUITTING]")
        pygame.quit()