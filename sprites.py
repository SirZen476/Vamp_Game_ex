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

class HiddenSprite(Sprite):
    def __init__(self,pos,size,groups):
        super().__init__(groups)
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(topleft = pos)