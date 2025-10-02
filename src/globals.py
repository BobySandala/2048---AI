import pygame
from . import game
from . import globals
from . import GeneticAI
from . import HeurisiticAI
from . import button as ButtonModule
from multiprocessing import Process, Queue
import os

input_q = Queue()
output_q = Queue()
queue = Queue()


screen = None
font = None

key_map = {
    pygame.K_UP: 3,
    pygame.K_DOWN: 1,
    pygame.K_LEFT: 0,
    pygame.K_RIGHT: 2
}

Game = None
ai = None

globals.screen = None
# Build path relative to project root
globals.font = None

clock = None
user_input = False
running = True
