import random
from copy import deepcopy
import numpy as np
from src.game import Game2048


class HeuristicAI:

    def __init__(self, game, weights=[2.7, 1.0, 1.0]):
        self.game = game
        self.weights = {
            'empty_tiles': weights[0],
            'max_tile_in_corner': weights[1],
            'monotonicity': weights[2],
        }
        self.score = 0 # score for the simulated move

    def set_weights(self, w1, w2, w3):
        self.weights = {
            'empty_tiles': w1,
            'max_tile_in_corner': w2,
            'monotonicity': w3
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

    def can_move(self, board):
        if np.any(board == 0):
            return True
        for x in range(self.game.size):
            for y in range(self.game.size-1):
                if board[x, y] == board[x, y+1]:
                    return True
                if board[y, x] == board[y+1, x]:
                    return True
        return False

    def _move_row_left(self, row):
        # slide non-zero tiles
        tiles = row[row != 0]
        result = []
        skip = False
        i = 0
        while i < len(tiles):
            if i + 1 < len(tiles) and tiles[i] == tiles[i + 1]:
                result.append(tiles[i] * 2)
                self.score += tiles[i] * 2
                i += 2
            else:
                result.append(tiles[i])
                i += 1
        result.extend([0] * (self.game.size - len(result)))
        return np.array(result, dtype=int)

    def simulate_move(self, board, direction):
        """
        direction: {'up': 3, 'down': 1, 'left': 0, 'right': 2}
        returns: (changed, reward, done)
        """
        rotated = np.rot90(board, -direction)
        moved = np.array([self._move_row_left(row) for row in rotated])
        new_board = np.rot90(moved, direction)

        if not np.array_equal(board, new_board):
            board = new_board
            reward = self.score
            done = not self.can_move(new_board)
            return True, reward, done
        else:
            return False, 0, not self.can_move(new_board)

    def get_best_move(self):
        best_score = -1
        best_move = None
        for move in range(4):  # {'up': 3, 'down': 1, 'left': 0, 'right': 2}
            self.score = 0
            changed, reward, done = self.simulate_move(self.game.board, move)
            if changed and not done:
                # score = self.evaluate_board(temp_game.get_state())
                if reward > best_score:
                    best_score = reward
                    best_move = move
        return best_move if best_move is not None else random.choice([0, 1, 2, 3])