#this project uses files by CodeClear - https://github.com/clear-code-projects/5games

import random
import pygame
from Tools.scripts.dutree import display
from fontTools.merge.util import current_time
from sympy.core.random import randint
from random import randint, uniform
from pygame.sprite import Sprite
from settings import *

class Game():
    def __init__(self):
        #pygame.init()# init pygame, causes freeze at start - neet to see if something goes wrong
        self.screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))# create screen
        pygame.display.set_caption('Vamp Survivor')
        self.clock = pygame.time.Clock()  # control framerate, control
        self.running = True
        self.FPS_target = FPS_TARGET

    def gameloop(self):
        while self.running:
            #dt calc
            dt = self.clock.tick(self.FPS_target) /1000
            #event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.screen.fill('blue')

            #update

            #draw
            pygame.display.update()  # or flip - flip updates a part of the window , update the whole window
        pygame.quit()

class Player(Sprite):
    def __init__(self,groups):
        super().__init__(groups)


if __name__ == '__main__':# to run only main file to avoid future messups
    game = Game()
    game.gameloop()
