from pygame.sprite import Sprite

from settings import *


class CollisionSprite(Sprite):
    def __init__(self,pos,size,groups):
        super().__init__(groups)
        self.image = pygame.Surface(size)
        self.image.fill('blue')
        self.rect = self.image.get_rect(center = pos)
