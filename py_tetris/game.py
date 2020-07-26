import random

import pygame

from . import settings, sprites


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(settings.TITLE)
        self.screen = pygame.display.set_mode(settings.WIN_SIZE)
        self.clock = pygame.time.Clock()
        self.sprites = pygame.sprite.Group()
        self.pieces = (
            sprites.S_,
            sprites.Z_,
            sprites.I_,
            sprites.O_,
            sprites.J_,
            sprites.L_,
            sprites.T_,
        )

    def new_piece(self):
        piece = random.choice(self.pieces)
        x = settings.BLOCK * 4
        y = settings.BLOCK * -2
        return piece((x, y), self, (self.sprites,))

    def launch_piece(self):
        self.current = self.next
        self.current.falling = True
        self.next = self.new_piece()

    def stack(self):
        for block in self.current.blocks:
            block.add((self.sprites,))
            xy = (block.x, block.y)
            column, line = xy[0] // settings.BLOCK, xy[1] // settings.BLOCK
            self.grid[line][column] = xy
            self.locked[xy] = block
        self.check_lines()
        self.launch_piece()

    def check_lines(self):
        removed = 0
        for i, line in enumerate(self.grid):
            if all(line):
                for j, xy in enumerate(line):
                    self.locked[xy].kill()
                    self.locked.pop(xy)
                    self.grid[i][j] = 0
                removed += 1
                for k in range(i - 1, -1, -1):
                    if any(self.grid[k]):
                        for l in range(10):
                            if self.grid[k][l]:
                                pos = self.grid[k][l]
                                self.grid[k][l] = 0
                                block = self.locked.pop(pos)
                                block.y += settings.BLOCK
                                xy = (block.x, block.y)
                                column = xy[0] // settings.BLOCK
                                line = xy[1] // settings.BLOCK
                                self.grid[line][column] = xy
                                self.locked[xy] = block
        if removed:
            self.lines += removed
            self.score += (10 * removed) * removed

    def reset(self):
        self.sprites.empty()
        self.grid = [[0 for _ in range(10)] for _ in range(20)]
        self.locked = {}
        self.lines = 0
        self.score = 0
        self.next = self.new_piece()
        self.launch_piece()
        self.running = True

    def update(self):
        self.sprites.update()

    def draw(self):
        self.screen.fill(settings.BLACK)
        self.sprites.draw(self.screen)
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.current.left()
                    return
                if event.key == pygame.K_RIGHT:
                    self.current.right()
                    return
                if event.key == pygame.K_DOWN:
                    self.current.down()
                    return
                if event.key == pygame.K_UP:
                    self.current.rotate()
                    return

    def loop(self):
        while self.running:
            self.update()
            self.draw()
            self.events()

    def run(self):
        self.reset()
        self.loop()
        pygame.quit()


def main():
    Game().run()


if __name__ == '__main__':
    main()
