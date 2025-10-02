import pygame
import src.globals as globals
import os

pygame.init()

globals.screen = pygame.display.set_mode((500, 600))
# Build path relative to project root
font_path = os.path.join("font", "Montserrat-VariableFont_wght.ttf")
globals.font = pygame.font.Font(font_path, 40)
pygame.display.set_caption("2048")

globals.clock = pygame.time.Clock()
globals.running = True
globals.user_input = False
globals.current_window = 0

globals.Game = globals.game.Game2048()
globals.ai = globals.HeurisiticAI.HeuristicAI(globals.Game)

import src.UI as UIModule

while globals.running:
    UIModule.draw_UI()

pygame.quit()
