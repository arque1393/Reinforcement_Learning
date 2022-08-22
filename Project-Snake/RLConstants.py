from types import SimpleNamespace


# RL Constants

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


MAX_MEMORY = 100_00
BATCH_SIZE = 1000
LEARNING_RATE = 0.001
