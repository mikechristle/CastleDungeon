# ---------------------------------------------------------------------------
# CastleDungeon, Cell
# Mike Christle 2022
# ---------------------------------------------------------------------------
class Cell:

    # Possible contents for a maze cell
    NONE = 0
    DOOR = 1
    COIN = 2
    SWORD = 3
    PIT = 4
    MONSTER = 5
    ROPE = 6

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.top = False
        self.bot = False
        self.lft = False
        self.rit = False
        self.con = Cell.NONE
        self.val = 0

    def clear(self):
        self.top = False
        self.bot = False
        self.lft = False
        self.rit = False
        self.con = Cell.NONE
        self.val = 0

    _contents = ('NONE', 'DOOR', 'COIN', 'SWORD', 'PIT', 'MONSTER', 'ROPE')

    def __repr__(self):
        return f'{self.x} {self.y} {Cell._contents[self.con]}'
