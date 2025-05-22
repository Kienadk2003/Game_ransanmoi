import pygame as pg
import random
import math
from init import *

class Food:
    def __init__(self, game=None):
        self.game = game  # Khởi tạo game reference trước
        self.position = self.generate_position()
        self.animation_frame = 0
        self.animation_speed = 0.1
        self.glow_size = 0
        self.glow_direction = 1

    def generate_position(self):
        """Tạo vị trí ngẫu nhiên cho thức ăn"""
        max_attempts = 100  # Giới hạn số lần thử để tránh vòng lặp vô hạn
        attempts = 0
        
        while attempts < max_attempts:
            attempts += 1
            
            # Tạo vị trí ngẫu nhiên
            x = random.randrange(
                GAME_CONFIG['BORDER_SIZE'],
                WINDOW_WIDTH - GAME_CONFIG['BORDER_SIZE'] - GAME_CONFIG['GRID_SIZE'],
                GAME_CONFIG['GRID_SIZE']
            )
            y = random.randrange(
                GAME_CONFIG['BORDER_SIZE'],
                WINDOW_HEIGHT - GAME_CONFIG['BORDER_SIZE'] - GAME_CONFIG['GRID_SIZE'],
                GAME_CONFIG['GRID_SIZE']
            )
            
            # Tạo Rect cho thức ăn
            food_rect = pg.Rect(x, y, GAME_CONFIG['GRID_SIZE'], GAME_CONFIG['GRID_SIZE'])
            
            # Kiểm tra không trùng với rắn
            if hasattr(self.game, 'snake') and self.game.snake:
                snake_overlap = False
                for pos in self.game.snake.positions:
                    snake_rect = pg.Rect(pos[0], pos[1], GAME_CONFIG['GRID_SIZE'], GAME_CONFIG['GRID_SIZE'])
                    if food_rect.colliderect(snake_rect):
                        snake_overlap = True
                        break
                if snake_overlap:
                    continue
            
            # Kiểm tra không trùng với chướng ngại vật
            if hasattr(self.game, 'obstacles') and self.game.obstacles:
                obstacle_overlap = False
                for obstacle in self.game.obstacles:
                    if food_rect.colliderect(obstacle):
                        obstacle_overlap = True
                        break
                if obstacle_overlap:
                    continue
            
            # Kiểm tra không trùng với bom
            if hasattr(self.game, 'bombs') and self.game.bombs:
                bomb_overlap = False
                for bomb in self.game.bombs:
                    bomb_rect = pg.Rect(bomb.position[0], bomb.position[1],
                                      GAME_CONFIG['GRID_SIZE'] * GAME_CONFIG['BOMB_MODE']['BOMB_SIZE'],
                                      GAME_CONFIG['GRID_SIZE'] * GAME_CONFIG['BOMB_MODE']['BOMB_SIZE'])
                    if food_rect.colliderect(bomb_rect):
                        bomb_overlap = True
                        break
                if bomb_overlap:
                    continue
            
            # Kiểm tra không trùng với vùng điểm số
            if hasattr(self.game, 'score_area') and self.game.score_area:
                if food_rect.colliderect(self.game.score_area):
                    continue
            
            # Nếu không có va chạm nào, trả về vị trí mới
            return [x, y]
        
        # Nếu không tìm được vị trí hợp lệ sau max_attempts lần thử
        # Trả về vị trí mặc định ở giữa màn hình
        return [WINDOW_WIDTH//2, WINDOW_HEIGHT//2]

    def update(self):
        # Cập nhật frame animation
        self.animation_frame += self.animation_speed
        if self.animation_frame >= 2 * math.pi:
            self.animation_frame = 0

        # Cập nhật hiệu ứng glow
        self.glow_size += 0.2 * self.glow_direction
        if self.glow_size >= 5:
            self.glow_direction = -1
        elif self.glow_size <= 0:
            self.glow_direction = 1

    def draw(self):
        # Vẽ hiệu ứng glow
        glow_color = (
            int(COLORS['RED'][0] * (1 - self.glow_size/5) + COLORS['YELLOW'][0] * (self.glow_size/5)),
            int(COLORS['RED'][1] * (1 - self.glow_size/5) + COLORS['YELLOW'][1] * (self.glow_size/5)),
            int(COLORS['RED'][2] * (1 - self.glow_size/5) + COLORS['YELLOW'][2] * (self.glow_size/5))
        )
        
        # Vẽ outer glow
        pg.draw.rect(screen, glow_color,
                    [self.position[0] - self.glow_size, 
                     self.position[1] - self.glow_size,
                     GAME_CONFIG['GRID_SIZE'] + 2 * self.glow_size,
                     GAME_CONFIG['GRID_SIZE'] + 2 * self.glow_size],
                    border_radius=5)

        # Vẽ food với hiệu ứng pulse
        pulse = abs(math.sin(self.animation_frame)) * 2
        food_size = GAME_CONFIG['GRID_SIZE'] - pulse
        
        # Vẽ food với gradient
        for i in range(int(food_size)):
            color = (
                int(COLORS['RED'][0] * (1 - i/food_size) + COLORS['YELLOW'][0] * (i/food_size)),
                int(COLORS['RED'][1] * (1 - i/food_size) + COLORS['YELLOW'][1] * (i/food_size)),
                int(COLORS['RED'][2] * (1 - i/food_size) + COLORS['YELLOW'][2] * (i/food_size))
            )
            pg.draw.rect(screen, color,
                        [self.position[0] + i/2,
                         self.position[1] + i/2,
                         food_size - i,
                         food_size - i],
                        border_radius=5)

        # Vẽ highlight
        highlight_size = food_size * 0.3
        pg.draw.rect(screen, COLORS['WHITE'],
                    [self.position[0] + highlight_size,
                     self.position[1] + highlight_size,
                     highlight_size,
                     highlight_size],
                    border_radius=2)