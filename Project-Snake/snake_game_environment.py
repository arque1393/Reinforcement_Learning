# Reset
# reward
# play (ACTION) -> Direction
# Game Iteration
# is_collition

import pygame
from random import randint
from constants import Direction, Colours, VELOCITY, BLOCK_SIZE, HEIGHT, WIDTH, Point, image_path
from RLConstants import Reward, Action
pygame.init()
font = pygame.font.SysFont('arial', 25)

bg_img = pygame.image.load(image_path)
bg_img = pygame.transform.scale(bg_img, (HEIGHT, WIDTH))


class SnakeGameEnvironment:
    def __init__(self, width=HEIGHT, height=WIDTH):
        self.width = width
        self.height = height
        # init display
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(((self.width/2)//BLOCK_SIZE)*BLOCK_SIZE,
                          ((self.width/2)//BLOCK_SIZE)*BLOCK_SIZE)
        self.snake = [self.head,
                      Point(self.head .x+BLOCK_SIZE, self.head .y),
                      Point(self.head .x+(2*BLOCK_SIZE), self.head .y)
                      ]

        self.score = 0
        self.food = None
        self._place_food()

        self.frame_iteration = 0

    def _place_food(self):
        x = randint(0, (self.width-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = randint(2, (self.height-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self, action):
        self.frame_iteration += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # 2. move
        self._move(action)  # update the head
        self.snake.insert(0, self.head)

        reward = Reward.NONE
        # 3. check if game over
        game_over = False
        if (self.is_collision() or self.frame_iteration > 100*len(self.snake)):
            game_over = True
            reward = Reward.GAME_OVER
            return game_over, self.score, reward

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1

            reward = Reward.EAT_FOOD
            self._place_food()
        else:
            self.snake.pop()

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(VELOCITY)
        # 6. return game over and score
        return game_over, self.score, reward

    def is_collision(self, point=None):
        if (point == None):
            point = self.head
        # hits boundary
        if (point.x > self.width - BLOCK_SIZE
                    or point.x < 0
                    or point.y > self.height - BLOCK_SIZE
                    or point.y < 2*BLOCK_SIZE
                    or point in self.snake[1:]
                ):
            return True
        # # hits itself
        # if point in self.snake[1:]:
        #     return True

        return False

    def _update_ui(self):
        self.display.fill(Colours.BLACK)
        self.display.blit(bg_img, (0, 2*BLOCK_SIZE))

        for pt in self.snake:
            pygame.draw.rect(self.display, Colours.BLUE1, pygame.Rect(
                pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.circle(self.display, Colours.BLUE2, (
                pt.x+BLOCK_SIZE/2, pt.y+BLOCK_SIZE/2), BLOCK_SIZE/2)

            # pygame.draw.rect(self.display, Colours.BLUE2,
            #                  pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        pygame.draw.rect(self.display, Colours.RED, pygame.Rect(
            self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, Colours.WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, action):

        # [Straight Right Left]
        clock_wise_directions = [
            Direction.RIGHT, Direction.DOWN,
            Direction.LEFT, Direction.UP
        ]
        index = clock_wise_directions.index(self.direction)

        if (action == Action.GO_RIGHT):
            self.direction = clock_wise_directions[(index+1) % 4]
        elif (action == Action.GO_LEFT):
            self.direction = clock_wise_directions[(index-1) % 4]
        else:
            pass

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)
