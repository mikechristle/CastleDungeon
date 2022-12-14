# ---------------------------------------------------------------------------
# CastleDungeon, Paint
# Mike Christle 2022
# ---------------------------------------------------------------------------

import GameState
import pygame
from Cell import Cell

# Do not change these parameters, they match the size of the .PNG files
CELL_SIZE = 48
PAD = 8

IMAGE_WIDTH = (GameState.MAZE_WIDTH * CELL_SIZE) + PAD
IMAGE_HEIGHT = (GameState.MAZE_HEIGHT * CELL_SIZE) + PAD

COIN_OFFSET = PAD + (CELL_SIZE * 2)
SWORD_OFFSET = COIN_OFFSET + (CELL_SIZE * GameState.COINS)
ROPE_OFFSET = SWORD_OFFSET + (CELL_SIZE * GameState.SWORDS)

RED = (255, 0, 0)
WHITE = (255, 255, 255)
GRAY = (48, 48, 48)

pygame.init()
screen = pygame.display.set_mode((IMAGE_WIDTH, IMAGE_HEIGHT + CELL_SIZE))
pygame.display.set_caption('Castle Dungeon   V1.2')

STATUS_FONT = pygame.font.SysFont('Arial', 36)
HEADER_FONT = pygame.font.SysFont('Arial Bold', 72)
INFO_FONT = pygame.font.SysFont('Arial Bold', 48)

img_door = pygame.image.load("Bitmaps/Door.png")
img_bottom_edge = pygame.image.load("Bitmaps/BottomEdge.png")
img_right_edge = pygame.image.load("Bitmaps/RightEdge.png")
img_cell = pygame.image.load("Bitmaps/Cell.png")
img_coin = pygame.image.load("Bitmaps/Coin.png")
img_cell_l = pygame.image.load("Bitmaps/CellL.png")
img_cell_t = pygame.image.load("Bitmaps/CellT.png")
img_cell_lt = pygame.image.load("Bitmaps/CellLT.png")
img_monster = pygame.image.load("Bitmaps/Monster.png")
img_pit = pygame.image.load("Bitmaps/Pit.png")
img_prisoner = pygame.image.load("Bitmaps/Prisoner.png")
img_prisoner_r = pygame.image.load("Bitmaps/PrisonerR.png")
img_prisoner_s = pygame.image.load("Bitmaps/PrisonerS.png")
img_prisoner_rs = pygame.image.load("Bitmaps/PrisonerRS.png")
img_rope = pygame.image.load("Bitmaps/Rope.png")
img_sword = pygame.image.load("Bitmaps/Sword.png")
img_wall_back = pygame.image.load("Bitmaps/WallBack.png")
img_wall_side = pygame.image.load("Bitmaps/WallSide.png")


# ---------------------------------------------------------------------------
def paint():
    """Paint the screen."""

    # Clear the previous screen
    screen.fill(GRAY)

    # if the game is active, only paint the area around the prisoner
    if GameState.game_active:
        paint_local(GameState.pris_x, GameState.pris_y, 0)

    # Else paint the entire maze
    else:
        paint_all()

    # Paint the status bar at the bottom
    paint_status()

    # Paint the prisoner
    x = (GameState.pris_x * CELL_SIZE) + PAD
    y = (GameState.pris_y * CELL_SIZE) + PAD
    match [GameState.sword_count, GameState.rope_count]:
        case [0, 0]: screen.blit(img_prisoner, (x, y))
        case [0, _]: screen.blit(img_prisoner_r, (x, y))
        case [_, 0]: screen.blit(img_prisoner_s, (x, y))
        case [_, _]: screen.blit(img_prisoner_rs, (x, y))

    pygame.display.flip()


# ---------------------------------------------------------------------------
def paint_status():
    """Paint the status bar."""

    # Paint the dollar amount of coins
    text = STATUS_FONT.render(f'${GameState.coin_count * 100}', True, WHITE)
    rect = text.get_rect()
    rect.top = IMAGE_HEIGHT
    rect.left = PAD
    screen.blit(text, rect)

    # Paint the coins
    y = IMAGE_HEIGHT
    x = COIN_OFFSET
    for _ in range(GameState.coin_count):
        screen.blit(img_coin, (x, y))
        x += CELL_SIZE

    # Paint the swords
    x = SWORD_OFFSET
    for _ in range(GameState.sword_count):
        screen.blit(img_sword, (x, y))
        x += CELL_SIZE

    # Paint the ropes
    x = ROPE_OFFSET
    for _ in range(GameState.rope_count):
        screen.blit(img_rope, (x, y))
        x += CELL_SIZE


