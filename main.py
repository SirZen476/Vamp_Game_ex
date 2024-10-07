#this project uses files by CodeClear - https://github.com/clear-code-projects/5games

import random
import pygame
from Tools.scripts.dutree import display
from fontTools.merge.util import current_time
from sympy.core.random import randint
from random import randint, uniform
from pygame.sprite import Sprite
from settings import *
from player import Player
from sprites import *

class Game():
    def __init__(self):
        #pygame.init()# init pygame, causes freeze at start - neet to see if something goes wrong
        self.screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))# create screen
        pygame.display.set_caption('Vamp Survivor')
        self.clock = pygame.time.Clock()  # control framerate, control
        self.running = True
        self.FPS_target = FPS_TARGET
        #groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        #sprites
        self.player = Player(self.all_sprites,WINDOW_WIDTH/2,WINDOW_HEIGHT/2)
        for i in range(6):# for collision test
            pos = (randint(0,WINDOW_WIDTH),randint(0,WINDOW_HEIGHT))
            size = (randint(50,100),randint(50,100))
            CollisionSprite(pos,size ,self.all_sprites)

    def gameloop(self):
        while self.running:
            #dt calc
            dt = self.clock.tick(self.FPS_target) /1000
            #event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
            #backround fill
            self.screen.fill('black')
            #update
            self.all_sprites.update(dt)
            #draw
            self.all_sprites.draw(self.screen)
            pygame.display.update()  # or flip - flip updates a part of the window , update the whole window
        pygame.quit()

if __name__ == '__main__':# to run only main file to avoid future messups
    game = Game()
    game.gameloop()
    pygame.quit()
