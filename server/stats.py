import threading
import copy
import data
from game.game import Game
from arena import Arena


def add_game_to_db(conn, c, original_game, winner):
    game = copy.deepcopy(original_game)

    not_beginning = True
    while not_beginning:
        game_json = game.json_description()
        data.add_game_occurence(conn, c, game_json, winner)

        not_beginning = game.undo_move()


def show_game_stats(conn, c, game):
    game_json = game.json_description()
    occurences, p1_wins = data.check_game_stats(conn, c, game_json)
    if occurences == 0:
        print("[GAME STATS] This is a new game")
    else:
        print(f"[GAME STATS] This game was played {occurences} times.", end='')
        print(f"Player 1 win ratio is {p1_wins / occurences}")