import torch as torch
import numpy as np
import random

from model import Linear_QNet, QTrainer

from snake_game_environment import SnakeGameEnvironment
from collections import deque
from constants import Point, Direction, BLOCK_SIZE
from RLConstants import Action, MAX_MEMORY, BATCH_SIZE, MAX_EPSILON, LEARNING_RATE, State, GAMA


class Agent:
    def __init__(self) -> None:
        self.n_game = 0
        self.epsilon = 0  # Randomness
        self.gama = GAMA   # Discount Factor

        # if full autometicly call pop left
        self.memory = deque(maxlen=MAX_MEMORY)

        # Model and trainer
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(
            self.model, learning_rate=LEARNING_RATE, gama=GAMA)

    def get_state(self, environment: SnakeGameEnvironment):
        state = State()
        head = environment.head

        collision_info = [
            environment.is_collision(Point(head.x-BLOCK_SIZE, head.y)),
            environment.is_collision(Point(head.x+BLOCK_SIZE, head.y)),
            environment.is_collision(Point(head.x, head.y-BLOCK_SIZE)),
            environment.is_collision(Point(head.x, head.y+BLOCK_SIZE)),
        ]

        state.set_danger(collision_info)
        state.set_direction(environment.direction)
        state.set_food_location(environment.food, head)

        return state

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)

        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state: State):
        self.epsilon = MAX_EPSILON - self.n_game
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)  # Exploration
        else:
            state0 = torch.tensor(state.flatten(), dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()

        return Action[move]


def train():
    plot_score = []
    mean_score = []
    total_score = 0
    record = 0
    agent = Agent()
    game_environment = SnakeGameEnvironment()
    while True:
        # get old state
        old_state = agent.get_state(game_environment)
        # final move
        final_move = agent.get_action(old_state)
        # perform move and get new state
        done, score, reward = game_environment.play_step(final_move)
        new_state = agent.get_state(game_environment)
        # short memory trsin
        agent.train_short_memory(
            old_state, final_move, reward, new_state, done)
        # remember
        agent.remember(old_state, final_move, reward, new_state, done)

        if done:
            # train Long memory
            game_environment.reset()
            agent.n_game = + 1
            agent.train_long_memory()
            if score > record:
                record = score
                # agent.model.save()

            print("Game :", game_environment.n_game,
                  "Score :", score,
                  "Record :", record)


if __name__ == '__main__':
    train()
