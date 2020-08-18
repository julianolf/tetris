import pygame

from . import settings


class Block(pygame.sprite.Sprite):
    def __init__(self, image, xy, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = xy
        self.x, self.y = xy

    def update(self):
        self.rect.topleft = (self.x, self.y)


class Piece(pygame.sprite.Sprite):
    def __init__(self, xy, game, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        return tuple(Block(self.img, p) for p in self.positions)

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
            self.game.sfx["rotate"].play()

    def drop(self):
        while self.y < settings.HEIGHT - settings.BLOCK:
            self.y += settings.BLOCK
            if self.hit():
                self.y -= settings.BLOCK
                break

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
        if elapsed_time > self.game.speed:
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
                    coord = (y * settings.BLOCK, x * settings.BLOCK)
                    image.blit(self.img, coord)
        self.image = image.convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)


class S_(Piece):
    def __init__(self, xy, game, *args, **kwargs):
        self.shapes = (((0, 1, 1), (1, 1, 0)), ((1, 0), (1, 1), (0, 1)))
        self.img = game.get_image("sqr03.png")
        super().__init__(xy, game, *args, **kwargs)


class Z_(Piece):
    def __init__(self, xy, game, *args, **kwargs):
        self.shapes = (((1, 1, 0), (0, 1, 1)), ((0, 1), (1, 1), (1, 0)))
        self.img = game.get_image("sqr01.png")
        super().__init__(xy, game, *args, **kwargs)


class O_(Piece):
    def __init__(self, xy, game, *args, **kwargs):
        self.shapes = (((1, 1), (1, 1)),)
        self.img = game.get_image("sqr07.png")
        super().__init__(xy, game, *args, **kwargs)


class J_(Piece):
    def __init__(self, xy, game, *args, **kwargs):
        self.shapes = (
            ((1, 0, 0), (1, 1, 1)),
            ((1, 1), (1, 0), (1, 0)),
            ((1, 1, 1), (0, 0, 1)),
            ((0, 1), (0, 1), (1, 1)),
        )
        self.img = game.get_image("sqr08.png")
        super().__init__(xy, game, *args, **kwargs)


class L_(Piece):
    def __init__(self, xy, game, *args, **kwargs):
        self.shapes = (
            ((0, 0, 1), (1, 1, 1)),
            ((1, 0), (1, 0), (1, 1)),
            ((1, 1, 1), (1, 0, 0)),
            ((1, 1), (0, 1), (0, 1)),
        )
        self.img = game.get_image("sqr09.png")
        super().__init__(xy, game, *args, **kwargs)


class T_(Piece):
    def __init__(self, xy, game, *args, **kwargs):
        self.shapes = (
            ((0, 1, 0), (1, 1, 1)),
            ((1, 0), (1, 1), (1, 0)),
            ((1, 1, 1), (0, 1, 0)),
            ((0, 1), (1, 1), (0, 1)),
        )
        self.img = game.get_image("sqr02.png")
        super().__init__(xy, game, *args, **kwargs)


class I_(Piece):
    def __init__(self, xy, game, *args, **kwargs):
        self.shapes = (((1, 1, 1, 1),), ((1,), (1,), (1,), (1,)))
        self.img = [
            game.get_image("sqr04.png"),
            game.get_image("sqr05.png"),
            game.get_image("sqr06.png"),
            game.get_image("sqr14.png"),
            game.get_image("sqr15.png"),
            game.get_image("sqr16.png"),
        ]
        super().__init__(xy, game, *args, **kwargs)

    @property
    def blocks(self):
        imgs = self.img[:3] if len(self.shape) == 1 else self.img[3:]
        idx = (0, 1, 1, 2)
        return tuple(
            Block(imgs[idx[i]], p) for i, p in enumerate(self.positions)
        )

    def draw(self):
        shape = self.shape
        rows = len(shape)
        cols = len(shape[0])
        size = (cols * settings.BLOCK, rows * settings.BLOCK)
        image = pygame.Surface(size)
        image.fill(settings.BLACK)
        image.set_colorkey(settings.BLACK)
        imgs = self.img[:3] if rows == 1 else self.img[3:]
        coords = [
            (y * settings.BLOCK, x * settings.BLOCK)
            for x in range(rows)
            for y in range(cols)
        ]
        image.blit(imgs[0], coords[0])
        image.blit(imgs[1], coords[1])
        image.blit(imgs[1], coords[2])
        image.blit(imgs[2], coords[3])
        self.image = image.convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)


class SplashScreen(pygame.sprite.Sprite):
    def __init__(self, text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        image = pygame.Surface(settings.WIN_SIZE)
        image.fill(settings.BLACK)
        image.set_colorkey(settings.BLACK)
        screen_center = (settings.WIDTH / 2, settings.HEIGHT / 2)
        font_big = pygame.font.Font(settings.FONT, 80)
        title = font_big.render(text, True, settings.WHITE)
        title_rect = title.get_rect()
        title_rect.midbottom = screen_center
        font_small = pygame.font.Font(settings.FONT, 30)
        hint = font_small.render("Press any key to play", True, settings.WHITE)
        hint_rect = hint.get_rect()
        hint_rect.midtop = screen_center
        image.blit(title, title_rect)
        image.blit(hint, hint_rect)
        self.image = image.convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
