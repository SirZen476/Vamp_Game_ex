from Tools.demo.spreadsheet import center
from pygame.sprite import Sprite
from settings import *
from sprites import CollisionSprite


class Player(Sprite):
    def __init__(self, groups, x,y,collision_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('images/player/down/0.png').convert_alpha()
        self.rect = self.image.get_rect(center = (int(x),int(y)))
        self.hitbox_rect = self.rect.inflate(-60,-80)
        #movment
        self.speed = 500
        self.direction = pygame.math.Vector2()
        self.collision_sprites = collision_sprites


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

    def collscreen(self):
        if (self.rect.bottom > WINDOW_HEIGHT and self.direction.y > 0) or (
                self.rect.top < 0 and self.direction.y < 0):
            self.direction.y = 0
        if (self.rect.right > WINDOW_WIDTH and self.direction.x > 0) or (
                self.rect.left < 0 and self.direction.x < 0):
            self.direction.x = 0

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = (int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT]))  # x direction
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])  # y direction
        #self.collscreen()# to collision with screen boundary
        if self.direction: self.direction.normalize()


    def move(self,dt):
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('x')#horizantal
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('y')#vertical
        self.rect.center = self.hitbox_rect.center



    def update(self,dt):
        self.input()
        self.move(dt)

