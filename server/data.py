import sqlite3

def connect_to_database(path_to_db):
    conn = sqlite3.connect(path_to_db)
    c = conn.cursor()
    return conn, c


def create_table(conn, c):
    c.execute("""CREATE TABLE games(
                 game_json JSON,
                 num_occ INTEGER,
                 p1_wins INTEGER
                 )""")


def check_table_existance(conn, c):
    c.execute("""SELECT name FROM sqlite_master 
                 WHERE type = 'table' AND name = 'games'""")
    res = c.fetchall()
    if len(res) == 0:
        return False
    return True


def delete_table(conn, c):
    c.execute("DROP TABLE games")


def insert_new_game(conn, c, game_json, winner):
    with conn:
        if winner == 0:
            p1_wins = 1
        else:
            p1_wins = 0
        c.execute("INSERT INTO games VALUES (:game_json, 1, :p1_wins)",
                  {'game_json': game_json, 'p1_wins': p1_wins})


def add_game_occurence(conn, c, game_json, winner):
    c.execute("SELECT num_occ, p1_wins FROM games WHERE game_json = :game_json",
              {'game_json': game_json})
    res = c.fetchall()
    if len(res) == 0: # First occurence of this game
        insert_new_game(conn, c, game_json, winner)
    else: # Next occurance of first game
        new_num_occ = res[0][0] + 1
        if winner == 0:
            new_p1_wins = res[0][1] + 1
        else:
            new_p1_wins = res[0][1]
        with conn:
            c.execute("""UPDATE games SET num_occ = :num_occ, p1_wins = :p1_wins
                         WHERE game_json = :game_json""",
                      {'game_json': game_json, 'num_occ': new_num_occ, 'p1_wins': new_p1_wins})


def check_game_stats(conn, c, game_json):
    c.execute("SELECT num_occ, p1_wins FROM games WHERE game_json = :game_json",
              {'game_json': game_json})
    res = c.fetchall()
    if len(res) == 0:
        return 0, 0
    else:
        return res[0][0], res[0][1]


def close_connection(conn):
    conn.close()
