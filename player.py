from Tools.demo.spreadsheet import center
from pygame.sprite import Sprite
from settings import *
from sprites import CollisionSprite


class Player(Sprite):
    def __init__(self, groups, x,y,collision_sprites):
        super().__init__(groups)
        self.load_images()
        self.state = 'down'
        self.frame_index = 0
        self.image = pygame.image.load('images/player/down/0.png').convert_alpha()
        self.rect = self.image.get_rect(center = (int(x),int(y)))
        self.hitbox_rect = self.rect.inflate(-60,-90)
        #movment
        self.speed = 500
        self.direction = pygame.math.Vector2()
        self.collision_sprites = collision_sprites

        self.walk_anim_speed = 7

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
        self.animate(dt)

    def load_images(self):
        self.frames = {"left":[], "right":[], "up":[], "down":[]}# frame dictionary
        for state in self.frames.keys():
            for folder_path, sub_folders, file_names in walk(join('images','player',state)):
                if file_names:
                    for file_name in sorted(file_names,key = lambda name: int(name.split('.')[0])):
                        full_path = join(folder_path, file_name)
                        self.frames[state].append(pygame.image.load(full_path).convert_alpha())
        print(self.frames)

    def animate(self,dt):
        # state check:
        if self.direction.x >0 : self.state = 'right'
        if self.direction.x < 0: self.state = 'left'
        if self.direction.y <0: self.state = 'up'
        if self.direction.y > 0: self.state = 'down'
        if self.direction:
            self.frame_index += self.walk_anim_speed * dt
        else : self.frame_index =0

        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]
