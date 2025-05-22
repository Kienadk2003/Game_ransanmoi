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
    'WINDOW_SIZE': (800, 600),
    'GRID_SIZE': 20,
    'BORDER_SIZE': 20,
    'INITIAL_SNAKE_LENGTH': 3,
    'SPEEDS': {
        'EASY': 10,
        'MEDIUM': 15,
        'HARD': 20
    },
    'SPEED_BOOST': {
        'POINTS_THRESHOLD': 15,  # Số điểm cần để tăng tốc
        'SPEED_INCREASE': 5,     # Số đơn vị tăng tốc
        'DURATION': 300          # Thời gian tăng tốc (frames)
    },
    'BOMB_MODE': {
        'BOMB_COUNT': 5,  # Số lượng bom ban đầu
        'BOMB_SIZE': 2,   # Kích thước bom
        'SCORE_PENALTY': 5,  # Số điểm bị trừ khi chạm bom
        'SPEED_INCREASE': {
            '15_POINTS': 5,   # Tăng tốc độ khi đạt 15 điểm
            '30_POINTS': 10,  # Tăng tốc độ khi đạt 30 điểm
        },
        'ANIMATION': {
            'BLINK_SPEED': 0.1,    # Tốc độ nhấp nháy (thấp hơn = nhấp nháy chậm hơn)
            'GLOW_SIZE': 8,        # Kích thước hiệu ứng phát sáng
            'GLOW_SPEED': 0.05,    # Tốc độ hiệu ứng phát sáng
            'ALPHA_MIN': 50,       # Độ trong suốt tối thiểu
            'ALPHA_MAX': 255       # Độ trong suốt tối đa
        },
        'BOMB_POSITIONS': {
            'INITIAL': [  # 5 vị trí bom ban đầu
                (200, 200),
                (600, 200),
                (400, 400),
                (200, 600),
                (600, 600)
            ],
            '15_POINTS': [  # 7 vị trí bom khi đạt 15 điểm
                (200, 200),
                (600, 200),
                (400, 400),
                (200, 600),
                (600, 600),
                (300, 300),
                (500, 500)
            ],
            '30_POINTS': [  # 10 vị trí bom khi đạt 30 điểm
                (200, 200),
                (600, 200),
                (400, 400),
                (200, 600),
                (600, 600),
                (300, 300),
                (500, 500),
                (150, 450),
                (450, 150),
                (450, 450)
            ]
        }
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