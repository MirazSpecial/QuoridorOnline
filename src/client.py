import pygame
import sys
from network import Network
from game import Game
from board import Board

def wait_for_game(net, board, pos_type = "null", pos = (0, 0)):
    game = net.send_recv_info(pos_type, pos)
    while type(game) != Game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("[QUITTING]")
                run = False
                pygame.quit()
        board.show_waiting(game)
        game = net.send_recv_info(pos_type, pos)
    return game

def main():
    ip = sys.argv[1]
    port = int(sys.argv[2])
    net = Network(ip, port)
    net.connect()
        
    if net.connected:
        player = int(net.recv())
        board = Board(864, 864)
        holding_pawn = False

        clock = pygame.time.Clock()

        run = True      
        while run:
            game = wait_for_game(net, board)

            mouse_pos = pygame.mouse.get_pos()
            pos_type, pos = board.check_mouse_pos(game, mouse_pos)
            game.highlight = pos_type, pos

            board.draw_game(game, player)

            if game.ended:
                board.show_winner(game)
                print("Game ended")
                pygame.time.delay(8000) 
                break

            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("[QUITTING]")
                    run = False
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_pos = event.__dict__["pos"]
                    pos_type, pos = board.check_mouse_pos(game, mouse_pos)
                    if board.undo_button.click(mouse_pos):
                        pos_type = "undo"
                    game = wait_for_game(net, board, pos_type, pos)


main()