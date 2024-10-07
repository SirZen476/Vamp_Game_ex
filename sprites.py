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