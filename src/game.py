import queue

class Game:
    def __init__(self, width = 9, height = 9, blocks1 = 10, blocks2 = 10):
        self.width = width
        self.height = height
        self.blocks_left = [blocks1, blocks2]
        self.move = 0
        self.moves = []
        self.ended = False
        self.winner = -1
        self.players_pos = [(self.width // 2, 0), ((self.width - 1) // 2, self.height - 1)]
        self.blocks = {}
        for i in range(self.width - 1):
            for j in range(self.height - 1):
                self.blocks[(i, j)] = "null"


    def check_step(self, pos1, pos2):
        """ Checks if move is possible between pos1 and pos2,
        neglecting players positions and turns. Used also in BFS. """

        if pos1[0] < 0 or pos1[0] >= self.width or pos1[1] < 0 or pos1[1] >= self.height:
            return  False # First position not on the board
        if pos2[0] < 0 or pos2[0] >= self.width or pos2[1] < 0 or pos2[1] >= self.height:
            return  False # Second position not on the board

        x_dis = abs(pos1[0] - pos2[0])
        y_dis = abs(pos1[1] - pos2[1])
        if x_dis + y_dis != 1:
            return False # Position too far      
        if x_dis != 0:
            space_vert_x = min(pos1[0], pos2[0])
            if pos1[1] > 0 and self.blocks[(space_vert_x, pos1[1] - 1)] == "vert":
                return False # Blocked by vertical block
            if pos1[1] < self.height - 1 and self.blocks[(space_vert_x, pos1[1])] == "vert":
                return False # Blocked by vertical block
        if y_dis != 0:
            space_vert_y = min(pos1[1], pos2[1])
            if pos1[0] > 0 and self.blocks[(pos1[0] - 1, space_vert_y)] == "horiz":
                return False # Blocked by horizontal block
            if pos1[0] < self.width - 1 and self.blocks[(pos1[0], space_vert_y)] == "horiz":
                return False # Blocked by horizontal block

        return True


    def move_if_possible(self, player, pos):
        if self.move % 2 != player:
            return False # Not this players turn

        second_player_pos = self.players_pos[(player + 1) % 2]
        if second_player_pos == (pos[0], pos[1]):
            return False # Another player is standing there
        if self.check_step(self.players_pos[player], pos):
            self.players_pos[player] = pos[0], pos[1]
            self.move += 1
            return True # Move was correct
        if self.check_step(self.players_pos[player], second_player_pos) and self.check_step(second_player_pos, pos):
            self.players_pos[player] = pos[0], pos[1]
            self.move += 1
            return True # Jumped over second player
        return False


    def check_dist(self, player, rank):
        """ Checks length of route between player and the closest
        field of given rank. Returns -1 if route is blocked. """

        dist = []
        for i in range(self.width):
            dist.append([-1] * self.height)
        que = queue.Queue()
        que.put(self.players_pos[player])
        dist[self.players_pos[player][0]][self.players_pos[player][1]] = 0

        while not que.empty():
            x, y = que.get()
            dist_here = dist[x][y]
            if y == rank:
                return dist_here
            if self.check_step((x - 1, y), (x, y)) and dist[x - 1][y] == -1:
                dist[x - 1][y] = dist_here + 1
                que.put((x - 1, y))
            if self.check_step((x + 1, y), (x, y)) and dist[x + 1][y] == -1:
                dist[x + 1][y] = dist_here + 1
                que.put((x + 1, y))
            if self.check_step((x, y - 1), (x, y)) and dist[x][y - 1] == -1:
                dist[x][y - 1] = dist_here + 1
                que.put((x, y - 1))
            if self.check_step((x, y + 1), (x, y)) and dist[x][y + 1] == -1:
                dist[x][y + 1] = dist_here + 1
                que.put((x, y + 1))
        return -1


    def check_accessibility(self):
        """ Checks if both players can reach ther winning ranks. """

        return self.check_dist(0, self.height - 1) != -1 and self.check_dist(1, 0) != -1
        


    def check_block(self, block_type, pos):
        """ Checks if placing block is possible, neglecting players turn.
        Used also in highlighting """

        if pos[0] < 0 or pos[0] >= self.width - 1 or pos[1] < 0 or pos[1] >= self.height - 1:
            return False # Position outside of the board

        if self.blocks[pos] != "null":
            return False # Block already at this position

        if block_type == "vert":
            if pos[1] > 0 and self.blocks[(pos[0], pos[1] - 1)] == "vert":
                return False # Block at upper half
            if pos[1] < self.height - 2 and self.blocks[(pos[0], pos[1] + 1)] == "vert":
                return False # Block at lower half

        if block_type == "horiz":
            if pos[0] > 0 and self.blocks[(pos[0] - 1, pos[1])] == "horiz":
                return False # Block at left half
            if pos[0] < self.width - 2 and self.blocks[(pos[0] + 1, pos[1])] == "horiz":
                return False # Block at right half

        self.blocks[pos] = block_type
        accessible = self.check_accessibility()
        self.blocks[pos] = "null"

        return accessible


    def place_block(self, player, block_type, pos):
        if player == self.move % 2 and self.blocks_left[player] > 0:
            if self.check_block(block_type, pos):
                self.blocks[pos] = block_type
                self.blocks_left[player] -= 1
                self.move += 1
                return True
            elif block_type == "vert" and self.check_block(block_type, (pos[0], pos[1] - 1)):
                self.blocks[pos[0], pos[1] - 1] = block_type
                self.blocks_left[player] -= 1
                self.move += 1
                return True
            elif block_type == "horiz" and self.check_block(block_type, (pos[0] - 1, pos[1])):
                self.blocks[pos[0] - 1, pos[1]] = block_type
                self.blocks_left[player] -= 1
                self.move += 1
                return True
        return False

    
    def undo_move(self):
        if len(self.moves) == 0:
            return
        
        last_move = self.moves[-1]
        self.moves.pop()
        self.move -= 1

        if last_move["id"] == "move":
            self.players_pos[self.move % 2] = last_move["old_pos"]
        elif last_move["id"] in ("vert", "horiz"):
            print(f"Block at {last_move['pos']} removed")
            self.blocks[tuple(last_move["pos"])] = "null"
            self.blocks_left[self.move % 2] += 1



    def check_winner(self, player):
        if player == 0 and self.players_pos[player][1] == self.height - 1:
            return True
        elif player == 1 and self.players_pos[player][1] == 0:
            return True
        return False