from Tools.demo.spreadsheet import center
from pygame.sprite import Sprite

from settings import *

class Player(Sprite):
    def __init__(self, groups, x,y):
        super().__init__(groups)
        self.image = pygame.image.load('images/player/down/0.png').convert_alpha()
        self.rect = self.image.get_rect(center = (int(x),int(y)))
        #movment
        self.speed = 500
        self.direction = pygame.math.Vector2()
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
        self.collscreen()# to collision with screen boundary
        if self.direction: self.direction.normalize()


    def move(self,dt):
        self.rect.center += self.direction * self.speed * dt


    def update(self,dt):
        self.input()
        self.move(dt)

