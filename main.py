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
from pytmx.util_pygame import load_pygame
from groups import AllSprites

class Game():
    def __init__(self):
        #pygame.init()# init pygame, causes freeze at start - neet to see if something goes wrong
        self.screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))# create screen
        pygame.display.set_caption('Vamp Survivor')
        self.clock = pygame.time.Clock()  # control framerate, control
        self.running = True
        self.FPS_target = FPS_TARGET
        #groups
        self.all_sprites = AllSprites()
        self.collision_sprites = AllSprites()
        #sprites
        self.setup()
        self.player = Player(self.all_sprites,WINDOW_WIDTH/2,WINDOW_HEIGHT/2,self.collision_sprites)

    def setup(self):
        map = load_pygame('data/maps/world.tmx')
        for obj in map.get_layer_by_name('Collisions'):# first ground collisions so will be invisible
            HiddenSprite((obj.x,obj.y),(obj.width,obj.height),(self.all_sprites,self.collision_sprites))
        for x,y,image in map.get_layer_by_name('Ground').tiles():# first ground to show on top
            GroundSprite((x*TILE_SIZE,y*TILE_SIZE),image,self.all_sprites)
        for obj in map.get_layer_by_name('Objects'):# then objects
            CollisionSprite((obj.x,obj.y),obj.image,(self.all_sprites,self.collision_sprites))


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
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()  # or flip - flip updates a part of the window , update the whole window
        pygame.quit()

if __name__ == '__main__':# to run only main file to avoid future messups
    game = Game()
    game.gameloop()
    pygame.quit()
