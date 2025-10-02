import src.globals as globals
import os
import numpy as np
import pygame

if __name__ == "__main__":
    pygame.init()


    globals.screen = pygame.display.set_mode((500, 600))
    # Build path relative to project root
    font_path = os.path.join("font", "Montserrat-VariableFont_wght.ttf")
    globals.font = pygame.font.Font(font_path, 36)
    pygame.display.set_caption("2048")

    globals.clock = pygame.time.Clock()
    globals.running = True
    globals.user_input = False
    globals.current_window = 0

    globals.Game = globals.game.Game2048(board=np.zeros((4, 4), dtype=int), size=4)
    globals.ai = globals.HeurisiticAI.HeuristicAI(globals.Game)

    import src.UI as UIModule
    import src.GeneticAI as GeneticAIModule

    while globals.running:
        UIModule.draw_UI()

pygame.quit()
