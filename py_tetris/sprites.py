import pygame

from . import settings


class Block(pygame.sprite.Sprite):
    def __init__(self, color, xy, *args, **kwargs):
        super().__init__(*args, **kwargs)
        w, h = (settings.BLOCK, settings.BLOCK)
        image = pygame.Surface((w, h))
        image.fill(settings.BLACK)
        image.set_colorkey(settings.BLACK)
        pygame.draw.rect(image, color, pygame.Rect((1, 1), (w - 2, h - 2)))
        self.image = image.convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = xy
        self.color = color
        self.x, self.y = xy

    def update(self):
        self.rect.topleft = (self.x, self.y)


class Piece(pygame.sprite.Sprite):
    def __init__(self, shapes, color, xy, game, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shapes = shapes
        self.color = color
        self.x, self.y = xy
        self.game = game
        self.rotation = 0
        self.last_move = 0
        self.falling = False
        self.draw()

    @property
    def shape(self):
        return self.shapes[self.rotation % len(self.shapes)]

    @property
    def positions(self):
        shape = self.shape
        for x in range(len(shape[0])):
            for y in range(len(shape)):
                if shape[y][x]:
                    yield (
                        x * settings.BLOCK + self.x,
                        y * settings.BLOCK + self.y,
                    )

    @property
    def blocks(self):
        return tuple(Block(self.color, p) for p in self.positions)

    def move(self, xy):
        self.x, self.y = xy
        self.rect.topleft = xy

    def left(self):
        if self.rect.left > 0:
            self.x -= settings.BLOCK
            if self.hit():
                self.x += settings.BLOCK

    def right(self):
        if self.rect.right < settings.AREA:
            self.x += settings.BLOCK
            if self.hit():
                self.x -= settings.BLOCK

    def down(self):
        if self.rect.bottom < settings.HEIGHT:
            self.y += settings.BLOCK
            if self.hit():
                self.y -= settings.BLOCK

    def rotate(self):
        self.rotation += 1
        if self.hit():
            self.rotation -= 1
        else:
            self.draw()

    def hit(self):
        return any(tuple(p) in self.game.locked for p in self.positions)

    def lock(self):
        self.game.stack()
        self.kill()

    def update(self):
        if not self.falling:
            return
        now = pygame.time.get_ticks()
        elapsed_time = now - self.last_move
        if elapsed_time > 1500:
            self.last_move = now
            if self.rect.bottom == settings.HEIGHT and self.falling:
                self.lock()
                return
            self.y += settings.BLOCK
        if self.rect.left < 0:
            self.x = 0
        if self.rect.right > settings.AREA:
            self.x = settings.AREA - self.rect.width
        if self.rect.bottom > settings.HEIGHT:
            self.y = settings.HEIGHT - self.rect.height
        if self.hit():
            self.y -= settings.BLOCK
            self.lock()
        self.rect.topleft = (self.x, self.y)

    def draw(self):
        shape = self.shape
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
        self.rect.topleft = (self.x, self.y)


class S_(Piece):
    def __init__(self, xy, *args, **kwargs):
        shapes = (((0, 1, 1), (1, 1, 0)), ((1, 0), (1, 1), (0, 1)))
        super().__init__(shapes, settings.GREEN, xy, *args, **kwargs)


class Z_(Piece):
    def __init__(self, xy, *args, **kwargs):
        shapes = (((1, 1, 0), (0, 1, 1)), ((0, 1), (1, 1), (1, 0)))
        super().__init__(shapes, settings.RED, xy, *args, **kwargs)


class I_(Piece):
    def __init__(self, xy, *args, **kwargs):
        shapes = (((1, 1, 1, 1),), ((1,), (1,), (1,), (1,)))
        super().__init__(shapes, settings.CYAN, xy, *args, **kwargs)


class O_(Piece):
    def __init__(self, xy, *args, **kwargs):
        shapes = (((1, 1), (1, 1)),)
        super().__init__(shapes, settings.YELLOW, xy, *args, **kwargs)


class J_(Piece):
    def __init__(self, xy, *args, **kwargs):
        shapes = (
            ((1, 0, 0), (1, 1, 1)),
            ((1, 1), (1, 0), (1, 0)),
            ((1, 1, 1), (0, 0, 1)),
            ((0, 1), (0, 1), (1, 1)),
        )
        super().__init__(shapes, settings.BLUE, xy, *args, **kwargs)


class L_(Piece):
    def __init__(self, xy, *args, **kwargs):
        shapes = (
            ((0, 0, 1), (1, 1, 1)),
            ((1, 0), (1, 0), (1, 1)),
            ((1, 1, 1), (1, 0, 0)),
            ((1, 1), (0, 1), (0, 1)),
        )
        super().__init__(shapes, settings.ORANGE, xy, *args, **kwargs)


class T_(Piece):
    def __init__(self, xy, *args, **kwargs):
        shapes = (
            ((0, 1, 0), (1, 1, 1)),
            ((1, 0), (1, 1), (1, 0)),
            ((1, 1, 1), (0, 1, 0)),
            ((0, 1), (1, 1), (0, 1)),
        )
        super().__init__(shapes, settings.PURPLE, xy, *args, **kwargs)
