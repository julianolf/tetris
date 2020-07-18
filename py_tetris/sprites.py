import pygame

from . import settings


class Piece(pygame.sprite.Sprite):
    def __init__(self, shapes, color, position, game, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shapes = shapes
        self.color = color
        self.position = position
        self.game = game
        self.rotation = 0
        self.last_move = 0
        self.gravity = 0
        self.draw()

    def left(self):
        self.position.x -= settings.BLOCK

    def right(self):
        self.position.x += settings.BLOCK

    def down(self):
        self.position.y += settings.BLOCK

    def rotate(self):
        self.rotation += 1

    def update(self):
        if not self.gravity:
            return
        if self.rect.bottom == settings.HEIGHT and self.gravity:
            self.gravity = 0
            self.game.launch_piece()
            return
        now = pygame.time.get_ticks()
        elapsed_time = now - self.last_move
        if elapsed_time > 1500:
            self.last_move = now
            self.position.y += self.gravity
        self.draw()

    def draw(self):
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
        super().__init__(shapes, settings.GREEN, position, *args, **kwargs)


class Z_(Piece):
    def __init__(self, position, *args, **kwargs):
        shapes = (((1, 1, 0), (0, 1, 1)), ((0, 1), (1, 1), (1, 0)))
        super().__init__(shapes, settings.RED, position, *args, **kwargs)


class I_(Piece):
    def __init__(self, position, *args, **kwargs):
        shapes = (((1, 1, 1, 1),), ((1,), (1,), (1,), (1,)))
        super().__init__(shapes, settings.CYAN, position, *args, **kwargs)


class O_(Piece):
    def __init__(self, position, *args, **kwargs):
        shapes = (((1, 1), (1, 1)),)
        super().__init__(shapes, settings.YELLOW, position, *args, **kwargs)


class J_(Piece):
    def __init__(self, position, *args, **kwargs):
        shapes = (
            ((1, 0, 0), (1, 1, 1)),
            ((1, 1), (1, 0), (1, 0)),
            ((1, 1, 1), (0, 0, 1)),
            ((0, 1), (0, 1), (1, 1)),
        )
        super().__init__(shapes, settings.BLUE, position, *args, **kwargs)


class L_(Piece):
    def __init__(self, position, *args, **kwargs):
        shapes = (
            ((0, 0, 1), (1, 1, 1)),
            ((1, 0), (1, 0), (1, 1)),
            ((1, 1, 1), (1, 0, 0)),
            ((1, 1), (0, 1), (0, 1)),
        )
        super().__init__(shapes, settings.ORANGE, position, *args, **kwargs)


class T_(Piece):
    def __init__(self, position, *args, **kwargs):
        shapes = (
            ((0, 1, 0), (1, 1, 1)),
            ((1, 0), (1, 1), (1, 0)),
            ((1, 1, 1), (0, 1, 0)),
            ((0, 1), (1, 1), (0, 1)),
        )
        super().__init__(shapes, settings.PURPLE, position, *args, **kwargs)
