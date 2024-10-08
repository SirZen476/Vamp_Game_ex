import pygame
from fontTools.merge.util import current_time
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
    def __init__(self,player,groups,bullet_group):
        self.player = player
        self.distance = 140
        self.player_direction = pygame.Vector2(1,0)
        self.angle = 0
        self.groups = groups
        self.bullet_group = bullet_group
        # sprite setup
        super().__init__(groups)
        self.gun_surface = pygame.image.load(join('images','gun','gun.png')).convert_alpha()
        self.image = self.gun_surface
        self.rect = self.image.get_rect(center = self.player.rect.center + self.player_direction* self.distance)
        self.last_shot = 0.0
        self.cooldown = 400

    def cooldown_check(self):# check if firing interval has passed.
        current_time = pygame.time.get_ticks()
        interval = current_time - self.last_shot
        if interval > self.cooldown:
            return True
        else : return False

    def get_direction(self):
        #mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) # mouse pos
        #player_pos = WINDOW_WIDTH/2 ,WINDOW_HEIGHT/2 # player always in middle of screen
        return (pygame.Vector2(pygame.mouse.get_pos()) - (WINDOW_WIDTH/2 ,WINDOW_HEIGHT/2)).normalize()

    def input(self):
        mouse_in = pygame.mouse.get_pressed()
        if(mouse_in[0] and self.cooldown_check()):
            bullet( (self.groups, self.bullet_group), self)
            self.last_shot = pygame.time.get_ticks()

    def rotate_gun(self):
        self.player_direction = self.get_direction()
        self.rect.center = self.player.rect.center + self.player_direction * self.distance  # place the gun
        if self.rect.centerx > self.player.rect.centerx:
            self.angle = self.player_direction.angle_to(pygame.Vector2(1, 0))
            self.image = pygame.transform.rotate(self.gun_surface, self.angle)
        else:
            self.image = pygame.transform.flip(self.gun_surface, True, False)# rotate
            self.angle = self.player_direction.angle_to(pygame.Vector2(-1, 0))
            self.image = pygame.transform.rotate(self.image, self.angle)


    def update(self,_):
        self.rotate_gun()
        self.input()

class bullet(Sprite):
    def __init__(self,groups,gun):
        super().__init__(groups)
        self.direction = gun.player_direction
        self.image = pygame.image.load(join('images', 'gun', 'bullet.png')).convert_alpha()
        self.image = pygame.transform.rotate(self.image,self.direction.angle_to(pygame.Vector2(1,0)))
        self.rect = self.image.get_rect(center = gun.rect.center + gun.player_direction *50)
        self.speed = 1500
        self.ttd = 1500
        self.spawn_time = pygame.time.get_ticks()


    def update(self,dt):
        curr_time =  pygame.time.get_ticks()
        if (curr_time -self.spawn_time) > self.ttd:
            self.kill()
        self.rect.x += self.direction.x * self.speed * dt
        self.rect.y += self.direction.y * self.speed * dt


class Enemy(Sprite):
    def __init__(self,pos,frames,player, groups,collision_sprites):
        super().__init__(groups)
        self.player = player
        #image
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.walk_anim_speed = 7

        #rect
        self.rect = self.image.get_rect(center = pos)
        self.hitbox_rect = self.rect.inflate(-20,-40)
        self.collision_sprites = collision_sprites
        self.direction = pygame.Vector2()
        self.speed = 350

    def collision(self,direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'x':
                    if self.direction.x >0:# right side coll
                        self.hitbox_rect.right = sprite.rect.left#
                    elif self.direction.x <0:# left side coll
                        self.hitbox_rect.left = sprite.rect.right
                if direction == 'y':
                    if self.direction.y >0:# right side coll
                        self.hitbox_rect.bottom = sprite.rect.top
                    elif self.direction.y <0:# left side coll
                        self.hitbox_rect.top = sprite.rect.bottom  #

    def move(self,dt):
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('x')#horizantal
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('y')#vertical
        self.rect.center = self.hitbox_rect.center

    def update(self,dt):
        # move to player here

        self.direction = pygame.Vector2(-self.rect.centerx + self.player.rect.centerx,-self.rect.centery + self.player.rect.centery)
        if self.direction: self.direction = self.direction.normalize()
        self.move(dt)
        self.animate(dt)

    def animate(self,dt):
        # state check:
        if self.direction.x >0 : self.state = 'right'
        if self.direction.x < 0: self.state = 'left'
        if self.direction.y <0: self.state = 'up'
        if self.direction.y > 0: self.state = 'down'
        if self.direction:
            self.frame_index += self.walk_anim_speed * dt
        else : self.frame_index =0

        self.image = self.frames[int(self.frame_index) % len(self.frames)]




