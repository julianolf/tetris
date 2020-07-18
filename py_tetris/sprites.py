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
                    coord = (y * settings.BLOCK + 1, x * settings.BLOCK + 1)
                    block = (settings.BLOCK - 2, settings.BLOCK - 2)
                    rect = pygame.Rect(coord, block)
                    pygame.draw.rect(image, self.color, rect)
        self.image = image.convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position


class S_(Piece):
    def __init__(self, position, *args, **kwargs):
        shapes = (((0, 1, 1), (1, 1, 0)), ((1, 0), (1, 1), (0, 1)))
        color = (0, 255, 0)
        super().__init__(shapes, color, position, *args, **kwargs)


class Z_(Piece):
    def __init__(self, position, *args, **kwargs):
        shapes = (((1, 1, 0), (0, 1, 1)), ((0, 1), (1, 1), (1, 0)))
        color = (255, 0, 0)
        super().__init__(shapes, color, position, *args, **kwargs)


class I_(Piece):
    def __init__(self, position, *args, **kwargs):
        shapes = (((1, 1, 1, 1),), ((1,), (1,), (1,), (1,)))
        color = (0, 255, 255)
        super().__init__(shapes, color, position, *args, **kwargs)


class O_(Piece):
    def __init__(self, position, *args, **kwargs):
        shapes = (((1, 1), (1, 1)),)
        color = (255, 255, 0)
        super().__init__(shapes, color, position, *args, **kwargs)


class J_(Piece):
    def __init__(self, position, *args, **kwargs):
        shapes = (
            ((1, 0, 0), (1, 1, 1)),
            ((1, 1), (1, 0), (1, 0)),
            ((1, 1, 1), (0, 0, 1)),
            ((0, 1), (0, 1), (1, 1)),
        )
        color = (0, 0, 255)
        super().__init__(shapes, color, position, *args, **kwargs)


class L_(Piece):
    def __init__(self, position, *args, **kwargs):
        shapes = (
            ((0, 0, 1), (1, 1, 1)),
            ((1, 0), (1, 0), (1, 1)),
            ((1, 1, 1), (1, 0, 0)),
            ((1, 1), (0, 1), (0, 1)),
        )
        color = (255, 165, 0)
        super().__init__(shapes, color, position, *args, **kwargs)


class T_(Piece):
    def __init__(self, position, *args, **kwargs):
        shapes = (
            ((0, 1, 0), (1, 1, 1)),
            ((1, 0), (1, 1), (1, 0)),
            ((1, 1, 1), (0, 1, 0)),
            ((0, 1), (1, 1), (0, 1)),
        )
        color = (128, 0, 128)
        super().__init__(shapes, color, position, *args, **kwargs)
