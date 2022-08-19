# imports
import pygame
import random

pygame.init() # init

class SnakeGame:
    def __init__(self, w=640, h=480):
        self.w=w
        self.h=h
        # init Display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        # imit Game State 
    
    def play_step(self):
        pass 





#main
def main():
    game = SnakeGame()

    #Game Loop
    while True:
        game.play_step()

        # if game over break

    pygame.quit()

if __name__ == '__main__':
    main()