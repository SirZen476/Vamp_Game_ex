import pygame.sprite

from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def draw(self, player_center):
        self.offset.x = - player_center[0] + WINDOW_WIDTH/2
        self.offset.y = - player_center[1] + WINDOW_HEIGHT/2
        ground_sprites = [sprite for sprite in self if hasattr(sprite,'ground')]
        object_sprites = [sprite for sprite in self if not hasattr(sprite,'ground')]

        for layer in  [ground_sprites,object_sprites]:
            for sprite in sorted(layer,key = lambda sprite :  sprite.rect.centery):
              self.screen.blit(sprite.image,sprite.rect.topleft + self.offset)# topleft pos

