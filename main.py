#this project uses files by CodeClear - https://github.com/clear-code-projects/5games

import random
import pygame
from Tools.scripts.dutree import display
from fontTools.merge.util import current_time
from sympy.core.random import randint ,choice
from random import randint, uniform
from pygame.sprite import Sprite
from settings import *
from player import Player
from sprites import *
from pytmx.util_pygame import load_pygame
from groups import AllSprites

class Game():
    def __init__(self):
        pygame.init()# init pygame, causes freeze at start - neet to see if something goes wrong
        self.screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))# create screen
        pygame.display.set_caption('Vamp Survivor')
        self.clock = pygame.time.Clock()  # control framerate, control
        self.running = True
        self.FPS_target = FPS_TARGET
        #groups
        self.all_sprites = AllSprites()
        self.collision_sprites = AllSprites()
        self.bullet_sprites = AllSprites()
        self.enemy_sprites = AllSprites()
        #hit timer for player
        self.last_hit = 0.0
        self.hp_cooldown = 1000
        self.font = pygame.font.Font('font/Oxanium-Bold.ttf', 30)

        # enemy timer
        self.enemy_event = pygame.event.custom_type()
        pygame.time.set_timer(self.enemy_event, 500)
        self.spawn_pos = []

        # setup
        self.load_audio()
        self.load_enemy_frames()
        self.setup()

    def load_audio(self):
        self.sound_impact = pygame.mixer.Sound('audio/impact.ogg')
        self.sound_shoot = pygame.mixer.Sound('audio/shoot.wav')
        self.sound_game = pygame.mixer.Sound('audio/music.wav')
        self.sound_game.set_volume(0.4)
        self.sound_game.play(loops=-1)

    def setup(self):
        map = load_pygame('data/maps/world.tmx')
        for obj in map.get_layer_by_name('Collisions'):# first ground collisions so will be invisible
            HiddenSprite((obj.x,obj.y),(obj.width,obj.height),(self.all_sprites,self.collision_sprites))

        for x,y,image in map.get_layer_by_name('Ground').tiles():# first ground to show on top
            GroundSprite((x*TILE_SIZE,y*TILE_SIZE),image,self.all_sprites)

        for obj in map.get_layer_by_name('Objects'):# then objects
            CollisionSprite((obj.x,obj.y),obj.image,(self.all_sprites,self.collision_sprites))

        for obj in map.get_layer_by_name(('Entities')):
            if(obj.name == 'Player'):
                self.player = Player(self.all_sprites, obj.x, obj.y, self.collision_sprites,self.enemy_sprites)
                self.gun = Gun(self.player,self.all_sprites,self.bullet_sprites)
            else:
                self.spawn_pos.append((obj.x,obj.y))

    def cooldown_check(self):# check if firing interval has passed.
        current_time = pygame.time.get_ticks()
        interval = current_time - self.last_hit
        if interval > self.hp_cooldown:
            return True
        else : return False

    def load_enemy_frames(self):
        self.frames = {"bat": [], "blob": [], "skeleton": [],}  # frame dictionary
        for state in self.frames.keys():
            for folder_path, sub_folders, file_names in walk(join('images', 'enemies', state)):
                if file_names:
                    for file_name in sorted(file_names, key=lambda name: int(name.split('.')[0])):
                        full_path = join(folder_path, file_name)
                        self.frames[state].append(pygame.image.load(full_path).convert_alpha())

    def collision_bullets_obj(self):
        for obj in self.collision_sprites:
            for bullet in self.bullet_sprites:
                if obj.rect.colliderect(bullet.rect):
                    bullet.kill()
                    self.sound_impact.play()

    def collision_bullet(self):
        for enemy in self.enemy_sprites:
            for bullet in self.bullet_sprites:
                if enemy.hitbox_rect.colliderect(bullet.rect):
                    enemy.kill()
                    bullet.kill()
                    self.sound_impact.play()
                    break

    def collision_enemy(self):
        for sprite in self.enemy_sprites:
            if sprite.hitbox_rect.colliderect(self.player.hitbox_rect) and self.cooldown_check():
                self.last_hit =pygame.time.get_ticks()
                self.sound_impact.play()
                if not self.player.hit_enemy():
                    self.running = False

    def gameloop(self):
        while self.running:
            #dt calc
            dt = self.clock.tick(self.FPS_target) /1000
            #event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                if event.type == self.enemy_event:
                    enemy_type = choice(["bat","blob","skeleton"])
                    Enemy(choice(self.spawn_pos),self.frames[enemy_type], self.player, (self.all_sprites,self.enemy_sprites),self.collision_sprites )
            #backround fill
            self.screen.fill('black')
            #update
            self.all_sprites.update(dt)
            self.collision_bullets_obj()#coll bullet with enviorment and collision sprites
            self.collision_bullet()#coll bullet enemy
            self.collision_enemy()#coll player, co

            #draw
            self.all_sprites.draw(self.player.rect.center)
            self.draw_hp()
            pygame.display.update()  # or flip - flip updates a part of the window , update the whole window
        pygame.quit()

    def draw_hp(self):
        hp_surt = self.font.render('health: ' + str(self.player.hp), True, 'red')
        hp_rect = hp_surt.get_rect(topleft=(10, 10))
        self.screen.blit(hp_surt, hp_rect)
        pygame.draw.rect(self.screen, 'red', hp_rect.inflate(20, 15), 5, 10)

if __name__ == '__main__':# to run only main file to avoid future messups
    game = Game()
    game.gameloop()
    pygame.quit()
