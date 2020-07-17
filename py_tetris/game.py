import pygame


def main():
    pygame.init()
    pygame.display.set_caption('PyTETRIS')
    pygame.display.set_mode((300, 600))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

    pygame.quit()


if __name__ == '__main__':
    main()
