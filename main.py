import pygame
import random
import numpy as np
from src import game as Game
from src.HeurisiticAI import HeuristicAI
import src.globals as globals
import src.button as ButtonModule

pygame.init()

key_map = {
    pygame.K_UP: 3,
    pygame.K_DOWN: 1,
    pygame.K_LEFT: 0,
    pygame.K_RIGHT: 2
}

game = Game.Game2048()
ai = HeuristicAI(game)

globals.screen = pygame.display.set_mode((500, 600))
globals.font = pygame.font.SysFont("font\Montserrat-VariableFont_wght.ttf", 40)
pygame.display.set_caption("2048")

clock = pygame.time.Clock()
running = True
user_input = False

current_window = 0

button1 = ButtonModule.Button(
    rect=pygame.Rect(150, 250, 200, 60),
    color=(255, 165, 100),
    text="Quit",
    font=globals.font,
    text_color=(255, 255, 255),
    action=lambda: quit_game()
)
button2 = ButtonModule.Button(
    rect=pygame.Rect(150, 350, 200, 60),
    color=(255, 165, 100),
    text="Heuristic AI",
    font=globals.font,
    text_color=(255, 255, 255),
    action=lambda: play_game()
)

def quit_game():
    global running
    running = False

def play_game():
    global current_window
    current_window = 1

buttons = [button1, button2]

def game_over_screen():
    global current_window
    current_window = 0
    game.reset()

def draw_game_over(screen, score, screenshot):

    # Step 2: Downscale + upscale = blur
    scale = 0.1
    w, h = screenshot.get_size()
    small = pygame.transform.smoothscale(screenshot, (int(w*scale), int(h*scale)))
    blurred = pygame.transform.smoothscale(small, (w, h))

    screen.blit(blurred, (0, 0))

    # Step 3: Dark overlay
    overlay = pygame.Surface((w, h))
    overlay.set_alpha(100)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    # Step 4: Text
    font_big = globals.font
    font_small = globals.font

    game_over_text = font_big.render("GAME OVER", True, (255, 127, 80))
    score_text = font_small.render(f"Score: {score}", True, (255, 127, 80))

    screen.blit(game_over_text, (w//2 - game_over_text.get_width()//2, h//3))
    screen.blit(score_text, (w//2 - score_text.get_width()//2, h//3 + 100))

    # Step 5: Buttons
    button_color = (255, 150, 100)
    button_hover = (255, 180, 140)

    restart_rect = pygame.Rect(w//2 - 100, h//2, 200, 50)
    quit_rect = pygame.Rect(w//2 - 100, h//2 + 70, 200, 50)

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    for rect, text, action in [
        (restart_rect, "Restart", "restart"),
        (quit_rect, "Quit", "quit")
    ]:
        color = button_hover if rect.collidepoint(mouse) else button_color
        pygame.draw.rect(screen, color, rect, border_radius=10)

        txt = font_small.render(text, True, (0, 0, 0))
        screen.blit(txt, (rect.centerx - txt.get_width()//2,
                          rect.centery - txt.get_height()//2))

        if rect.collidepoint(mouse) and click[0]:  # left click
            return action  # <── Return "restart" or "quit"

    pygame.display.flip()
    return None

while running:

    if current_window == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for btn in buttons:
                btn.handle_event(event)

        globals.screen.fill((251,249,215))  # background

        # draw buttons
        for btn in buttons:
            btn.draw(globals.screen)

    if current_window == 1:
        action = None
        if user_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False  # allows window to close
                elif event.type == pygame.KEYDOWN:
                    if event.key in key_map:
                        action = key_map[event.key]
        else:
            action = ai.get_best_move()

        if action is not None:
            changed, reward, done = game.move(action)
            if changed:
                print(f"Action {action}, reward {reward}")
                print(game)

            if done:  # game over
                screenshot = globals.screen.copy()
                game_over = True
                while game_over:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()

                    action = draw_game_over(globals.screen, game.score, screenshot)

                    if action == "restart":
                        game = Game.Game2048()  # reset the game
                        game_over = False       # leave game-over loop
                        current_window = 0
                    elif action == "quit":
                        pygame.quit()
                        exit()

            game.animate_tile_movement(game.moves)

        # draw your board
        game.draw_tile_map()

    pygame.display.flip()
    clock.tick(60)  # limit to 60 FPS

pygame.quit()
