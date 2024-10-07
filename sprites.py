import pygame
from pygame.sprite import Sprite

from settings import *


class CollisionSprite(Sprite):
    def __init__(self,pos,surf,groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)

class GroundSprite(Sprite):
    def __init__(self,pos,surf,groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.ground = True

class HiddenSprite(Sprite):
    def __init__(self,pos,size,groups):
        super().__init__(groups)
        self.image = pygame.Surface(size,pygame.SRCALPHA, 32)# extra to make it invisible
        self.rect = self.image.get_rect(topleft = pos)

class Gun(Sprite):
    def __init__(self,player,groups):
        self.player = player
        self.distance = 140
        self.player_direction = pygame.Vector2(1,0)
        self.angle = 0
        # sprite setup
        super().__init__(groups)
        self.gun_surface = pygame.image.load(join('images','gun','gun.png')).convert_alpha()
        self.bullet_surface = pygame.image.load(join('images', 'gun', 'bullet.png')).convert_alpha()
        self.image = self.gun_surface
        self.rect = self.image.get_rect(center = self.player.rect.center + self.player_direction* self.distance)

    def get_direction(self):
        #mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) # mouse pos
        #player_pos = WINDOW_WIDTH/2 ,WINDOW_HEIGHT/2 # player always in middle of screen
        return (pygame.Vector2(pygame.mouse.get_pos()) - (WINDOW_WIDTH/2 ,WINDOW_HEIGHT/2)).normalize()

    def update(self,_):
        self.player_direction = self.get_direction()
        self.angle = self.player_direction.angle_to(pygame.Vector2(1,0))
        self.image = pygame.transform.rotate(self.gun_surface,self.angle)
        self.rect.center=self.player.rect.center + self.player_direction * self.distance
