from enum import Enum
from types import SimpleNamespace
from collections import namedtuple
HEIGHT = 1000
WIDTH = 1000

BLOCK_SIZE = 20
VELOCITY = 100


class Direction(Enum):
    RIGHT = 1
    LEFT = -1
    UP = 2
    DOWN = -2


Colours = SimpleNamespace()
Colours.BLUE2 = (150, 100, 255)
Colours.BLACK = (0, 0, 0)
Colours.WHITE = (255, 255, 255)
Colours.RED = (255, 50, 50)
Colours.BLUE1 = (0, 0, 255)


Point = namedtuple('Point', 'x, y')
# print(Colours.BLACK._value_ == (0, 0, 0))

image_path = "./resource/green_bg_2.jpg"


# AI Constants

# Actions
Action = SimpleNamespace()
Action.GO_FORWORD = [1, 0, 0]
Action.GO_LEFT = [0, 0, 1]
Action.GO_RIGHT = [0, 1, 0]

# Rewords
Reword = SimpleNamespace()
Reword.EAT_FOOD = 10
Reword.NONE = 0
Reword.GAME_OVER = -10
