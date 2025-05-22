import pygame as pg
import random
import math
from init import *

class Bomb:
    def __init__(self, game=None):
        self.game = game
        self.size = GAME_CONFIG['BOMB_MODE']['BOMB_SIZE']
        self.position = self.generate_position()
        self.is_exploding = False
        self.explosion_frame = 0
        self.animation_frame = 0
        self.glow_size = 0
        self.glow_direction = 1
        self.visible = True  # Biến để kiểm soát hiệu ứng nhấp nháy
        self.blink_timer = 0
        
        # Tải hình ảnh bom
        try:
            bomb_path = os.path.join(PATHS['IMAGES'], 'bomb_5.png')
            self.image = pg.image.load(bomb_path)
            self.image = pg.transform.scale(self.image, 
                (GAME_CONFIG['GRID_SIZE'] * self.size, 
                 GAME_CONFIG['GRID_SIZE'] * self.size))
        except Exception as e:
            print(f"Không thể tải hình ảnh bom: {e}")
            self.image = None

    def generate_position(self):
        """Tạo vị trí ngẫu nhiên cho bom"""
        while True:
            x = random.randrange(
                GAME_CONFIG['BORDER_SIZE'],
                WINDOW_WIDTH - GAME_CONFIG['BORDER_SIZE'] - (GAME_CONFIG['GRID_SIZE'] * self.size),
                GAME_CONFIG['GRID_SIZE']
            )
            y = random.randrange(
                GAME_CONFIG['BORDER_SIZE'],
                WINDOW_HEIGHT - GAME_CONFIG['BORDER_SIZE'] - (GAME_CONFIG['GRID_SIZE'] * self.size),
                GAME_CONFIG['GRID_SIZE']
            )
            
            # Kiểm tra không trùng với vị trí thức ăn
            if hasattr(self.game, 'food') and self.game.food:
                food_rect = pg.Rect(self.game.food.position[0], self.game.food.position[1],
                                  GAME_CONFIG['GRID_SIZE'], GAME_CONFIG['GRID_SIZE'])
                bomb_rect = pg.Rect(x, y, GAME_CONFIG['GRID_SIZE'] * self.size, 
                                  GAME_CONFIG['GRID_SIZE'] * self.size)
                if bomb_rect.colliderect(food_rect):
                    continue
                    
            # Kiểm tra không trùng với vị trí rắn
            if hasattr(self.game, 'snake') and self.game.snake:
                bomb_rect = pg.Rect(x, y, GAME_CONFIG['GRID_SIZE'] * self.size, 
                                  GAME_CONFIG['GRID_SIZE'] * self.size)
                for pos in self.game.snake.positions:
                    snake_rect = pg.Rect(pos[0], pos[1], GAME_CONFIG['GRID_SIZE'], 
                                       GAME_CONFIG['GRID_SIZE'])
                    if bomb_rect.colliderect(snake_rect):
                        continue
                    
            # Kiểm tra không trùng với vị trí bom khác
            if hasattr(self.game, 'bombs') and self.game.bombs:
                bomb_rect = pg.Rect(x, y, GAME_CONFIG['GRID_SIZE'] * self.size, 
                                  GAME_CONFIG['GRID_SIZE'] * self.size)
                for bomb in self.game.bombs:
                    other_bomb_rect = pg.Rect(bomb.position[0], bomb.position[1],
                                            GAME_CONFIG['GRID_SIZE'] * self.size,
                                            GAME_CONFIG['GRID_SIZE'] * self.size)
                    if bomb_rect.colliderect(other_bomb_rect):
                        continue
                    
            return [x, y]

    def draw(self):
        if not self.visible and not self.is_exploding:
            return

        # Tính toán kích thước bom
        bomb_size = GAME_CONFIG['GRID_SIZE'] * self.size

        if self.is_exploding:
            # Vẽ hiệu ứng nổ
            explosion_size = bomb_size * (1 + math.sin(self.explosion_frame))
            explosion_color = (
                int(COLORS['RED'][0] * (1 - self.explosion_frame/(2*math.pi)) + COLORS['YELLOW'][0] * (self.explosion_frame/(2*math.pi))),
                int(COLORS['RED'][1] * (1 - self.explosion_frame/(2*math.pi)) + COLORS['YELLOW'][1] * (self.explosion_frame/(2*math.pi))),
                int(COLORS['RED'][2] * (1 - self.explosion_frame/(2*math.pi)) + COLORS['YELLOW'][2] * (self.explosion_frame/(2*math.pi)))
            )
            
            # Vẽ vòng tròn nổ
            pg.draw.circle(screen, explosion_color,
                         (self.position[0] + bomb_size//2, self.position[1] + bomb_size//2),
                         int(explosion_size//2))
            
            # Vẽ tia sáng
            for i in range(8):
                angle = i * math.pi / 4 + self.explosion_frame
                end_x = self.position[0] + bomb_size//2 + math.cos(angle) * explosion_size
                end_y = self.position[1] + bomb_size//2 + math.sin(angle) * explosion_size
                pg.draw.line(screen, explosion_color,
                           (self.position[0] + bomb_size//2, self.position[1] + bomb_size//2),
                           (end_x, end_y), 3)
        else:
            # Tính toán độ trong suốt dựa trên hiệu ứng nhấp nháy
            alpha = int(GAME_CONFIG['BOMB_MODE']['ANIMATION']['ALPHA_MIN'] + 
                       (GAME_CONFIG['BOMB_MODE']['ANIMATION']['ALPHA_MAX'] - 
                        GAME_CONFIG['BOMB_MODE']['ANIMATION']['ALPHA_MIN']) * 
                       (1 - abs(math.sin(self.blink_timer * math.pi))))
            
            # Tạo surface cho hiệu ứng phát sáng
            glow_surface = pg.Surface((bomb_size + 2 * self.glow_size, 
                                     bomb_size + 2 * self.glow_size), 
                                    pg.SRCALPHA)
            
            # Vẽ hiệu ứng phát sáng với màu đỏ
            glow_color = (255, 0, 0, alpha)  # Màu đỏ với độ trong suốt
            pg.draw.rect(glow_surface, glow_color,
                        [0, 0, bomb_size + 2 * self.glow_size, bomb_size + 2 * self.glow_size],
                        border_radius=5)
            screen.blit(glow_surface, 
                       (self.position[0] - self.glow_size, 
                        self.position[1] - self.glow_size))

            # Tạo surface cho bom
            bomb_surface = pg.Surface((bomb_size, bomb_size), pg.SRCALPHA)
            
            # Vẽ bom với màu đỏ đậm
            bomb_color = (200, 0, 0, alpha)  # Màu đỏ đậm với độ trong suốt
            pg.draw.rect(bomb_surface, bomb_color,
                        [0, 0, bomb_size, bomb_size],
                        border_radius=5)
            
            screen.blit(bomb_surface, self.position)

            # Vẽ ngòi nổ
            fuse_color = (255, 255, 0, alpha)  # Màu vàng với độ trong suốt
            fuse_length = bomb_size * 0.3
            pg.draw.line(screen, fuse_color,
                        (self.position[0] + bomb_size//2, self.position[1]),
                        (self.position[0] + bomb_size//2, self.position[1] - fuse_length), 3)
            
            # Vẽ tia lửa
            spark_angle = math.sin(self.glow_size) * math.pi / 4
            spark_length = fuse_length * 0.5
            spark_x = self.position[0] + bomb_size//2 + math.cos(spark_angle) * spark_length
            spark_y = self.position[1] - fuse_length + math.sin(spark_angle) * spark_length
            spark_color = (255, 165, 0, alpha)  # Màu cam với độ trong suốt
            pg.draw.line(screen, spark_color,
                        (self.position[0] + bomb_size//2, self.position[1] - fuse_length),
                        (spark_x, spark_y), 2)

    def update(self):
        # Cập nhật hiệu ứng nổ
        if self.is_exploding:
            self.explosion_frame += 0.2
            if self.explosion_frame >= 2 * math.pi:
                self.is_exploding = False
                self.explosion_frame = 0
            return

        # Cập nhật hiệu ứng nhấp nháy
        self.blink_timer += GAME_CONFIG['BOMB_MODE']['ANIMATION']['BLINK_SPEED']
        if self.blink_timer >= 2:  # Tăng chu kỳ nhấp nháy
            self.blink_timer = 0

        # Cập nhật hiệu ứng phát sáng
        self.glow_size += GAME_CONFIG['BOMB_MODE']['ANIMATION']['GLOW_SPEED'] * self.glow_direction
        if self.glow_size >= GAME_CONFIG['BOMB_MODE']['ANIMATION']['GLOW_SIZE']:
            self.glow_direction = -1
        elif self.glow_size <= 0:
            self.glow_direction = 1

        # Cập nhật trạng thái bom
        if self.is_exploding:
            self.position = self.generate_position() 