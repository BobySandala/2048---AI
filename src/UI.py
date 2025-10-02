import pygame
from . import game
from . import globals
from . import GeneticAI
from . import HeurisiticAI
from . import button as ButtonModule
from . import read_write_json
from multiprocessing import Process, Queue

pygame.init()

current_window = 0
train_ui_stage = 0  # 0: input params, 1: training in progress, 2: training complete
train_progress = {"progress": 0.0}
p = None

quit_btn = ButtonModule.Button(
    rect=pygame.Rect(130, 500, 240, 60),
    color=(255, 165, 100),
    text="Quit",
    font=globals.font,
    text_color=(255, 255, 255),
    action=lambda: quit_game()
)
genetic_train_btn = ButtonModule.Button(
    rect=pygame.Rect(130, 420, 240, 60),
    color=(255, 165, 100),
    text="Genetic Train",
    font=globals.font,
    text_color=(255, 255, 255),
    action=lambda: train_genetic_ai_ui()
)
heurisitc_btn = ButtonModule.Button(
    rect=pygame.Rect(130, 350, 240, 60),
    color=(255, 165, 100),
    text="Heuristic AI",
    font=globals.font,
    text_color=(255, 255, 255),
    action=lambda: play_game()
)
start_train_btn = ButtonModule.Button(
    rect=pygame.Rect(130, 420, 240, 60),
    color=(255, 165, 100),
    text="Start Training",
    font=globals.font,
    text_color=(255, 255, 255),
    action=lambda: start_train_genetic_ai()
)
main_menu_btn = ButtonModule.Button(
    rect=pygame.Rect(130, 420, 240, 60),
    color=(255, 165, 100),
    text="Main Menu",
    font=globals.font,
    text_color=(255, 255, 255),
    action=lambda: go_to_main_menu()
)

weight_input_box_1 = ButtonModule.NumberInputBox(
    x=350, y=150, w=100, h=50,
    font=globals.font,
    initial_text="50"
)
weight_input_box_2 = ButtonModule.NumberInputBox(
    x=350, y=220, w=100, h=50,
    font=globals.font,
    initial_text="10"
)
weight_input_box_3 = ButtonModule.NumberInputBox(
    x=350, y=290, w=100, h=50,
    font=globals.font,
    initial_text="5"
)
weight_input_boxes = [weight_input_box_1, weight_input_box_2, weight_input_box_3]

def quit_game():
    globals.running = False
    print("Quitting game...")

def play_game():
    global current_window
    current_window = 1
    w1 = read_write_json.load_value("genetic_ai_weights_w1")
    w2 = read_write_json.load_value("genetic_ai_weights_w2")
    w3 = read_write_json.load_value("genetic_ai_weights_w3")
    globals.ai.set_weights(w1, w2, w3)
    print("Starting game with Heuristic AI...")

def train_genetic_ai_ui():
    global current_window
    current_window = 2
    print("Starting Genetic AI training...")

def go_to_main_menu():
    global current_window
    current_window = 0
    print("Go to main menu")

def start_train_genetic_ai():
    global train_ui_stage, p
    print("Starting Genetic AI training with parameters from input boxes...")
    if train_ui_stage == 0:
        try:
            population_size = int(weight_input_box_1.text)
            generations = int(weight_input_box_2.text)
            games = int(weight_input_box_3.text)
            print(f"Starting training with Population: {population_size}, Generations: {generations}, Games: {games}")
            #result = GeneticAI.start_genetic_ai(population_size=population_size, generations=generations, number_of_games=games)
            #GeneticAI.save_to_json(result)

            p = Process(target=GeneticAI.start_genetic_ai, args=(globals.queue, population_size, generations, games))
            p.start()

            train_ui_stage = 1  # move to next stage

            #print(f"Training complete. Best Weights: {result}")
            #start_train_btn.text = "Training Complete"
        except ValueError:
            print("Please enter valid integers for all fields.")

buttons = [genetic_train_btn, heurisitc_btn, quit_btn]
train_ai_buttons = [quit_btn, start_train_btn]
after_train_buttons = [quit_btn, main_menu_btn]

def game_over_screen():
    global current_window
    current_window = 0
    globals.game.reset()

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

def genetic_ai_train_UI():
    global train_ui_stage, train_progress, running, p
    globals.screen.fill((251,249,215))  # background
    if train_ui_stage == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for btn in train_ai_buttons:
                btn.handle_event(event)
            for weight_input_box in weight_input_boxes:
                weight_input_box.handle_event(event)
        # draw buttons and input boxes
        for input_box in weight_input_boxes:
            input_box.draw(globals.screen)
        for btn in train_ai_buttons:
            btn.draw(globals.screen)
        # draw labels
        generations_text = globals.font.render("Generations:", True, (255, 127, 80))
        population_text = globals.font.render("Population:", True, (255, 127, 80))
        games_text = globals.font.render("Games:", True, (255, 127, 80))

        globals.screen.blit(generations_text, (50, 150))
        globals.screen.blit(population_text, (50, 220))
        globals.screen.blit(games_text, (50, 290))
    if train_ui_stage == 1:
        training_text = globals.font.render("Training in progress...", True, (255, 127, 80))
        globals.screen.blit(training_text, (50, 250))
        if not globals.queue.empty():
            train_progress = globals.queue.get()
            print(train_progress)
        train_progress_text = globals.font.render(f"Progress: {train_progress['progress']*100:.2f}%", True, (255, 127, 80))
        globals.screen.blit(train_progress_text, (50, 320))
        if train_progress['progress'] == -1:
            # training finished
            train_ui_stage = 2
            p.join()

            
    if train_ui_stage == 2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for btn in after_train_buttons:
                btn.handle_event(event)
        # draw buttons
        for btn in after_train_buttons:
            btn.draw(globals.screen)

        completed_text = globals.font.render("Completed", True, (255, 127, 80))
        globals.screen.blit(completed_text, (50, 100))

        score_text = globals.font.render(f"Best Score: {read_write_json.load_value("best_score_genetic"):.0f}", True, (255, 127, 80))
        globals.screen.blit(score_text, (50, 150))

    pygame.display.flip()


def draw_UI():
    global current_window, buttons, game
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
        if globals.user_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False  # allows window to close
                elif event.type == pygame.KEYDOWN:
                    if event.key in globals.key_map:
                        action = globals.key_map[event.key]
        else:
            action = globals.ai.get_best_move()

        if action is not None:
            changed, reward, done = globals.Game.move(action)
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

                    action = draw_game_over(globals.screen, globals.Game.score, screenshot)

                    if action == "restart":
                        game = globals.game.Game2048()  # reset the game
                        game_over = False       # leave game-over loop
                        current_window = 0
                    elif action == "quit":
                        pygame.quit()
                        exit()

            globals.Game.animate_tile_movement(globals.Game.moves)

        # draw your board
        globals.Game.draw_tile_map()
    if current_window == 2:
        genetic_ai_train_UI()

    pygame.display.flip()
    globals.clock.tick(60)  # limit to 60 FPS



