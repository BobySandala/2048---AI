import random
import numpy as np
import pygame
from . import tile, globals
import keyboard
from typing import Dict, Tuple

class Game2048:
    def __init__(self, size=4):
        self.size = size
        self.board = np.zeros((size, size), dtype=int)
        self.score = 0
        self.reset()

        self.window_size = width, height = 500, 600
        self.tile_size = 400 // 4
        self.tile_offset = 5
        self.tile_map_pos = (50, 150)
        self.moves = {}  # mapping of tile movements for animation

    def reset(self):
        self.board[:] = 0
        self.score = 0
        self._spawn()
        self._spawn()
        return self.board.copy()

    def _spawn(self):
        empties = list(zip(*np.where(self.board == 0)))
        if not empties:
            return False
        x, y = random.choice(empties)
        self.board[x, y] = 2 if random.random() < 0.9 else 4
        return True

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
        result.extend([0] * (self.size - len(result)))
        return np.array(result, dtype=int)

    def calc_moves(self, old_board, new_board, direction: int) -> Dict[Tuple[int,int], Tuple[int,int,int]]:
        """
        Return mapping of moved tiles:
        { (r_old, c_old): (r_new, c_new, value) }

        old_board, new_board: 2D arrays of ints (numpy arrays are fine)
        direction: 0=left, 1=down, 2=right, 3=up
        """
        old = np.asarray(old_board)
        new = np.asarray(new_board)
        N = self.size

        # --- helper: simulate one row left and return mapping old_col -> new_col ---
        def move_row_left_with_mapping(row):
            """
            row: list/1D-array of length N
            returns (new_row_list, mapping_dict)
            mapping_dict: { old_col_index: new_col_index }
            """
            positions = [i for i, v in enumerate(row) if v != 0]
            values = [row[i] for i in positions]
            mapping = {}
            new_vals = []
            new_col = 0
            i = 0
            while i < len(values):
                if i + 1 < len(values) and values[i] == values[i + 1]:
                    # merge values[i] and values[i+1]
                    new_vals.append(values[i] * 2)
                    mapping[positions[i]] = new_col
                    mapping[positions[i+1]] = new_col
                    i += 2
                else:
                    new_vals.append(values[i])
                    mapping[positions[i]] = new_col
                    i += 1
                new_col += 1
            # pad to full width
            new_row = new_vals + [0] * (N - len(new_vals))
            return new_row, mapping

        # --- rotate boards so the move becomes a LEFT move in rotated coordinates ---
        rot_old = np.rot90(old, -direction)   # same rotation used before calling _move_row_left
        # rot_new = np.rot90(new, -direction) # not required for mapping; used only for optional validation

        # prepare a coords grid so we can map rotated coords back to world coords
        coords = np.empty((N, N), dtype=object)
        for r in range(N):
            for c in range(N):
                coords[r, c] = (r, c)
        coords_rot = np.rot90(coords, -direction)  # coords_rot[r_rot,c_rot] -> (r_world, c_world)

        # --- compute mapping in rotated space by simulating each row ---
        moves_rot = {}   # keys: (r_rot, c_old_rot) -> (r_rot, c_new_rot, value)
        for r in range(N):
            row = rot_old[r].tolist()
            _, mapping = move_row_left_with_mapping(row)
            for old_col, new_col in mapping.items():
                val = int(row[old_col])
                moves_rot[(r, old_col)] = (r, new_col, val)

        # --- convert rotated positions back to world coordinates ---
        final_moves = {}
        for (r_old_rot, c_old_rot), (r_new_rot, c_new_rot, val) in moves_rot.items():
            r_old_world, c_old_world = coords_rot[r_old_rot, c_old_rot]
            r_new_world, c_new_world = coords_rot[r_new_rot, c_new_rot]
            final_moves[(int(r_old_world), int(c_old_world))] = (int(r_new_world), int(c_new_world), int(val))

        return final_moves


    def move(self, direction):
        """
        direction: {'up': 3, 'down': 1, 'left': 0, 'right': 2}
        returns: (changed, reward, done)
        """
        rotated = np.rot90(self.board, -direction)
        moved = np.array([self._move_row_left(row) for row in rotated])
        new_board = np.rot90(moved, direction)
        self.moves = self.calc_moves(self.board, new_board, direction)
        print("Moves:", self.moves)

        if not np.array_equal(self.board, new_board):
            self.board = new_board
            self._spawn()
            reward = self.score
            done = not self.can_move()
            return True, reward, done
        else:
            return False, 0, not self.can_move()

    def can_move(self):
        if np.any(self.board == 0):
            return True
        for x in range(self.size):
            for y in range(self.size-1):
                if self.board[x, y] == self.board[x, y+1]:
                    return True
                if self.board[y, x] == self.board[y+1, x]:
                    return True
        return False
    
    def draw_tile_map(self):
        globals.screen.fill((251, 249, 215))  # background color
        tile.draw_grid()
        tile.display_score(self.score)
        for i in range(self.size):
            for j in range(self.size):
                tile.display_tile(self.board[i, j], (j, i), 
                                  offset=self.tile_offset, size=self.tile_size, 
                                  board_pos=self.tile_map_pos)
        pygame.display.flip()

    def animate_tile_movement(self, moves):
        for i in range(101):  # 0% to 100%
            progress = i / 100.0

            # clear once
            globals.screen.fill((251, 249, 215))
            tile.draw_grid()
            tile.display_score(self.score)

            # draw ALL tiles at this progress
            for (sr, sc), (er, ec, v) in moves.items():
                tile.animate_tile_movement(
                    (sc, sr), (ec, er), v,
                    size=self.tile_size, progress=progress
                )

            # then update once
            pygame.display.flip()
            pygame.time.delay(2)


    def get_state(self):
        return self.board.copy()

    def __str__(self):
        return str(self.board) + f"  Score: {self.score}"
