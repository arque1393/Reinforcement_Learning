
from collections import namedtuple
from constants import SimpleNamespace, Point, BLOCK_SIZE, Direction
import numpy as np

# RL Constants

# Actions
# Action = SimpleNamespace()
# Action.GO_FORWORD = [1, 0, 0]
# Action.GO_LEFT = [0, 0, 1]
# Action.GO_RIGHT = [0, 1, 0]

Action = namedtuple("Action", ["GO_FORWORD", "GO_LEFT", "GO_RIGHT"])(
    [1, 0, 0], [0, 0, 1], [0, 1, 0])

# Rewords
Reword = SimpleNamespace()
Reword.EAT_FOOD = 10
Reword.NONE = 0
Reword.GAME_OVER = -10

# State
# [ 0,0,0  Danger_Straight    Danger_Right    Denger_Left
#   0,0,0,0   Direction_Left    Direction_Right Direction_Up Direction_Down
#   0,0,0,0 ] Food_Left Food_Right Food_Up Food_Down

# State is a array off 0 and 1
MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LEARNING_RATE = 0.001
MAX_EPSILON = 80
GAMA = 0.9


class State:
    def __init__(self):
        self._danger = [1, 0, 0]
        self._direction = [1, 0, 0, 0]
        self._food_location = [1, 0, 0, 0]

    def set_danger(self,  is_collition):

        self._danger[0] = int(
            (self._direction[1] and is_collition[1]) or
            (self._direction[0] and is_collition[0]) or
            (self._direction[2] and is_collition[2]) or
            (self._direction[3] and is_collition[3])
        )
        self._danger[1] = int(

            (self._direction[2] and is_collition[1]) or
            (self._direction[3] and is_collition[0]) or
            (self._direction[0] and is_collition[2]) or
            (self._direction[1] and is_collition[3])
        )

        self._danger[2] = int(
            (self._direction[3] and is_collition[1]) or
            (self._direction[2] and is_collition[0]) or
            (self._direction[1] and is_collition[2]) or
            (self._direction[0] and is_collition[3])
        )

    def set_direction(self, direction):
        self._direction[0] = direction == Direction.LEFT
        self._direction[1] = direction == Direction.RIGHT
        self._direction[2] = direction == Direction.UP
        self._direction[3] = direction == Direction.DOWN

    def set_food_location(self, food_pos, head_pos):
        self._food_location[0] = (food_pos.x < head_pos.x)
        self._food_location[1] = (food_pos.y < head_pos.y)
        self._food_location[2] = (food_pos.x < head_pos.x)
        self._food_location[3] = (food_pos.y < head_pos.y)

    def flatten(self):
        return (self._danger + self._direction + self._food_location)

    @staticmethod
    def get_matrix_data(states):
        array = np.empty(0)
        for state in states:
            np.append(array, state.flatten())
            # state.flatten() -> list of integer
        # array should be like this
        # array ([ [1,2,3,4],
        #          [0,2,3,0],
        #          [1,2,3,5] ])
        return array
    # def array_to_state(self, array):
    #     pass


# print(Action[1])
