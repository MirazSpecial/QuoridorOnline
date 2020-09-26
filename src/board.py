import pygame
import math
from game import Game
from button import Button
from pygame import gfxdraw

class Board:
    GAME_NAME = "QuoridorOnline"
    LINE_COLOR = 204,204,204,255
    FIELDS_COLOR = 227,227,227,255
    PLAYER1_COLOR = 104,34,139,255
    PLAYER2_COLOR = 205,91,69,255
    BLOCK_COLOR = 71,71,71,255
    HIGHLIGHTED_FIELD_COLOR = 255,255,255,255
    HIGHLIGHTED_BLOCK_COLOR = 151,151,151,255
    END_TEXT_COLOR = 128,128,128,255
    INFO_BOX_SIZE = 50
    INFO_TEXT_SIZE = 30
    BUTTON_TEXT_SIZE = 45
    BUTTON_WIDTH = 100 
    BUTTON_HEIGHT = 40

    def __init__(self, width = 864, height = 864, prec = 8):
        self.width = width
        self.height = height
        self.prec = prec # Field would be (prec - 2) / prec size of grid size

        pygame.init()
        self.win = pygame.display.set_mode((width, height + Board.INFO_BOX_SIZE))
        pygame.display.set_caption(Board.GAME_NAME)

        button_x = self.width // 2 - Board.BUTTON_WIDTH // 2
        button_y = self.height + Board.INFO_BOX_SIZE // 2 - Board.BUTTON_HEIGHT // 2
        self.undo_button = Button("Undo", Board.BUTTON_TEXT_SIZE, button_x, button_y, Board.BUTTON_WIDTH, Board.BUTTON_HEIGHT)

    
    def set_drawing_variables(self, game):
        # Grid and precise grid sizes
        self.grid_width = self.width // game.width
        self.grid_height = self.height // game.height
        self.prec_grid_width = self.width // (game.width * self.prec)
        self.prec_grid_height = self.height // (game.height * self.prec)
        self.field_size = self.grid_width - 2 * self.prec_grid_width, self.grid_height - 2 * self.prec_grid_height
        
        # Players pawns
        self.p1_x = game.players_pos[0][0] * self.grid_width + self.grid_width // 2
        self.p1_y = game.players_pos[0][1] * self.grid_height + self.grid_height // 2
        self.p2_x = game.players_pos[1][0] * self.grid_width + self.grid_width // 2
        self.p2_y = game.players_pos[1][1] * self.grid_height + self.grid_height // 2
        self.player_radius = min(self.grid_width, self.grid_height) // 3
        

    def draw_game(self, game, player):
        # Setting variables
        self.set_drawing_variables(game)

        # Drawing background
        pygame.draw.rect(self.win, Board.LINE_COLOR, (0, 0, self.width, self.height))
        
        # Drawing fields
        for i in range(game.height):
            for j in range(game.width):
                field_pos = j * self.grid_width + self.prec_grid_width, i * self.grid_height + self.prec_grid_height
                pygame.draw.rect(self.win, Board.FIELDS_COLOR, field_pos + self.field_size)

        # Drawing highlighted spot
        if "highlight" in game.__dict__:
            h_type, h_pos = game.highlight
            if h_type == "move" and game.check_move(player, h_pos):
                field_pos = self.grid_width * h_pos[0] + self.prec_grid_width, self.grid_height * h_pos[1] + self.prec_grid_height
                pygame.draw.rect(self.win, Board.HIGHLIGHTED_FIELD_COLOR, field_pos + self.field_size)
            elif h_type == "vert" and game.blocks_left[player] > 0:
                if game.check_block("vert", h_pos):
                    block_pos = self.grid_width * (h_pos[0] + 1) - self.prec_grid_width, self.grid_height * h_pos[1] + self.prec_grid_height
                    block_size = 2 * self.prec_grid_width, 2 * self.grid_height - 2 * self.prec_grid_height
                    pygame.draw.rect(self.win, Board.HIGHLIGHTED_BLOCK_COLOR, block_pos + block_size)
                elif game.check_block("vert", (h_pos[0], h_pos[1] - 1)):
                    block_pos = self.grid_width * (h_pos[0] + 1) - self.prec_grid_width, self.grid_height * (h_pos[1] - 1) + self.prec_grid_height
                    block_size = 2 * self.prec_grid_width, 2 * self.grid_height - 2 * self.prec_grid_height
                    pygame.draw.rect(self.win, Board.HIGHLIGHTED_BLOCK_COLOR, block_pos + block_size)     
            elif h_type == "horiz" and game.blocks_left[player] > 0:
                if game.check_block("horiz", h_pos):
                    block_pos = self.grid_width * h_pos[0] + self.prec_grid_width, self.grid_height * (h_pos[1] + 1) - self.prec_grid_height
                    block_size = 2 * self.grid_width - 2 * self.prec_grid_width, 2 * self.prec_grid_height
                    pygame.draw.rect(self.win, Board.HIGHLIGHTED_BLOCK_COLOR, block_pos + block_size)
                elif game.check_block("horiz", (h_pos[0] - 1, h_pos[1])):
                    block_pos = self.grid_width * (h_pos[0] - 1) + self.prec_grid_width, self.grid_height * (h_pos[1] + 1) - self.prec_grid_height
                    block_size = 2 * self.grid_width - 2 * self.prec_grid_width, 2 * self.prec_grid_height
                    pygame.draw.rect(self.win, Board.HIGHLIGHTED_BLOCK_COLOR, block_pos + block_size)

        # Drawing blocks
        for pos in game.blocks:
            block_type = game.blocks[pos]
            if block_type == "null":
                continue
            elif block_type == "vert":
                block_pos = self.grid_width * (pos[0] + 1) - self.prec_grid_width, self.grid_height * pos[1] + self.prec_grid_height
                block_size = 2 * self.prec_grid_width, 2 * self.grid_height - 2 * self.prec_grid_height
            elif block_type == "horiz":
                block_pos = self.grid_width * pos[0] + self.prec_grid_width, self.grid_height * (pos[1] + 1) - self.prec_grid_height
                block_size = 2 * self.grid_width - 2 * self.prec_grid_width, 2 * self.prec_grid_height
            pygame.draw.rect(self.win, Board.BLOCK_COLOR, block_pos + block_size)

        # Drawing players (antialiased)
        gfxdraw.aacircle(self.win, self.p1_x, self.p1_y, self.player_radius, Board.PLAYER1_COLOR)
        gfxdraw.filled_circle(self.win, self.p1_x, self.p1_y, self.player_radius, Board.PLAYER1_COLOR)
        gfxdraw.aacircle(self.win, self.p2_x, self.p2_y, self.player_radius, Board.PLAYER2_COLOR)
        gfxdraw.filled_circle(self.win, self.p2_x, self.p2_y, self.player_radius, Board.PLAYER2_COLOR)

        # Bliting info text
        self.print_info(game)

        # Drawing undo button
        self.undo_button.draw(self.win)

        # Updating display
        pygame.display.update()


    def check_mouse_pos(self, game, mouse_pos):
        """ Checks if mouse points on field or block, returns
        what mouse points on and it's position. """

        # Setting lengths
        self.set_drawing_variables(game)
        prec_grid_x = mouse_pos[0] // self.prec_grid_width
        prec_grid_y = mouse_pos[1] // self.prec_grid_height
        x_rem = prec_grid_x % self.prec
        y_rem = prec_grid_y % self.prec

        pos_type = "null"
        vert_pos, horiz_pos = 0, 0

        # Checking vertical space between fields
        if x_rem in (0, self.prec - 1) and y_rem not in (0, self.prec - 1):
            pos_type = "vert"
            vert_pos = (prec_grid_x + 1) // self.prec - 1
            horiz_pos = prec_grid_y // self.prec

        # Checking horizontal space between fields
        if x_rem not in (0, self.prec - 1) and y_rem in (0, self.prec - 1):
            pos_type = "horiz"
            vert_pos = prec_grid_x // self.prec
            horiz_pos = (prec_grid_y + 1) // self.prec - 1

        # Checking field
        if x_rem not in (0, self.prec - 1) and y_rem not in (0, self.prec - 1):
            pos_type = "move"
            vert_pos = prec_grid_x // self.prec
            horiz_pos = prec_grid_y // self.prec

        return pos_type, (vert_pos, horiz_pos)


    def print_info(self, game):
        pygame.draw.rect(self.win, Board.FIELDS_COLOR, (0, self.height, self.width, Board.INFO_BOX_SIZE))

        font = pygame.font.SysFont("comicsans", Board.INFO_TEXT_SIZE)
        text_left_1 = f" Distance to endline: {game.check_dist(0, game.height - 1)}"
        text_left_2 = f" Remaining blocks: {game.blocks_left[0]}"
        text_right_1 = f"Distance to endline: {game.check_dist(1, 0)} "
        text_right_2 = f"Remaining blocks: {game.blocks_left[1]} "
        
        text_left_1_renderd = font.render(text_left_1, 1, Board.PLAYER1_COLOR)
        text_left_2_renderd = font.render(text_left_2, 1, Board.PLAYER1_COLOR)
        text_right_1_renderd = font.render(text_right_1, 1, Board.PLAYER2_COLOR)
        text_right_2_renderd = font.render(text_right_2, 1, Board.PLAYER2_COLOR)

        self.win.blit(text_left_1_renderd, (0, self.height))
        self.win.blit(text_left_2_renderd, (0, self.height + font.size(text_left_1)[1]))
        self.win.blit(text_right_1_renderd, (self.width - font.size(text_right_1)[0], self.height))
        self.win.blit(text_right_2_renderd, (self.width - font.size(text_right_2)[0], self.height + font.size(text_right_1)[1]))


    def show_waiting(self, game):
        font = pygame.font.SysFont("comicsans", 80)
        text = "Waiting for connection..."
        text_renderd = font.render(text, 1, Board.END_TEXT_COLOR)
        self.win.blit(text_renderd, (self.width // 2 - font.size(text)[0] // 2, self.height // 2))
        pygame.display.update()


    def show_winner(self, game):
        font = pygame.font.SysFont("comicsans", 80)
        end_text = f"Player {game.winner + 1} won"
        end_text_renderd = font.render(end_text, 1, Board.END_TEXT_COLOR)
        self.win.blit(end_text_renderd, (self.width // 2 - font.size(end_text)[0] // 2, self.height // 2))
        pygame.display.update()

