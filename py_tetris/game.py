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
        return piece(pygame.Vector2(x, y), self, (self.sprites,))

    def launch_piece(self):
        self.current = self.next
        self.current.gravity = settings.BLOCK
        self.next = self.new_piece()

    def stack(self):
        for block in self.current.blocks:
            block.add((self.sprites,))
            xy = tuple(block.position)
            column, line = xy[0] / settings.BLOCK, xy[1] / settings.BLOCK
            self.grid[int(line)][int(column)] = 1
            self.locked[xy] = block
        self.launch_piece()

    def reset(self):
        self.sprites.empty()
        self.grid = [[0 for _ in range(10)] for _ in range(20)]
        self.locked = {}
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
