import pygame as pg
import sys
import random
import os
from init import *
from menu import Menu
from snake import Snake
from food import Food
from bomb import Bomb

class Game:
    def __init__(self):
        self.clock = pg.time.Clock()
        self.menu = Menu()
        self.snake = None
        self.food = None
        self.bombs = []  # Danh sách các bom
        self.game_speed = GAME_CONFIG['SPEEDS']['MEDIUM']
        self.base_speed = GAME_CONFIG['SPEEDS']['MEDIUM']  # Tốc độ cơ bản
        self.running = True
        self.game_mode = "NORMAL"
        self.obstacles = []  # Danh sách các chướng ngại vật
        self.speed_boost_message = None  # Thông báo tăng tốc
        self.speed_boost_timer = 0  # Thời gian hiển thị thông báo
        self.speed_boost_duration = 0  # Thời gian còn lại của speed boost
        self.speed_boost_count = 0  # Đếm số mồi tăng tốc còn lại trong NO_WALL mode
        self.speed_boost_target = 0  # Số điểm cần đạt để tăng tốc trong SPEED_BOOST mode
        
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
        self.bombs = []
        self.snake = None
        self.food = None
        
        # Khởi tạo rắn và thức ăn
        self.snake = Snake()
        self.snake.game = self  # Truyền tham chiếu game vào snake
        self.food = Food(self)  # Truyền tham chiếu game vào food
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
        
        # Tạo bom nếu ở chế độ BOMB
        if self.game_mode == "BOMB":
            print("Creating initial bombs...")
            self.create_bombs('INITIAL')
            print(f"Number of bombs created: {len(self.bombs)}")

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

    def create_bombs(self, stage):
        """Tạo bom ở các vị trí cố định dựa trên giai đoạn"""
        if stage == 'INITIAL':
            # Tạo 5 bom ở vị trí cố định ban đầu
            self.bombs = []
            positions = [
                (WINDOW_WIDTH//4, WINDOW_HEIGHT//4),
                (WINDOW_WIDTH//4, 3*WINDOW_HEIGHT//4),
                (3*WINDOW_WIDTH//4, WINDOW_HEIGHT//4),
                (3*WINDOW_WIDTH//4, 3*WINDOW_HEIGHT//4),
                (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
            ]
            for pos in positions:
                bomb = Bomb(self)
                bomb.position = list(pos)
                self.bombs.append(bomb)
        elif stage == '15_POINTS':
            # Tạo 7 bom ở vị trí cố định
            self.bombs = []
            positions = [
                (WINDOW_WIDTH//4, WINDOW_HEIGHT//4),
                (WINDOW_WIDTH//4, 3*WINDOW_HEIGHT//4),
                (3*WINDOW_WIDTH//4, WINDOW_HEIGHT//4),
                (3*WINDOW_WIDTH//4, 3*WINDOW_HEIGHT//4),
                (WINDOW_WIDTH//2, WINDOW_HEIGHT//4),
                (WINDOW_WIDTH//2, 3*WINDOW_HEIGHT//4),
                (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
            ]
            for pos in positions:
                bomb = Bomb(self)
                bomb.position = list(pos)
                self.bombs.append(bomb)
        elif stage == '30_POINTS':
            # Tạo 10 bom ở vị trí cố định
            self.bombs = []
            positions = [
                (WINDOW_WIDTH//4, WINDOW_HEIGHT//4),
                (WINDOW_WIDTH//4, 3*WINDOW_HEIGHT//4),
                (3*WINDOW_WIDTH//4, WINDOW_HEIGHT//4),
                (3*WINDOW_WIDTH//4, 3*WINDOW_HEIGHT//4),
                (WINDOW_WIDTH//2, WINDOW_HEIGHT//4),
                (WINDOW_WIDTH//2, 3*WINDOW_HEIGHT//4),
                (WINDOW_WIDTH//2, WINDOW_HEIGHT//2),
                (WINDOW_WIDTH//4, WINDOW_HEIGHT//2),
                (3*WINDOW_WIDTH//4, WINDOW_HEIGHT//2),
                (WINDOW_WIDTH//2, WINDOW_HEIGHT//3)
            ]
            for pos in positions:
                bomb = Bomb(self)
                bomb.position = list(pos)
                self.bombs.append(bomb)

    def move_bomb(self, bomb):
        """Di chuyển bom đến vị trí mới cách vị trí cũ 5 ô"""
        old_x, old_y = bomb.position
        grid_size = GAME_CONFIG['GRID_SIZE']
        move_distance = 5 * grid_size  # Di chuyển 5 ô
        
        # Tạo danh sách các hướng có thể di chuyển
        possible_moves = [
            (old_x + move_distance, old_y),  # Phải
            (old_x - move_distance, old_y),  # Trái
            (old_x, old_y + move_distance),  # Xuống
            (old_x, old_y - move_distance)   # Lên
        ]
        
        # Lọc các vị trí hợp lệ (trong phạm vi màn hình và không chồng lên bom khác)
        valid_moves = []
        for new_x, new_y in possible_moves:
            if (GAME_CONFIG['BORDER_SIZE'] <= new_x <= WINDOW_WIDTH - GAME_CONFIG['BORDER_SIZE'] - grid_size and
                GAME_CONFIG['BORDER_SIZE'] <= new_y <= WINDOW_HEIGHT - GAME_CONFIG['BORDER_SIZE'] - grid_size):
                
                # Kiểm tra không chồng lên bom khác
                new_rect = pg.Rect(new_x, new_y, 
                                 grid_size * GAME_CONFIG['BOMB_MODE']['BOMB_SIZE'],
                                 grid_size * GAME_CONFIG['BOMB_MODE']['BOMB_SIZE'])
                
                overlap = False
                for other_bomb in self.bombs:
                    if other_bomb != bomb:
                        other_rect = pg.Rect(other_bomb.position[0], other_bomb.position[1],
                                           grid_size * GAME_CONFIG['BOMB_MODE']['BOMB_SIZE'],
                                           grid_size * GAME_CONFIG['BOMB_MODE']['BOMB_SIZE'])
                        if new_rect.colliderect(other_rect):
                            overlap = True
                            break
                
                if not overlap:
                    valid_moves.append((new_x, new_y))
        
        # Nếu có vị trí hợp lệ, chọn ngẫu nhiên một vị trí
        if valid_moves:
            new_x, new_y = random.choice(valid_moves)
            bomb.position = [new_x, new_y]
        else:
            # Nếu không có vị trí hợp lệ, giữ nguyên vị trí cũ
            pass

    def check_bomb_collision(self, pos):
        """Kiểm tra va chạm với bom"""
        if self.game_mode != "BOMB" or not self.bombs:
            return False
            
        # Tạo Rect cho vị trí cần kiểm tra
        pos_rect = pg.Rect(pos[0], pos[1], GAME_CONFIG['GRID_SIZE'], GAME_CONFIG['GRID_SIZE'])
        
        # Kiểm tra va chạm với tất cả các bom
        for bomb in self.bombs:
            bomb_rect = pg.Rect(bomb.position[0], bomb.position[1], 
                              GAME_CONFIG['GRID_SIZE'] * GAME_CONFIG['BOMB_MODE']['BOMB_SIZE'],
                              GAME_CONFIG['GRID_SIZE'] * GAME_CONFIG['BOMB_MODE']['BOMB_SIZE'])
            if pos_rect.colliderect(bomb_rect):
                # Kích hoạt hiệu ứng nổ
                bomb.is_exploding = True
                
                # Trừ điểm (chỉ trừ 5 điểm)
                self.snake.score = max(0, self.snake.score - GAME_CONFIG['BOMB_MODE']['SCORE_PENALTY'])
                
                # Di chuyển bom đến vị trí mới cách 5 ô
                self.move_bomb(bomb)
                
                # Kiểm tra và tăng số lượng bom dựa trên điểm số
                current_score = self.snake.score
                if current_score >= 30 and len(self.bombs) < 10:
                    self.create_bombs('30_POINTS')
                elif current_score >= 15 and len(self.bombs) < 7:
                    self.create_bombs('15_POINTS')
                
                # Nếu điểm về 0, game over
                if self.snake.score == 0:
                    return True
                    
                return False
        return False

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

        # Vẽ nền trong với độ trong suốt
        inner_rect = pg.Rect(
            0,
            0,
            WINDOW_WIDTH,
            WINDOW_HEIGHT
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
        
        # Vẽ bom nếu ở chế độ BOMB
        if self.game_mode == "BOMB" and self.bombs:
            for bomb in self.bombs:
                bomb.draw()

    def draw_score(self):
        # Vẽ điểm số với hiệu ứng đẹp
        score_text = f"Score: {self.snake.score} - Difficulty: {self.menu.difficulty} - Mode: {self.game_mode}"
        if self.game_mode == "SPEED_BOOST":
            score_text += f" - Speed: {self.game_speed}"
        text_surface = FONTS['MEDIUM'].render(score_text, True, COLORS['BROWN'])
        text_rect = text_surface.get_rect(topleft=(10, 10))
        
        # Vẽ nền cho text với kích thước lớn hơn
        score_area = text_rect.inflate(40, 20)
        pg.draw.rect(screen, COLORS['ORANGE'], score_area, border_radius=10)
        # Vẽ viền
        pg.draw.rect(screen, COLORS['BROWN'], score_area, 2, border_radius=10)
        # Vẽ text với shadow
        shadow = FONTS['MEDIUM'].render(score_text, True, COLORS['BLACK'])
        screen.blit(shadow, (text_rect.x + 2, text_rect.y + 2))
        screen.blit(text_surface, text_rect)
        
        # Vẽ thông báo tăng tốc nếu có
        if self.speed_boost_message and self.speed_boost_timer > 0:
            boost_text = f"Speed Boost! New Speed: {self.game_speed}"
            boost_surface = FONTS['MEDIUM'].render(boost_text, True, COLORS['YELLOW'])
            boost_rect = boost_surface.get_rect(center=(WINDOW_WIDTH // 2, 50))
            
            # Vẽ nền cho thông báo
            pg.draw.rect(screen, COLORS['RED'], boost_rect.inflate(40, 20), border_radius=10)
            # Vẽ viền
            pg.draw.rect(screen, COLORS['BROWN'], boost_rect.inflate(40, 20), 2, border_radius=10)
            # Vẽ text
            screen.blit(boost_surface, boost_rect)
            
            # Giảm thời gian hiển thị
            self.speed_boost_timer -= 1
        
        # Lưu vùng điểm số để tránh sinh mồi (mở rộng thêm)
        self.score_area = score_area.inflate(20, 20)

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

    def reposition_bombs(self):
        """Di chuyển tất cả bom đến vị trí mới, đảm bảo không chồng lên nhau"""
        # Lưu lại các vị trí cũ
        old_positions = [bomb.position for bomb in self.bombs]
        
        # Tạo vị trí mới cho từng bom
        for bomb in self.bombs:
            while True:
                new_pos = bomb.generate_position()
                # Kiểm tra không trùng với vị trí cũ của các bom khác
                if not any(self.check_bomb_overlap(new_pos, old_pos) for old_pos in old_positions):
                    bomb.position = new_pos
                    break

    def check_bomb_overlap(self, pos1, pos2):
        """Kiểm tra xem hai bom có chồng lên nhau không"""
        bomb_size = GAME_CONFIG['GRID_SIZE'] * GAME_CONFIG['BOMB_MODE']['BOMB_SIZE']
        rect1 = pg.Rect(pos1[0], pos1[1], bomb_size, bomb_size)
        rect2 = pg.Rect(pos2[0], pos2[1], bomb_size, bomb_size)
        return rect1.colliderect(rect2)

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
            
            # Cập nhật bom nếu ở chế độ BOMB
            if self.game_mode == "BOMB":
                for bomb in self.bombs:
                    bomb.update()

            # Cập nhật speed boost
            if self.speed_boost_duration > 0:
                self.speed_boost_duration -= 1
                if self.speed_boost_duration == 0:
                    self.game_speed = self.base_speed
                    self.speed_boost_message = None

            # Kiểm tra và kích hoạt speed boost cho chế độ SPEED_BOOST
            if self.game_mode == "SPEED_BOOST":
                if self.snake.score >= 15 and self.speed_boost_target < 15:
                    self.game_speed = self.base_speed + 5
                    self.speed_boost_target = 15
                    self.speed_boost_message = "Speed Boost! +5"
                    self.speed_boost_timer = 60
                elif self.snake.score >= 30 and self.speed_boost_target < 30:
                    self.game_speed = self.base_speed + 10
                    self.speed_boost_target = 30
                    self.speed_boost_message = "Speed Boost! +10"
                    self.speed_boost_timer = 60

            # Xử lý xuyên tường cho chế độ NO_WALL
            if self.game_mode == "NO_WALL":
                head = self.snake.positions[0]
                # Nếu rắn đi ra khỏi màn hình, đưa nó vào từ phía đối diện
                if head[0] <= 0:
                    self.snake.positions[0][0] = WINDOW_WIDTH - GAME_CONFIG['GRID_SIZE']
                elif head[0] >= WINDOW_WIDTH - GAME_CONFIG['GRID_SIZE']:
                    self.snake.positions[0][0] = 0
                if head[1] <= 0:
                    self.snake.positions[0][1] = WINDOW_HEIGHT - GAME_CONFIG['GRID_SIZE']
                elif head[1] >= WINDOW_HEIGHT - GAME_CONFIG['GRID_SIZE']:
                    self.snake.positions[0][1] = 0

            # Kiểm tra va chạm
            if (self.snake.check_collision() or 
                self.check_obstacle_collision(self.snake.positions[0]) or
                self.check_bomb_collision(self.snake.positions[0])):
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
                
                # Xử lý tăng tốc cho chế độ NO_WALL
                if self.game_mode == "NO_WALL":
                    if self.speed_boost_count > 0:
                        self.speed_boost_count -= 1
                        if self.speed_boost_count == 0:
                            self.game_speed = self.base_speed
                            self.speed_boost_message = None
                    else:
                        # Random tăng tốc cho 3 mồi tiếp theo
                        if random.random() < 0.3:  # 30% cơ hội tăng tốc
                            self.speed_boost_count = 3
                            self.game_speed = self.base_speed + 5
                            self.speed_boost_message = "Speed Boost! Next 3 foods"
                            self.speed_boost_timer = 60
                
                # Tạo thức ăn mới
                self.food = Food(self)
                # Đảm bảo thức ăn mới không xuất hiện trên chướng ngại vật hoặc bom
                if self.game_mode == "OBSTACLE" or self.game_mode == "BOMB":
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