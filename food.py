import pygame as pg
import random
import math
from init import *

class Food:
    def __init__(self):
        self.position = self.generate_position()
        self.animation_frame = 0
        self.animation_speed = 0.1
        self.glow_size = 0
        self.glow_direction = 1

    def generate_position(self):
        """Tạo vị trí ngẫu nhiên cho thức ăn, đảm bảo không chồng lấn với chướng ngại vật"""
        max_attempts = 100
        attempts = 0
        
        while attempts < max_attempts:
            # Tạo vị trí ngẫu nhiên trên lưới
            x = GAME_CONFIG['BORDER_SIZE'] + random.randrange(
                0, (WINDOW_WIDTH - 2 * GAME_CONFIG['BORDER_SIZE']) // GAME_CONFIG['GRID_SIZE']
            ) * GAME_CONFIG['GRID_SIZE']
            
            y = GAME_CONFIG['BORDER_SIZE'] + random.randrange(
                0, (WINDOW_HEIGHT - 2 * GAME_CONFIG['BORDER_SIZE']) // GAME_CONFIG['GRID_SIZE']
            ) * GAME_CONFIG['GRID_SIZE']
            
            # Tạo Rect cho thức ăn
            food_rect = pg.Rect(x, y, GAME_CONFIG['GRID_SIZE'], GAME_CONFIG['GRID_SIZE'])
            
            # Kiểm tra va chạm với chướng ngại vật
            if hasattr(self, 'game') and self.game.game_mode == "OBSTACLE":
                # Kiểm tra va chạm với tất cả các chướng ngại vật
                collision = False
                for obstacle in self.game.obstacles:
                    # Tạo một Rect lớn hơn một chút để đảm bảo không chạm vào cạnh
                    expanded_obstacle = obstacle.inflate(10, 10)
                    if food_rect.colliderect(expanded_obstacle):
                        collision = True
                        break
                
                if not collision:
                    return [x, y]
            else:
                return [x, y]
                
            attempts += 1
        
        # Nếu không tìm được vị trí phù hợp, tìm vị trí trống gần nhất
        if hasattr(self, 'game') and self.game.game_mode == "OBSTACLE":
            # Tìm vị trí trống gần nhất từ góc trên trái
            min_distance = float('inf')
            best_position = None
            
            # Tìm vị trí trống trong các góc
            corners = [
                (GAME_CONFIG['BORDER_SIZE'] + GAME_CONFIG['GRID_SIZE'], 
                 GAME_CONFIG['BORDER_SIZE'] + GAME_CONFIG['GRID_SIZE']),  # Góc trên trái
                (WINDOW_WIDTH - GAME_CONFIG['BORDER_SIZE'] - GAME_CONFIG['GRID_SIZE'], 
                 GAME_CONFIG['BORDER_SIZE'] + GAME_CONFIG['GRID_SIZE']),  # Góc trên phải
                (GAME_CONFIG['BORDER_SIZE'] + GAME_CONFIG['GRID_SIZE'], 
                 WINDOW_HEIGHT - GAME_CONFIG['BORDER_SIZE'] - GAME_CONFIG['GRID_SIZE']),  # Góc dưới trái
                (WINDOW_WIDTH - GAME_CONFIG['BORDER_SIZE'] - GAME_CONFIG['GRID_SIZE'], 
                 WINDOW_HEIGHT - GAME_CONFIG['BORDER_SIZE'] - GAME_CONFIG['GRID_SIZE'])  # Góc dưới phải
            ]
            
            for corner_x, corner_y in corners:
                food_rect = pg.Rect(corner_x, corner_y, GAME_CONFIG['GRID_SIZE'], GAME_CONFIG['GRID_SIZE'])
                
                # Kiểm tra va chạm
                collision = False
                for obstacle in self.game.obstacles:
                    if food_rect.colliderect(obstacle):
                        collision = True
                        break
                
                if not collision:
                    distance = ((corner_x - GAME_CONFIG['BORDER_SIZE']) ** 2 + 
                              (corner_y - GAME_CONFIG['BORDER_SIZE']) ** 2) ** 0.5
                    if distance < min_distance:
                        min_distance = distance
                        best_position = [corner_x, corner_y]
            
            if best_position:
                return best_position
        
        # Nếu vẫn không tìm được vị trí phù hợp, trả về vị trí mặc định ở góc trên trái
        return [GAME_CONFIG['BORDER_SIZE'] + GAME_CONFIG['GRID_SIZE'], 
                GAME_CONFIG['BORDER_SIZE'] + GAME_CONFIG['GRID_SIZE']]

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