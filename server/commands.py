import data
import stats
from arena import Arena
from game.game import Game


def listen_for_commands(arena, path_to_db):
    conn, c = data.connect_to_database(path_to_db)
    game_table_exist = data.check_table_existance(conn, c)
    if not game_table_exist:
        data.create_table(conn, c)

    while True: 
        command = input()
        if command == 'add':
            print('[STATS] Which player wins the game (options: 0, 1): ', end='')
            winner = input()
            if winner in ('0', '1'):
                stats.add_game_to_db(conn, c, arena.game, int(winner))
                print('[STATS] Game added successfully')
            else:
                print('[STATS] Wrong player number')
        elif command == 'check':
            stats.show_game_stats(conn, c, arena.game)
        elif command == 'reset_stats':
            print("[STATS] Do You really want to reset ALL stats (options: yes, no): ", end='')
            decision = input()
            if decision == 'yes':
                data.delete_table(conn, c)
                data.create_table(conn, c)
            else:
                print('[STATS] Operation aborted')
        elif command == 'exit':
            break
        else:
            print("[STATS] Wrong command")

    data.close_connection(conn)
    print("[STATS] Thread closing")
