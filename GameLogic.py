# ---------------------------------------------------------------------------
# CastleDungeon, GameLogic
# Mike Christle 2022
# ---------------------------------------------------------------------------

import pygame
import random
import GameState
from Cell import Cell
from pygame import mixer

slap = mixer.Sound('Sounds/Slap.wav')
ding = mixer.Sound('Sounds/Ding.wav')
fall = mixer.Sound('Sounds/Fall.wav')
fight = mixer.Sound('Sounds/Fight.wav')
roar = mixer.Sound('Sounds/Roar.wav')
tada = mixer.Sound('Sounds/TaDa.wav')
whoop = mixer.Sound('Sounds/Whoop.wav')


# ---------------------------------------------------------------------------
def check_move(key):
    cell = GameState.maze[GameState.pris_y][GameState.pris_x]

    match key:
        case pygame.K_RIGHT if cell.rit: GameState.pris_x += 1
        case pygame.K_LEFT  if cell.lft: GameState.pris_x -= 1
        case pygame.K_UP    if cell.top: GameState.pris_y -= 1
        case pygame.K_DOWN  if cell.bot: GameState.pris_y += 1
        case _:
            slap.play()
            return

    cell = GameState.maze[GameState.pris_y][GameState.pris_x]
    match cell.con:
        case Cell.COIN:
            GameState.coin_count += 1
            cell.con = Cell.NONE
            ding.play()
        case Cell.ROPE:
            GameState.rope_count += 1
            cell.con = Cell.NONE
            ding.play()
        case Cell.SWORD:
            GameState.sword_count += 1
            cell.con = Cell.NONE
            ding.play()
        case Cell.MONSTER if GameState.sword_count > 0:
            GameState.sword_count -= 1
            cell.con = Cell.NONE
            fight.play()
        case Cell.MONSTER if GameState.sword_count == 0:
            GameState.game_done = True
            roar.play()
        case Cell.PIT if GameState.rope_count > 0:
            GameState.rope_count -= 1
            cell.con = Cell.NONE
            whoop.play()
        case Cell.PIT if GameState.rope_count == 0:
            GameState.game_done = True
            fall.play()
        case Cell.DOOR:
            GameState.game_done = True
            tada.play()


# ---------------------------------------------------------------------------
def fill_maze():

    # Reset game
    GameState.coin_count = 0
    GameState.sword_count = 0
    GameState.rope_count = 0
    GameState.game_done = False

    # Add coins to the maze
    count = GameState.COINS
    while count > 0:
        x = random.randrange(0, GameState.MAZE_WIDTH)
        y = random.randrange(0, GameState.MAZE_HEIGHT)
        cell = GameState.maze[y][x]
        if cell.con == Cell.NONE:
            cell.con = Cell.COIN
            count -= 1

    # Add monsters to the maze
    count = GameState.SWORDS
    while count > 0:
        x = random.randrange(0, GameState.MAZE_WIDTH)
        y = random.randrange(0, GameState.MAZE_HEIGHT)
        cell = GameState.maze[y][x]
        if cell.con == Cell.NONE:
            cell.con = Cell.SWORD
            count -= 1

    # Add monsters to the maze
    count = GameState.SWORDS
    while count > 0:
        x = random.randrange(0, GameState.MAZE_WIDTH)
        y = random.randrange(0, GameState.MAZE_HEIGHT)
        cell = GameState.maze[y][x]
        if cell.con == Cell.NONE:
            cell.con = Cell.MONSTER
            count -= 1

    # Add ropes to the maze
    count = GameState.ROPES
    while count > 0:
        x = random.randrange(0, GameState.MAZE_WIDTH)
        y = random.randrange(0, GameState.MAZE_HEIGHT)
        cell = GameState.maze[y][x]
        if cell.con == Cell.NONE:
            cell.con = Cell.ROPE
            count -= 1

    # Add pits to the maze
    count = GameState.ROPES
    while count > 0:
        x = random.randrange(0, GameState.MAZE_WIDTH)
        y = random.randrange(0, GameState.MAZE_HEIGHT)
        cell = GameState.maze[y][x]
        if cell.con == Cell.NONE:
            cell.con = Cell.PIT
            count -= 1

    # Add a door to the maze
    while True:
        x = random.randrange(0, GameState.MAZE_WIDTH)
        y = random.randrange(0, GameState.MAZE_HEIGHT)
        cell = GameState.maze[y][x]
        if cell.con == Cell.NONE:
            cell.con = Cell.DOOR
            break

    # Add the prisoner to the maze
    while True:
        x = random.randrange(0, GameState.MAZE_WIDTH)
        y = random.randrange(0, GameState.MAZE_HEIGHT)
        cell = GameState.maze[y][x]
        if cell.con == Cell.NONE:
            GameState.pris_x = x
            GameState.pris_y = y
            break

