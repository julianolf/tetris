import pygame

from . import settings


class Piece(pygame.sprite.Sprite):
    def __init__(self, shapes, color, position, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shapes = shapes
        self.color = color
        self.position = position
        self.rotation = 0
        self.last_move = 0

    def left(self):
        self.position.x -= settings.BLOCK

    def right(self):
        self.position.x += settings.BLOCK

    def down(self):
        self.position.y += settings.BLOCK

    def rotate(self):
        self.rotation += 1

    def update(self):
        now = pygame.time.get_ticks()
        elapsed_time = now - self.last_move
        if elapsed_time > 1500:
            self.last_move = now
            self.position.y += settings.BLOCK
        shape = self.shapes[self.rotation % len(self.shapes)]
        rows = len(shape)
        cols = len(shape[0])
        size = (cols * settings.BLOCK, rows * settings.BLOCK)
        image = pygame.Surface(size)
        image.fill(settings.BLACK)
        image.set_colorkey(settings.BLACK)
        for x in range(rows):
            for y in range(cols):
                if shape[x][y]:
                    coord = (y * settings.BLOCK, x * settings.BLOCK)
                    block = (settings.BLOCK, settings.BLOCK)
                    rect = pygame.Rect(coord, block)
                    pygame.draw.rect(image, self.color, rect)
        self.image = image.convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position


class S(Piece):
    def __init__(self, position, *args, **kwargs):
        shapes = (((0, 1, 1), (1, 1, 0)), ((1, 0), (1, 1), (0, 1)))
        color = (0, 255, 0)
        super().__init__(shapes, color, position, *args, **kwargs)
