# ---------------------------------------------------------------------------
# CastleDungeon
# Mike Christle 2022
# ---------------------------------------------------------------------------

import sys
import pygame

import GameState
from Paint import paint
from MakeMaze import make_maze
from GameLogic import fill_maze, check_move

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

# 2 Second timer event
pygame.time.set_timer(pygame.USEREVENT, 2000)

make_maze()
fill_maze()
paint()

while True:

    # Get all pygame events
    for event in pygame.event.get():
        # print(event)
        match event.type:

            # Exit if window is closed
            case pygame.QUIT:
                sys.exit()

            case pygame.USEREVENT:
                print('Timer Event')

            case pygame.KEYDOWN if event.key == pygame.K_F1:
                make_maze()
                fill_maze()

            case pygame.KEYDOWN if not GameState.game_done:
                check_move(event.key)

            case pygame.JOYAXISMOTION if not GameState.game_done:
                value = int(event.value)
                match [event.axis, value]:
                    case [0,  1]: check_move(pygame.K_RIGHT)
                    case [0, -1]: check_move(pygame.K_LEFT)
                    case [4,  1]: check_move(pygame.K_DOWN)
                    case [4, -1]: check_move(pygame.K_UP)

            case pygame.JOYBUTTONDOWN if event.button == 9:
                make_maze()
                fill_maze()

            case pygame.JOYBUTTONDOWN if not GameState.game_done:
                match event.button:
                    case 0: check_move(pygame.K_UP)
                    case 1: check_move(pygame.K_RIGHT)
                    case 2: check_move(pygame.K_DOWN)
                    case 3: check_move(pygame.K_LEFT)

        paint()