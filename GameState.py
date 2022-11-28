# ---------------------------------------------------------------------------
# CastleDungeon, GameState
# Mike Christle 2022
# ---------------------------------------------------------------------------

from Cell import Cell

# These parameters can be adjusted for the size of the maze
MAZE_WIDTH = 22     # Width of maze is cells
MAZE_HEIGHT = 18    # Height of maze is cells

# Initial count of rewards
COINS = 10
SWORDS = 4
ROPES = 4

# The maze structure
maze = [[Cell(x, y) for x in range(MAZE_WIDTH)] for y in range(MAZE_HEIGHT)]

# Current location of prisoner
pris_x = 0
pris_y = 0

# Current count of rewards
coin_count = 0
sword_count = 0
rope_count = 0

# Indicates that the game is active
game_active = False

# Three minute alarm timer
timeout_counter = 0
