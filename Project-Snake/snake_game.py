import pygame
from random import randint
from constants import Direction, Colours, VELOCITY, BLOCK_SIZE, HEIGHT, WIDTH, Point, image_path

pygame.init()
font = pygame.font.SysFont('arial', 25)

bg_img = pygame.image.load(image_path)
bg_img = pygame.transform.scale(bg_img, (HEIGHT, WIDTH))


class SnakeGame:
    def __init__(self, width=HEIGHT, height=WIDTH):
        self.width = width
        self.height = height
        # init display
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()

        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(((self.width/2)//BLOCK_SIZE)*BLOCK_SIZE,
                          ((self.width/2)//BLOCK_SIZE)*BLOCK_SIZE)
        self.snake = [self.head,
                      Point(self.head .x-BLOCK_SIZE, self.head .y),
                      Point(self.head .x-(2*BLOCK_SIZE), self.head .y)]

        self.score = 0
        self.food = None
        self._place_food()

    def _place_food(self):
        x = randint(0, (self.width-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = randint(2, (self.height-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self):
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN

        # 2. move
        self._move(self.direction)  # update the head
        self.snake.insert(0, self.head)

        # 3. check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(VELOCITY)
        # 6. return game over and score
        return game_over, self.score

    def _is_collision(self):
        # hits boundary
        if self.head.x > self.width - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.height - BLOCK_SIZE or self.head .y < 2*BLOCK_SIZE:
            return True
        # hits itself
        if self.head in self.snake[1:]:
            return True

        return False

    def _update_ui(self):
        self.display.fill(Colours.BLACK)
        self.display.blit(bg_img, (0, 2*BLOCK_SIZE))

        for pt in self.snake:
            # pygame.draw.rect(self.display, Colours.BLUE1, pygame.Rect(
            #     pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.circle(self.display, Colours.BLUE1, (
                pt.x+BLOCK_SIZE/2, pt.y+BLOCK_SIZE/2), BLOCK_SIZE/2)

            # pygame.draw.rect(self.display, Colours.BLUE2,
            #                  pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        pygame.draw.rect(self.display, Colours.RED, pygame.Rect(
            self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, Colours.WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)


def main_loop():
    game = SnakeGame()

    # game loop
    while True:
        game_over, score = game.play_step()

        if game_over == True:
            break

    print('Final Score', score)

    pygame.quit()


if __name__ == '__main__':
    main_loop()
