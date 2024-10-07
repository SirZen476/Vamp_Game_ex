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
        self.groups = groups
        # sprite setup
        super().__init__(groups)
        self.gun_surface = pygame.image.load(join('images','gun','gun.png')).convert_alpha()
        self.image = self.gun_surface
        self.rect = self.image.get_rect(center = self.player.rect.center + self.player_direction* self.distance)

    def get_direction(self):
        #mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) # mouse pos
        #player_pos = WINDOW_WIDTH/2 ,WINDOW_HEIGHT/2 # player always in middle of screen
        return (pygame.Vector2(pygame.mouse.get_pos()) - (WINDOW_WIDTH/2 ,WINDOW_HEIGHT/2)).normalize()

    def input(self):
        mouse_in = pygame.mouse.get_pressed()
        if(mouse_in[0]):
            bullet(self.groups,self)


    def update(self,_):
        self.player_direction = self.get_direction()
        self.angle = self.player_direction.angle_to(pygame.Vector2(1,0))
        self.image = pygame.transform.rotate(self.gun_surface,self.angle)
        self.rect.center=self.player.rect.center + self.player_direction * self.distance
        self.input()

class bullet(Sprite):
    def __init__(self,groups,gun):
        super().__init__(groups)
        self.direction = gun.player_direction
        self.image = pygame.image.load(join('images', 'gun', 'bullet.png')).convert_alpha()
        self.image = pygame.transform.rotate(self.image,self.direction.angle_to(pygame.Vector2(1,0)))
        self.rect = self.image.get_rect(center = gun.rect.center + gun.player_direction *20)
        self.speed = 1000


    def update(self,dt):
        self.rect.x += self.direction.x * self.speed * dt
        self.rect.y += self.direction.y * self.speed * dt



