import pygame as pg
import os

# Khởi tạo pygame
pg.init()
pg.mixer.init()

# Cấu hình cửa sổ
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
WINDOW_TITLE = "Snake Game"

# Màu sắc
COLORS = {
    'WHITE': (255, 255, 255),
    'BLACK': (0, 0, 0),
    'RED': (255, 0, 0),
    'YELLOW': (255, 255, 0),
    'GREEN': (96, 165, 111),
    'BLUE': (0, 0, 255),
    'LIGHT_BLUE': (226, 247, 184),
    'ORANGE': (255, 140, 0),
    'BROWN': (165, 42, 42),
    'PURPLE': (128, 0, 128),
    'PINK': (255, 192, 203)
}

# Cấu hình game
GAME_CONFIG = {
    'GRID_SIZE': 20,
    'BORDER_SIZE': 35,
    'INITIAL_SNAKE_LENGTH': 3,
    'SPEEDS': {
        'EASY': 10,
        'MEDIUM': 15,
        'HARD': 20
    }
}

# Đường dẫn
PATHS = {
    'SOUNDS': os.path.join('assets', 'sounds'),
    'FONTS': os.path.join('assets', 'fonts'),
    'IMAGES': os.path.join('assets', 'images')
}

# Tạo cửa sổ game
screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pg.display.set_caption(WINDOW_TITLE)

# Font chữ
FONTS = {
    'SMALL': pg.font.SysFont('arial', 20),
    'MEDIUM': pg.font.SysFont('arial', 30),
    'LARGE': pg.font.SysFont('arial', 50)
}

# Khởi tạo âm thanh
SOUNDS = {}
try:
    SOUNDS = {
        'EAT': pg.mixer.Sound(os.path.join(PATHS['SOUNDS'], 'Snake_eat.wav')),
        'CLICK': pg.mixer.Sound(os.path.join(PATHS['SOUNDS'], 'click.wav')),
        'GAME_OVER': pg.mixer.Sound(os.path.join(PATHS['SOUNDS'], 'game_over.wav')),
        'MENU': pg.mixer.Sound(os.path.join(PATHS['SOUNDS'], 'menu.wav'))
    }
except:
    print("Không thể tải âm thanh")

# Tạo thư mục assets nếu chưa tồn tại
for path in PATHS.values():
    if not os.path.exists(path):
        os.makedirs(path) 