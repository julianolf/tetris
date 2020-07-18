import pygame

from . import settings, sprites


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(settings.TITLE)
        self.screen = pygame.display.set_mode(settings.WIN_SIZE)
        self.clock = pygame.time.Clock()
        self.sprites = pygame.sprite.Group()

    def reset(self):
        self.sprites.empty()
        self.current = sprites.S(pygame.Vector2(0, 0), (self.sprites,))
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
