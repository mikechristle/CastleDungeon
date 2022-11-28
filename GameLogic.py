# ---------------------------------------------------------------------------
# CastleDungeon, GameLogic
# Mike Christle 2022
# ---------------------------------------------------------------------------

import pygame
import random
import GameState
from Cell import Cell
from pygame import mixer

pygame.mixer.init()
slap = mixer.Sound('Sounds/Slap.wav')
ding = mixer.Sound('Sounds/Ding.wav')
fall = mixer.Sound('Sounds/Fall.wav')
fight = mixer.Sound('Sounds/Fight.wav')
roar = mixer.Sound('Sounds/Roar.wav')
tada = mixer.Sound('Sounds/TaDa.wav')
whoop = mixer.Sound('Sounds/Whoop.wav')
alarm = mixer.Sound('Sounds/Alarm.wav')

monsters = []
slap_count = 0
slap_key = pygame.K_SPACE


# ---------------------------------------------------------------------------
def check_slap(key):
    """If the same wall is slapped 5 times, remove the wall."""
    global slap_key, slap_count

    # If first slap
    if slap_key != key:
        slap_key = key
        slap_count = 4
    else:
        slap_count -= 1

        # If fifth slap
        if slap_count == 0:
            slap_key = pygame.K_SPACE
            x = GameState.pris_x
            y = GameState.pris_y

            # Which wall to remove
            match key:
                case pygame.K_RIGHT:
                    GameState.maze[y][x].rit = True
                    GameState.maze[y][x + 1].lft = True
                case pygame.K_LEFT:
                    GameState.maze[y][x].lft = True
                    GameState.maze[y][x - 1].rit = True
                case pygame.K_UP:
                    GameState.maze[y][x].top = True
                    GameState.maze[y - 1][x].bot = True
                case pygame.K_DOWN:
                    GameState.maze[y][x].bot = True
                    GameState.maze[y + 1][x].top = True


# ---------------------------------------------------------------------------
def check_move(key):
    """Check the key and move the prisoner."""

    global slap_key

    # Check for valid moves
    cell = GameState.maze[GameState.pris_y][GameState.pris_x]
    match key:
        case pygame.K_RIGHT if cell.rit: GameState.pris_x += 1
        case pygame.K_LEFT  if cell.lft: GameState.pris_x -= 1
        case pygame.K_UP    if cell.top: GameState.pris_y -= 1
        case pygame.K_DOWN  if cell.bot: GameState.pris_y += 1
        case _:
            # If not a valid move, slap the wall
            slap.play()
            check_slap(key)
            return

    # Check the new cell for rewords and hazards
    slap_key = pygame.K_SPACE
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
            GameState.game_active = False
            roar.play()
        case Cell.PIT if GameState.rope_count > 0:
            GameState.rope_count -= 1
            cell.con = Cell.NONE
            whoop.play()
        case Cell.PIT if GameState.rope_count == 0:
            GameState.game_active = False
            fall.play()
        case Cell.DOOR:
            GameState.game_active = False
            tada.play()


# ---------------------------------------------------------------------------
def move_monsters():
    """
    Randomly move the monsters once a second.
    Check tree minute alarm timer.
    """

    # If alarm timer has expired, sound alarm and end game.
    GameState.timeout_counter -= 1
    if GameState.timeout_counter == 0:
        GameState.game_active = False
        alarm.play()
        return

    # For each active monster
    for _ in range(len(monsters)):
        x0, y0 = monsters.pop(0)
        cell0 = GameState.maze[y0][x0]

        # If cell is empty then monster was slain
        if cell0.con != Cell.MONSTER:
            continue

        # Attempt to move monster in a random direction
        x1, y1 = x0, y0
        match random.randrange(0, 4):
            case 0 if cell0.top: y1 -= 1
            case 1 if cell0.rit: x1 += 1
            case 2 if cell0.bot: y1 += 1
            case 3 if cell0.lft: x1 -= 1
            case _:
                # If blocked by a wall, leave it where it is
                monsters.append((x0, y0))
                continue

        # If prisoner is in new cell
        if x1 == GameState.pris_x and y1 == GameState.pris_y:

            # If prisoner has a sword, slay the monster
            if GameState.sword_count > 0:
                GameState.sword_count -= 1
                cell0.con = Cell.NONE
                fight.play()
                continue

            # Else prisoner dies and the game ends
            else:
                GameState.game_active = False
                roar.play()
                return

        # Move the monster to the new cell
        cell1 = GameState.maze[y1][x1]
        if cell1.con == Cell.NONE:
            cell1.con = Cell.MONSTER
            cell0.con = Cell.NONE
            monsters.append((x1, y1))
        else:
            monsters.append((x0, y0))


# ---------------------------------------------------------------------------
def fill_maze():
    """Fill a new maze with rewords, hazards and a prisoner."""

    # Reset game
    GameState.coin_count = 0
    GameState.sword_count = 0
    GameState.rope_count = 0
    GameState.game_active = True
    GameState.timeout_counter = 180

    # Add coins to the maze
    count = GameState.COINS
    while count > 0:
        x = random.randrange(0, GameState.MAZE_WIDTH)
        y = random.randrange(0, GameState.MAZE_HEIGHT)
        cell = GameState.maze[y][x]
        if cell.con == Cell.NONE:
            cell.con = Cell.COIN
            count -= 1

    # Add swords to the maze
    count = GameState.SWORDS
    while count > 0:
        x = random.randrange(0, GameState.MAZE_WIDTH)
        y = random.randrange(0, GameState.MAZE_HEIGHT)
        cell = GameState.maze[y][x]
        if cell.con == Cell.NONE:
            cell.con = Cell.SWORD
            count -= 1

    # Add monsters to the maze
    monsters.clear()
    count = GameState.SWORDS
    while count > 0:
        x = random.randrange(0, GameState.MAZE_WIDTH)
        y = random.randrange(0, GameState.MAZE_HEIGHT)
        cell = GameState.maze[y][x]
        if cell.con == Cell.NONE:
            cell.con = Cell.MONSTER
            count -= 1
            monsters.append((x, y))

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
