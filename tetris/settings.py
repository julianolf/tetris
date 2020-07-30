from os import path

TITLE = 'TETRIS'
BLOCK = 30
WIDTH = BLOCK * 16
AREA = BLOCK * 10
INFO = BLOCK * 11
HEIGHT = BLOCK * 20
WIN_SIZE = (WIDTH, HEIGHT)
BORDER = ((1, 1), (AREA - 1, 1), (AREA - 1, HEIGHT - 1), (1, HEIGHT - 1))
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
ASSETS_PATH = path.join(path.dirname(__file__), 'assets')
FONT = path.join(ASSETS_PATH, 'font', 'Teko-Regular.ttf')
SFX = path.join(ASSETS_PATH, 'sfx')
