import random
from copy import deepcopy
import numpy as np
from src.game import Game2048


class HeuristicAI:

    def __init__(self, game):
        self.game = game
        self.weights = {
            'empty_tiles': 2.7,
            'max_tile_in_corner': 1.0,
            'monotonicity': 1.0,
        }

    def max_tile_in_corner(self, board):
        max_tile = board.max()
        corners = [board[0,0], board[0,-1], board[-1,0], board[-1,-1]]  # top-left, top-right, bottom-left, bottom-right
        if max_tile in corners:
            return max_tile   # reward = value of max tile
        else:
            return 0          # no reward if not in a corner
    
    def monotonicity(self, board):
        total = 0
        # Rows
        for row in board:
            inc = 0
            dec = 0
            for i in range(len(row)-1):
                diff = row[i+1] - row[i]
                inc += diff       # good for increasing
                dec -= diff       # bad for decreasing
            total += max(inc, dec)

        # Columns
        for col in board.T:
            inc = 0
            dec = 0
            for i in range(len(col)-1):
                diff = col[i+1] - col[i]
                inc += diff
                dec -= diff

            total += max(inc, dec)

        return total


    def evaluate_board(self, board):
        # Heuristic: prioritize empty tiles and higher values in corners
        empty_tiles = np.sum(board == 0)

        max_tile_in_corner_ = self.max_tile_in_corner(board)

        monotonicity_ = self.monotonicity(board)
                
        return  self.weights['empty_tiles'] * empty_tiles + \
                self.weights['max_tile_in_corner'] * max_tile_in_corner_ + \
                self.weights['monotonicity'] * monotonicity_

    def get_best_move(self):
        best_score = -float('inf')
        best_move = None
        for move in range(4):  # {'up': 3, 'down': 1, 'left': 0, 'right': 2}
            temp_game = deepcopy(self.game)
            changed, _, _ = temp_game.move(move)
            if changed:
                score = self.evaluate_board(temp_game.get_state())
                if score > best_score:
                    best_score = score
                    best_move = move
        return best_move if best_move is not None else random.choice([0, 1, 2, 3])