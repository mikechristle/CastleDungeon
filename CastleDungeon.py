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

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

# 2 Second timer event
pygame.time.set_timer(pygame.USEREVENT, 1000)

paint_intro()

while True:

    # Get all pygame events
    for event in pygame.event.get():
        match event.type:

            # Exit if window is closed
            case pygame.QUIT:
                sys.exit()

            case pygame.KEYDOWN if event.key == pygame.K_x:
                sys.exit()

            case pygame.KEYDOWN if event.key == pygame.K_n:
                make_maze()
                fill_maze()
                paint()

            case pygame.USEREVENT if GameState.game_active:
                move_monsters()
                paint()

            case pygame.KEYDOWN if GameState.game_active:
                check_move(event.key)
                paint()
