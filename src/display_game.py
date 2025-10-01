import pygame
import sys

BACKGROUND_COLOR = (251, 249, 215)

pygame.init()
window_size = width, height = 500, 600
tile_size = 400 // 4
tile_offset = 5
tile_map_pos = (50, 150)
screen = pygame.display.set_mode((width, height))
font = pygame.font.SysFont("Arial", 40)

import math

def get_color(value):
    if value == 0:
        return (205, 193, 180)  # empty tile gray

    # Normalize value using log2 (2 → 1, 4 → 2, ..., 2048 → 11)
    level = math.log2(value)

    # Define maximum level (cap at 11 = 2048)
    max_level = 11
    t = min(level / max_level, 1.0)  # in [0,1]

    # Interpolate between yellow (255,255,0) and red (255,0,0)
    r = 255
    g = int(255 * (1 - t))  # decreases with tile value
    b = 0

    return (r, g, b)



def draw_tile(value, pos, progress=1.0):
    """Draws a tile at a pixel position (x,y)."""
    x, y = pos
    rect = pygame.Rect(x, y, tile_size, tile_size)
    pygame.draw.rect(screen, get_color(value), rect, border_radius=8)
    if value:
        text_color = (0,0,0) if value < 8 else (255,255,255)
        text = font.render(str(value), True, text_color)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

def animate_move(board, moves, duration=0.15, fps=60):
    """
    board: final state of board after move
    moves: dict of { (old_i,old_j) : (new_i,new_j,value) }
    """
    frames = int(duration * fps)
    for frame in range(frames+1):
        screen.fill(BACKGROUND_COLOR)
        progress = frame / frames
        # draw moving tiles
        for (i,j), (ni,nj,value) in moves.items():
            start_x, start_y = j*tile_size, i*tile_size
            end_x, end_y = nj*tile_size, ni*tile_size
            x = start_x + (end_x - start_x) * progress
            y = start_y + (end_y - start_y) * progress
            draw_tile(value, (x,y))
        pygame.display.flip()
        pygame.time.delay(int(1000/fps))
