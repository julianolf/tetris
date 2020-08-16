from os import path

TITLE = "TETRIS"
FPS = 30
BLOCK = 30
WIDTH = BLOCK * 16
AREA = BLOCK * 10
INFO = BLOCK * 11
HEIGHT = BLOCK * 20
WIN_SIZE = (WIDTH, HEIGHT)
BORDER = ((1, 1), (AREA - 1, 1), (AREA - 1, HEIGHT - 1), (1, HEIGHT - 1))
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ASSETS_PATH = path.join(path.dirname(__file__), "assets")
FONT = path.join(ASSETS_PATH, "font", "Teko-Regular.ttf")
SFX = path.join(ASSETS_PATH, "sfx")
SPRITE_SHEET = path.join(ASSETS_PATH, "img", "sprite_sheet.png")
SPRITE_SHEET_INFO = path.join(ASSETS_PATH, "img", "sprite_sheet.json")
