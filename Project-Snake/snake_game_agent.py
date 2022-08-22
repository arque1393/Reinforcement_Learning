import torch as torch
import numpy as np
from snake_game_environment import SnakeGameEnvironment
from collections import deque
from constants import Point, Direction
from RLConstants import Action, Reword, MAX_MEMORY, BATCH_SIZE, LEARNING_RATE


class Agent:
    def __init__(self) -> None:
        pass

    def get_state(self, game):
        pass

    def remember(self, state, action, reward, next_state, done):
        pass

    def train_long_memory(self):
        pass

    def train_short_memory(self):
        pass

    def get_action(self, state):
        pass


def train():
    pass


if __name__ == '__main__':
    train()
