import pygame

from . import settings


class Block(pygame.sprite.Sprite):
    def __init__(self, color, position, *args, **kwargs):
        super().__init__(*args, **kwargs)
        w, h = (settings.BLOCK, settings.BLOCK)
        image = pygame.Surface((w, h))
        image.fill(settings.BLACK)
        image.set_colorkey(settings.BLACK)
        pygame.draw.rect(image, color, pygame.Rect((1, 1), (w - 2, h - 2)))
        self.image = image.convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = (position.x, position.y)
        self.color = color
        self.position = position


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

    @property
    def shape(self):
        return self.shapes[self.rotation % len(self.shapes)]

    @property
    def positions(self):
        for x in range(len(self.shape[0])):
            for y in range(len(self.shape)):
                if self.shape[y][x]:
                    yield pygame.Vector2(
                        x * settings.BLOCK + self.position.x,
                        y * settings.BLOCK + self.position.y,
                    )

    @property
    def blocks(self):
        return tuple(Block(self.color, p) for p in self.positions)

    def left(self):
        if self.rect.left > 0:
            self.position.x -= settings.BLOCK
            if self.hit():
                self.position.x += settings.BLOCK

    def right(self):
        if self.rect.right < settings.WIDTH:
            self.position.x += settings.BLOCK
            if self.hit():
                self.position.x -= settings.BLOCK

    def down(self):
        if self.rect.bottom < settings.HEIGHT:
            self.position.y += settings.BLOCK
            if self.hit():
                self.position.y -= settings.BLOCK

    def rotate(self):
        self.rotation += 1
        if self.hit():
            self.rotation -= 1

    def hit(self):
        return any(tuple(p) in self.game.locked for p in self.positions)

    def lock(self):
        self.game.stack()
        self.kill()

    def update(self):
        if not self.gravity:
            return
        now = pygame.time.get_ticks()
        elapsed_time = now - self.last_move
        if elapsed_time > 1500:
            self.last_move = now
            if self.rect.bottom == settings.HEIGHT and self.gravity:
                self.lock()
                return
            self.position.y += self.gravity
        if self.rect.left < 0:
            self.position.x = 0
        if self.rect.right > settings.WIDTH:
            self.position.x = settings.WIDTH - self.rect.width
        if self.rect.bottom > settings.HEIGHT:
            self.position.y = settings.HEIGHT - self.rect.height
        if self.hit():
            self.position.y -= self.gravity
            self.game.stack()
            self.kill()
        self.draw()

    def draw(self):
        rows = len(self.shape)
        cols = len(self.shape[0])
        size = (cols * settings.BLOCK, rows * settings.BLOCK)
        image = pygame.Surface(size)
        image.fill(settings.BLACK)
        image.set_colorkey(settings.BLACK)
        for x in range(rows):
            for y in range(cols):
                if self.shape[x][y]:
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
