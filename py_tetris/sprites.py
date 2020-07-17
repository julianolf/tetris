import pygame

from . import settings


class Block(pygame.sprite.Sprite):
    def __init__(self, color, pos, *args, **kwargs):
        super().__init__(*args, **kwargs)
        size = (settings.BLOCK, settings.BLOCK)
        image = pygame.Surface(size)
        image.fill(settings.BLACK)
        image.set_colorkey(settings.BLACK)
        pygame.draw.rect(image, color, pygame.Rect((0, 0), size))
        self.image = image.convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.color = color
