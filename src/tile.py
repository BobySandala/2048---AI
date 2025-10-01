import pygame
import math
from . import globals

def get_color(value):
    if value == 0:
        return (205, 193, 180)  # empty tile
    level = math.log2(value)
    max_level = 11  # 2048 tile
    t = min(level / max_level, 1.0)
    r = 255
    g = int(255 * (1 - t))  # goes from 255→0
    b = 0
    return (r, g, b)

def display_score(score, pos=(50, 50)):
    """Display the current score on the screen."""
    text = globals.font.render(f"Score: {score}", True, (0, 0, 0))
    globals.screen.blit(text, pos)

def draw_grid(size=4, tile_size=100, margin=5, font=None, offset_x=50, offset_y=150):
    """
    Draw the full 2048 grid with colored tiles and numbers.

    board: 2D array of ints
    tile_size: size of each tile in pixels
    margin: space between tiles
    font: pygame.font.Font object for drawing numbers
    offset_x, offset_y: top-left corner of the grid
    """
    screen = globals.screen
    background_color = (251, 249, 215)  # light background
    screen.fill(background_color)
    
    for r in range(size):
        for c in range(size):
            # compute top-left pixel position with offset
            x = offset_x + c * (tile_size) + margin
            y = offset_y + r * (tile_size) + margin

            color = (205, 193, 180)  # empty tile
            
            # draw rounded rectangle
            rect = pygame.Rect(x, y, tile_size - margin, tile_size - margin)
            pygame.draw.rect(screen, color, rect, border_radius=15)



def animate_tile_movement(start_pos, end_pos, value, size = 100, progress = 0.0):
    """Animate the movement of a tile from start_pos to end_pos."""
    if value == 0:
        return  # don't draw empty tiles
    x_start, y_start = start_pos
    x_end, y_end = end_pos
    x = x_start + (x_end - x_start) * progress
    y = y_start + (y_end - y_start) * progress

    display_tile(value, pos=(x, y), size=size,)


def display_tile(value, pos, offset = 5, size = 100, border_radius = 8, board_pos=(50,150)):
    """Display the tile using pygame."""

    if value == 0:
        return  # don't draw empty tiles
    x, y = pos
    rect = pygame.Rect(x * size + offset + board_pos[0],
                        y * size + offset + board_pos[1],
                        size - offset,
                        size - offset)
    pygame.draw.rect(globals.screen, get_color(value), rect, border_radius=border_radius)

    text_color = (0,0,0) if value < 8 else (255,255,255)
    text = globals.font.render(str(value), True, text_color)
    text_rect = text.get_rect(center=rect.center)
    globals.screen.blit(text, text_rect)

if __name__ == "__main__":
    pygame.init()
    globals.screen = pygame.display.set_mode((500, 600))
    font = pygame.font.SysFont("Arial", 40)
    clock = pygame.time.Clock()

    # Example usage
    tile_value = 128
    tile_pos = (1, 1)
    display_tile(globals.screen, tile_value, tile_pos, size=100, font=font)

    start_pos = (0, 0)
    end_pos = (3, 3)
    for i in range(101):
        progress = i / 100.0
        globals.screen.fill((255, 255, 255))  # Clear screen
        display_tile(globals.screen, tile_value, tile_pos, size=100, font=font)
        animate_tile_movement(globals.screen, start_pos, end_pos, tile_value, size=100, progress=progress, font=font)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()