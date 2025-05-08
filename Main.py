import pygame as pg
import sys
import random
import os
from init import *
from menu import Menu
from snake import Snake
from food import Food

class Game:
    def __init__(self):
        self.clock = pg.time.Clock()
        self.menu = Menu()
        self.snake = None
        self.food = None
        self.game_speed = GAME_CONFIG['SPEEDS']['MEDIUM']
        self.running = True
        self.game_mode = "NORMAL"
        self.obstacles = []  # Danh sách các chướng ngại vật
        
        # Tải hình nền
        try:
            background_path = os.path.join(PATHS['IMAGES'], 'co.jpg')
            self.background = pg.image.load(background_path)
            self.background = pg.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        except Exception as e:
            print(f"Không thể tải hình nền: {e}")
            print("Sử dụng nền mặc định")
            self.background = None

        # Tải hình ảnh tảng đá
        try:
            rock_path = os.path.join(PATHS['IMAGES'], 'da1.jpg')
            self.rock_image = pg.image.load(rock_path)
            self.rock_image = pg.transform.scale(self.rock_image, (60, 60))  # Kích thước cố định cho tảng đá
        except Exception as e:
            print(f"Không thể tải hình ảnh tảng đá: {e}")
            self.rock_image = None

    def initialize_game(self):
        """Khởi tạo game với các thông số từ menu"""
        print(f"Initializing game with mode: {self.game_mode}")
        
        # Reset game state
        self.obstacles = []
        self.snake = None
        self.food = None
        
        # Khởi tạo rắn và thức ăn
        self.snake = Snake()
        self.food = Food()
        self.food.game = self  # Truyền tham chiếu game vào food
        self.running = True
        
        # Tạo chướng ngại vật nếu ở chế độ OBSTACLE
        if self.game_mode == "OBSTACLE":
            print("Creating obstacles...")
            self.create_obstacles()
            # Đảm bảo thức ăn không xuất hiện trên chướng ngại vật
            self.food.position = self.food.generate_position()
            print(f"Number of obstacles created: {len(self.obstacles)}")
            
            # Kiểm tra vị trí ban đầu của rắn
            for pos in self.snake.positions:
                if self.check_obstacle_collision(pos):
                    print("Warning: Snake initial position overlaps with obstacle")
                    # Di chuyển rắn đến vị trí an toàn
                    self.snake.positions = [[GAME_CONFIG['BORDER_SIZE'] + 100, GAME_CONFIG['BORDER_SIZE'] + 100]]
                    break

    def create_obstacles(self):
        """Tạo 5 chướng ngại vật ở vị trí cố định"""
        border_rect = pg.Rect(
            GAME_CONFIG['BORDER_SIZE'],
            GAME_CONFIG['BORDER_SIZE'],
            WINDOW_WIDTH - 2 * GAME_CONFIG['BORDER_SIZE'],
            WINDOW_HEIGHT - 2 * GAME_CONFIG['BORDER_SIZE']
        )
        
        # Kích thước cố định cho chướng ngại vật
        obstacle_size = 60
        
        # Tính toán các vị trí cố định
        center_x = WINDOW_WIDTH // 2
        center_y = WINDOW_HEIGHT // 2
        
        # Tạo 5 chướng ngại vật ở các vị trí cố định
        obstacles = [
            # Chướng ngại vật ở giữa
            pg.Rect(center_x - obstacle_size//2, center_y - obstacle_size//2, 
                   obstacle_size, obstacle_size),
            
            # Chướng ngại vật ở trên
            pg.Rect(center_x - obstacle_size//2, GAME_CONFIG['BORDER_SIZE'] + 50, 
                   obstacle_size, obstacle_size),
            
            # Chướng ngại vật ở dưới
            pg.Rect(center_x - obstacle_size//2, WINDOW_HEIGHT - GAME_CONFIG['BORDER_SIZE'] - obstacle_size - 50, 
                   obstacle_size, obstacle_size),
            
            # Chướng ngại vật ở trái
            pg.Rect(GAME_CONFIG['BORDER_SIZE'] + 50, center_y - obstacle_size//2, 
                   obstacle_size, obstacle_size),
            
            # Chướng ngại vật ở phải
            pg.Rect(WINDOW_WIDTH - GAME_CONFIG['BORDER_SIZE'] - obstacle_size - 50, center_y - obstacle_size//2, 
                   obstacle_size, obstacle_size)
        ]
        
        self.obstacles = obstacles

    def draw_background(self):
        # Vẽ hình nền
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            # Vẽ nền với gradient động nếu không có hình nền
            for y in range(WINDOW_HEIGHT):
                color = (
                    int(COLORS['LIGHT_BLUE'][0] * (1 - y/WINDOW_HEIGHT) + COLORS['BLUE'][0] * (y/WINDOW_HEIGHT)),
                    int(COLORS['LIGHT_BLUE'][1] * (1 - y/WINDOW_HEIGHT) + COLORS['BLUE'][1] * (y/WINDOW_HEIGHT)),
                    int(COLORS['LIGHT_BLUE'][2] * (1 - y/WINDOW_HEIGHT) + COLORS['BLUE'][2] * (y/WINDOW_HEIGHT))
                )
                pg.draw.line(screen, color, (0, y), (WINDOW_WIDTH, y))

        # Vẽ viền đỏ sát với mép ngoài của phân cách
        border_rect = pg.Rect(
            GAME_CONFIG['BORDER_SIZE'] - 2,
            GAME_CONFIG['BORDER_SIZE'] - 2,
            WINDOW_WIDTH - 2 * (GAME_CONFIG['BORDER_SIZE'] - 2),
            WINDOW_HEIGHT - 2 * (GAME_CONFIG['BORDER_SIZE'] - 2)
        )
        pg.draw.rect(screen, COLORS['RED'], border_rect, 5)
        
        # Vẽ nền trong với độ trong suốt
        inner_rect = pg.Rect(
            GAME_CONFIG['BORDER_SIZE'],
            GAME_CONFIG['BORDER_SIZE'],
            WINDOW_WIDTH - 2 * GAME_CONFIG['BORDER_SIZE'],
            WINDOW_HEIGHT - 2 * GAME_CONFIG['BORDER_SIZE']
        )
        s = pg.Surface((inner_rect.width, inner_rect.height), pg.SRCALPHA)
        pg.draw.rect(s, (*COLORS['LIGHT_BLUE'], 32), s.get_rect(), border_radius=6)
        screen.blit(s, inner_rect)
        
        # Vẽ chướng ngại vật nếu ở chế độ OBSTACLE
        if self.game_mode == "OBSTACLE" and self.obstacles:
            for obstacle in self.obstacles:
                if self.rock_image:
                    # Vẽ hình ảnh tảng đá
                    screen.blit(self.rock_image, obstacle)
                else:
                    # Fallback: vẽ hình chữ nhật nếu không tải được hình ảnh
                    s = pg.Surface((obstacle.width + 2, obstacle.height + 2), pg.SRCALPHA)
                    pg.draw.rect(s, (*COLORS['BROWN'], 192), s.get_rect(), border_radius=5)
                    screen.blit(s, (obstacle.x - 1, obstacle.y - 1))
                    
                    s = pg.Surface((obstacle.width, obstacle.height), pg.SRCALPHA)
                    pg.draw.rect(s, (*COLORS['ORANGE'], 192), s.get_rect(), border_radius=5)
                    screen.blit(s, obstacle)

    def draw_score(self):
        # Vẽ điểm số với hiệu ứng đẹp
        score_text = f"Score: {self.snake.score} - Difficulty: {self.menu.difficulty}"
        text_surface = FONTS['MEDIUM'].render(score_text, True, COLORS['BROWN'])
        text_rect = text_surface.get_rect(topleft=(10, GAME_CONFIG['BORDER_SIZE'] // 2))
        
        # Vẽ nền cho text
        pg.draw.rect(screen, COLORS['ORANGE'], text_rect.inflate(20, 10), border_radius=10)
        # Vẽ viền
        pg.draw.rect(screen, COLORS['BROWN'], text_rect.inflate(20, 10), 2, border_radius=10)
        # Vẽ text với shadow
        shadow = FONTS['MEDIUM'].render(score_text, True, COLORS['BLACK'])
        screen.blit(shadow, (text_rect.x + 2, text_rect.y + 2))
        screen.blit(text_surface, text_rect)

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit_game()
                return False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit_game()
                    return False
                elif event.key == pg.K_LEFT:
                    self.snake.change_direction([-GAME_CONFIG['GRID_SIZE'], 0])
                elif event.key == pg.K_RIGHT:
                    self.snake.change_direction([GAME_CONFIG['GRID_SIZE'], 0])
                elif event.key == pg.K_UP:
                    self.snake.change_direction([0, -GAME_CONFIG['GRID_SIZE']])
                elif event.key == pg.K_DOWN:
                    self.snake.change_direction([0, GAME_CONFIG['GRID_SIZE']])
        return True

    def check_obstacle_collision(self, pos):
        """Kiểm tra va chạm với chướng ngại vật"""
        if self.game_mode != "OBSTACLE" or not self.obstacles:
            return False
            
        # Tạo Rect cho vị trí cần kiểm tra
        pos_rect = pg.Rect(pos[0], pos[1], GAME_CONFIG['GRID_SIZE'], GAME_CONFIG['GRID_SIZE'])
        
        # Kiểm tra va chạm với tất cả các chướng ngại vật
        for obstacle in self.obstacles:
            if pos_rect.colliderect(obstacle):
                return True
        return False

    def quit_game(self):
        """Clean up resources and exit the game"""
        self.running = False
        # Stop all sounds
        for sound in SOUNDS.values():
            if sound:
                sound.stop()
        # Quit pygame
        pg.quit()
        # Exit the program
        sys.exit()

    def run_game(self):
        """Vòng lặp chính của game"""
        while self.running:
            # Xử lý sự kiện
            if not self.handle_events():
                return False

            # Cập nhật game
            self.snake.update()
            self.food.update()

            # Kiểm tra va chạm
            if (self.snake.check_collision() or 
                self.check_obstacle_collision(self.snake.positions[0])):
                if 'GAME_OVER' in SOUNDS:
                    SOUNDS['GAME_OVER'].play()
                return True

            # Kiểm tra ăn mồi
            head_pos = self.snake.positions[0]
            food_pos = self.food.position
            
            # Tạo Rect cho đầu rắn và thức ăn để kiểm tra va chạm
            head_rect = pg.Rect(head_pos[0], head_pos[1], GAME_CONFIG['GRID_SIZE'], GAME_CONFIG['GRID_SIZE'])
            food_rect = pg.Rect(food_pos[0], food_pos[1], GAME_CONFIG['GRID_SIZE'], GAME_CONFIG['GRID_SIZE'])
            
            if head_rect.colliderect(food_rect):
                if 'EAT' in SOUNDS:
                    SOUNDS['EAT'].play()
                self.snake.length += 1
                self.snake.score += 1
                # Tạo thức ăn mới
                self.food = Food()
                self.food.game = self  # Truyền tham chiếu game vào food mới
                # Đảm bảo thức ăn mới không xuất hiện trên chướng ngại vật
                if self.game_mode == "OBSTACLE":
                    self.food.position = self.food.generate_position()

            # Vẽ game
            self.draw_background()
            self.food.draw()
            self.snake.draw()
            self.draw_score()
            
            pg.display.flip()
            self.clock.tick(self.game_speed)

        return False

    def run(self):
        while self.running:
            # Chạy menu
            result = self.menu.run()
            
            # Xử lý kết quả từ menu
            if result is False:  # Quit game
                self.quit_game()
                break
            elif isinstance(result, tuple) and result[0] == "START":
                # Cập nhật tốc độ game và chế độ chơi
                self.game_speed = GAME_CONFIG['SPEEDS'][result[1]]
                self.game_mode = result[2]
                print(f"Starting game with mode: {self.game_mode}")
                
                # Khởi tạo game mới
                self.initialize_game()
                
                # Chạy game
                game_result = self.run_game()
                if game_result is False:  # Game was quit
                    self.quit_game()
                    break
                elif game_result is True:  # Game over
                    continue  # Return to menu

if __name__ == "__main__":
    game = Game()
    game.run()