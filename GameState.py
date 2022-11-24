# ---------------------------------------------------------------------------
# CastleDungeon, GameState
# Mike Christle 2022
# ---------------------------------------------------------------------------

from Cell import Cell

MAZE_WIDTH = 21
MAZE_HEIGHT = 17

COINS = 10  # Number of coins
SWORDS = 4  # Number of monsters and swords
ROPES = 4   # Number of pits and ropes

maze = [[Cell(x, y) for x in range(MAZE_WIDTH)] for y in range(MAZE_HEIGHT)]

pris_x = 0
pris_y = 0

coin_count = 0
sword_count = 0
rope_count = 0

game_done = False
