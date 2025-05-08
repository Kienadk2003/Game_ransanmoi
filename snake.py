import pygame as pg
import math
from init import *

class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.positions = []
        self.length = GAME_CONFIG['INITIAL_SNAKE_LENGTH']
        self.direction = [GAME_CONFIG['GRID_SIZE'], 0]
        self.next_direction = [GAME_CONFIG['GRID_SIZE'], 0]
        self.score = 0
        
        # Vị trí ban đầu ở góc trên trái
        start_x = GAME_CONFIG['BORDER_SIZE'] + GAME_CONFIG['GRID_SIZE'] * 3
        start_y = GAME_CONFIG['BORDER_SIZE'] + GAME_CONFIG['GRID_SIZE'] * 3
        
        # Tạo thân rắn ban đầu
        for i in range(self.length):
            self.positions.append([start_x - i * GAME_CONFIG['GRID_SIZE'], start_y])

        # Hiệu ứng
        self.animation_frame = 0
        self.animation_speed = 0.1
        self.glow_size = 0
        self.glow_direction = 1

    def update(self):
        # Cập nhật hướng di chuyển
        self.direction = self.next_direction

        # Di chuyển đầu rắn
        new_head = [
            self.positions[0][0] + self.direction[0],
            self.positions[0][1] + self.direction[1]
        ]
        self.positions.insert(0, new_head)

        # Xóa đuôi nếu rắn không ăn
        while len(self.positions) > self.length:
            self.positions.pop()

        # Cập nhật animation
        self.animation_frame += self.animation_speed
        if self.animation_frame >= 2 * math.pi:
            self.animation_frame = 0

        # Cập nhật hiệu ứng glow
        self.glow_size += 0.2 * self.glow_direction
        if self.glow_size >= 3:
            self.glow_direction = -1
        elif self.glow_size <= 0:
            self.glow_direction = 1

    def draw(self):
        # Vẽ thân rắn với hiệu ứng gradient và glow
        for i, pos in enumerate(self.positions):
            # Tính toán màu gradient dựa trên vị trí trong thân rắn
            gradient_progress = i / len(self.positions)
            body_color = (
                int(COLORS['GREEN'][0] * (1 - gradient_progress) + COLORS['BLUE'][0] * gradient_progress),
                int(COLORS['GREEN'][1] * (1 - gradient_progress) + COLORS['BLUE'][1] * gradient_progress),
                int(COLORS['GREEN'][2] * (1 - gradient_progress) + COLORS['BLUE'][2] * gradient_progress)
            )

            # Vẽ glow effect
            if i == 0:  # Chỉ vẽ glow cho đầu rắn
                glow_color = (
                    int(body_color[0] * (1 - self.glow_size/3) + COLORS['WHITE'][0] * (self.glow_size/3)),
                    int(body_color[1] * (1 - self.glow_size/3) + COLORS['WHITE'][1] * (self.glow_size/3)),
                    int(body_color[2] * (1 - self.glow_size/3) + COLORS['WHITE'][2] * (self.glow_size/3))
                )
                pg.draw.rect(screen, glow_color,
                           [pos[0] - self.glow_size,
                            pos[1] - self.glow_size,
                            GAME_CONFIG['GRID_SIZE'] + 2 * self.glow_size,
                            GAME_CONFIG['GRID_SIZE'] + 2 * self.glow_size],
                           border_radius=5)

            # Vẽ thân rắn với hiệu ứng pulse
            pulse = abs(math.sin(self.animation_frame + i * 0.5)) * 2
            segment_size = GAME_CONFIG['GRID_SIZE'] - pulse

            # Vẽ segment với gradient
            for j in range(int(segment_size)):
                color = (
                    int(body_color[0] * (1 - j/segment_size) + COLORS['WHITE'][0] * (j/segment_size)),
                    int(body_color[1] * (1 - j/segment_size) + COLORS['WHITE'][1] * (j/segment_size)),
                    int(body_color[2] * (1 - j/segment_size) + COLORS['WHITE'][2] * (j/segment_size))
                )
                pg.draw.rect(screen, color,
                           [pos[0] + j/2,
                            pos[1] + j/2,
                            segment_size - j,
                            segment_size - j],
                           border_radius=5)

            # Vẽ mắt cho đầu rắn
            if i == 0:
                eye_size = GAME_CONFIG['GRID_SIZE'] // 4
                # Tính toán vị trí mắt dựa trên hướng di chuyển
                if self.direction[0] > 0:  # Di chuyển sang phải
                    eye_pos1 = (pos[0] + GAME_CONFIG['GRID_SIZE'] - eye_size, pos[1] + eye_size)
                    eye_pos2 = (pos[0] + GAME_CONFIG['GRID_SIZE'] - eye_size, pos[1] + GAME_CONFIG['GRID_SIZE'] - eye_size)
                elif self.direction[0] < 0:  # Di chuyển sang trái
                    eye_pos1 = (pos[0] + eye_size, pos[1] + eye_size)
                    eye_pos2 = (pos[0] + eye_size, pos[1] + GAME_CONFIG['GRID_SIZE'] - eye_size)
                elif self.direction[1] > 0:  # Di chuyển xuống
                    eye_pos1 = (pos[0] + eye_size, pos[1] + GAME_CONFIG['GRID_SIZE'] - eye_size)
                    eye_pos2 = (pos[0] + GAME_CONFIG['GRID_SIZE'] - eye_size, pos[1] + GAME_CONFIG['GRID_SIZE'] - eye_size)
                else:  # Di chuyển lên
                    eye_pos1 = (pos[0] + eye_size, pos[1] + eye_size)
                    eye_pos2 = (pos[0] + GAME_CONFIG['GRID_SIZE'] - eye_size, pos[1] + eye_size)

                # Vẽ mắt với hiệu ứng glow
                pg.draw.circle(screen, COLORS['WHITE'], eye_pos1, eye_size)
                pg.draw.circle(screen, COLORS['WHITE'], eye_pos2, eye_size)
                pg.draw.circle(screen, COLORS['BLACK'], eye_pos1, eye_size // 2)
                pg.draw.circle(screen, COLORS['BLACK'], eye_pos2, eye_size // 2)

    def change_direction(self, new_direction):
        # Ngăn rắn quay 180 độ
        if (new_direction[0] * -1, new_direction[1] * -1) != (self.direction[0], self.direction[1]):
            self.next_direction = new_direction

    def check_collision(self):
        head = self.positions[0]
        
        # Kiểm tra va chạm với tường (viền đỏ)
        if (head[0] < GAME_CONFIG['BORDER_SIZE'] or
            head[0] >= WINDOW_WIDTH - GAME_CONFIG['BORDER_SIZE'] - GAME_CONFIG['GRID_SIZE'] or
            head[1] < GAME_CONFIG['BORDER_SIZE'] or
            head[1] >= WINDOW_HEIGHT - GAME_CONFIG['BORDER_SIZE'] - GAME_CONFIG['GRID_SIZE']):
            return True

        # Kiểm tra va chạm với thân
        if head in self.positions[1:]:
            return True

        return False

    def check_food_collision(self, food_position):
        if self.positions[0] == food_position:
            self.length += 1
            self.score += 1
            if 'EAT' in SOUNDS:
                SOUNDS['EAT'].play()
            return True
        return False 