# ---------------------------------------------------------------------------
def paint_all():
    """Paint the entire maze."""

    # Paint cells
    for y in range(GameState.MAZE_HEIGHT):
        for x in range(GameState.MAZE_WIDTH):
            paint_cell(x, y)

    # Paint right side walls
    x = GameState.MAZE_WIDTH * CELL_SIZE
    for y in range(GameState.MAZE_HEIGHT):
        y *= CELL_SIZE
        screen.blit(img_right_edge, (x, y))

    # Paint bottom side walls
    y = GameState.MAZE_HEIGHT * CELL_SIZE
    for x in range(GameState.MAZE_WIDTH):
        x *= CELL_SIZE
        screen.blit(img_bottom_edge, (x, y))

    # Paint bottom right corner
    x = GameState.MAZE_WIDTH * CELL_SIZE
    y = GameState.MAZE_HEIGHT * CELL_SIZE
    screen.blit(img_cell, (x, y))


# ---------------------------------------------------------------------------
def paint_local(x, y, depth):
    """Paint cell around the prisoner."""

    # Only paint cells that are one or two cells away from prisoner
    if depth > 2:
        return

    # Paint the current cell
    paint_cell(x, y)

    # Paint the neighboring cells
    cell = GameState.maze[y][x]
    if cell.top:
        paint_local(x, y - 1, depth + 1)
    if cell.lft:
        paint_local(x - 1, y, depth + 1)
    if cell.bot:
        paint_local(x, y + 1, depth + 1)
    else:
        screen.blit(img_bottom_edge, (x * CELL_SIZE, (y + 1) * CELL_SIZE))
    if cell.rit:
        paint_local(x + 1, y, depth + 1)
    else:
        screen.blit(img_right_edge, ((x + 1) * CELL_SIZE, y * CELL_SIZE))


# ---------------------------------------------------------------------------
def paint_cell(x, y):
    """Paint a cell."""

    # Get the cell
    cell = GameState.maze[y][x]

    # Screen coordinates of the cell
    x *= CELL_SIZE
    y *= CELL_SIZE

    # Paint the blank cell image with optional left the top walls
    match [cell.lft, cell.top]:
        case [False, False]: img = img_cell_lt
        case [False, True]:  img = img_cell_l
        case [True, False]:  img = img_cell_t
        case [True, True]:   img = img_cell
    screen.blit(img, (x, y))

    # Paint any contents of the cell
    x += PAD
    y += PAD
    match cell.con:
        case Cell.DOOR: screen.blit(img_door, (x, y))
        case Cell.COIN: screen.blit(img_coin, (x, y))
        case Cell.PIT: screen.blit(img_pit, (x, y))
        case Cell.ROPE: screen.blit(img_rope, (x, y))
        case Cell.MONSTER: screen.blit(img_monster, (x, y))
        case Cell.SWORD: screen.blit(img_sword, (x, y))


# ---------------------------------------------------------------------------
def paint_intro():
    """Paint the intro text screen."""

    intro = (
        'You are a prisoner trapped in a dungeon!',
        'To escape you must find the green door.',
        'However, there are no lights, but you have a small',
        'lantern so you can see a little around yourself.',
        'Beware, there are monsters that will eat your bones.',
        'You can kill a monster if you have a sword, but each sword',
        'will only kill one monster because their blood is acid.',
        'Watch your step, so you don\'t fall into a bottomless pit.',
        'You can cross a bottomless pit if you have a rope.',
        'The rope will get tangled up in the rocks,',
        ' so it is only good for one bottomless pit.',
        'Keep a lookout for gold coins. Each coin is worth $100.',
        'You have three minutes to escape before the alarm goes',
        'off and you are captured.',
        '',
        'Use arrow keys to move prisoner.',
        'Press N for new game, X to exit.',
    )

    # Paint the game title
    text = HEADER_FONT.render('Castle Dungeon', True, RED)
    rect = text.get_rect()
    rect.center = (IMAGE_WIDTH // 2, 40)
    screen.blit(text, rect)

    # Paint each line ot intro text
    y = 120
    for line in intro:
        text = INFO_FONT.render(line, True, RED)
        rect = text.get_rect()
        rect.center = (IMAGE_WIDTH // 2, y)
        screen.blit(text, rect)
        y += 40

    pygame.display.update()

