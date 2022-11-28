# ---------------------------------------------------------------------------
# CastleDungeon
# Mike Christle 2022
# ---------------------------------------------------------------------------

import sys
import pygame

import GameState
from Paint import paint, paint_intro
from MakeMaze import make_maze
from GameLogic import fill_maze, check_move, move_monsters

MOVE_KEYS = (pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT)

# 1 Second timer event
pygame.time.set_timer(pygame.USEREVENT, 1000)

# Display the instruction screen
paint_intro()

while True:

    # Get all pygame events
    for event in pygame.event.get():
        match event.type:

            # Exit if window is closed
            case pygame.QUIT:
                sys.exit()

            # Exit is x key is pressed
            case pygame.KEYDOWN if event.key == pygame.K_x:
                sys.exit()

            # Start a new game if n key os pressed
            case pygame.KEYDOWN if event.key == pygame.K_n:
                make_maze()
                fill_maze()
                paint()

            # If game is active, move monsters each second
            case pygame.USEREVENT if GameState.game_active:
                move_monsters()
                paint()

            # if game is active, check keyboard inputs
            case pygame.KEYDOWN if GameState.game_active:
                if event.key in MOVE_KEYS:
                    check_move(event.key)
                    paint()
