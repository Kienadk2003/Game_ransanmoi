import pygame as pg
from init import *

class Button:
    def __init__(self, pos, text, size='LARGE'):
        self.pos = pos
        self.text = text
        self.font = FONTS[size]
        self.rect = None
        self.is_hovered = False
        self.animation_offset = 0
        self.update()

    def update(self):
        text_surface = self.font.render(self.text, True, COLORS['WHITE'] if not self.is_hovered else COLORS['YELLOW'])
        self.rect = text_surface.get_rect(center=self.pos)
        
        # Hiệu ứng hover
        if self.is_hovered:
            self.animation_offset = min(self.animation_offset + 0.2, 1)
        else:
            self.animation_offset = max(self.animation_offset - 0.2, 0)
        
        # Vẽ nút với hiệu ứng gradient và glow
        glow_size = int(10 * self.animation_offset)
        pg.draw.rect(screen, COLORS['YELLOW'], 
                    self.rect.inflate(24 + glow_size, 14 + glow_size), 
                    border_radius=12)
        pg.draw.rect(screen, COLORS['ORANGE'], 
                    self.rect.inflate(20 + glow_size, 10 + glow_size), 
                    border_radius=10)
        
        # Vẽ text với hiệu ứng shadow
        shadow_offset = 2
        shadow = self.font.render(self.text, True, COLORS['BLACK'])
        screen.blit(shadow, (self.rect.x + shadow_offset, self.rect.y + shadow_offset))
        screen.blit(text_surface, self.rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def check_hover(self, pos):
        was_hovered = self.is_hovered
        self.is_hovered = self.rect.collidepoint(pos)
        if not was_hovered and self.is_hovered and 'MENU' in SOUNDS:
            SOUNDS['MENU'].play()

class Menu:
    def __init__(self):
        self.current_state = "MAIN"
        self.difficulty = "MEDIUM"
        self.game_mode = "NORMAL"  # NORMAL hoặc OBSTACLE
        self.running = True
        
        # Load ảnh nền
        self.background = pg.image.load("assets/images/anhNen.png")
        self.background = pg.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        
        # Menu chính
        self.main_buttons = [
            Button((WINDOW_WIDTH // 2, 200), "START"),
            Button((WINDOW_WIDTH // 2, 300), "SPEED"),
            Button((WINDOW_WIDTH // 2, 400), "MODE"),
            Button((WINDOW_WIDTH // 2, 500), "QUIT")
        ]
        
        # Menu Speed
        self.speed_buttons = [
            Button((WINDOW_WIDTH // 2, 200), "EASY"),
            Button((WINDOW_WIDTH // 2, 300), "MEDIUM"),
            Button((WINDOW_WIDTH // 2, 400), "HARD"),
            Button((WINDOW_WIDTH // 2, 500), "BACK")
        ]
        
        # Menu Mode
        self.mode_buttons = [
            Button((WINDOW_WIDTH // 2, 200), "NORMAL"),
            Button((WINDOW_WIDTH // 2, 300), "OBSTACLE"),
            Button((WINDOW_WIDTH // 2, 400), "NO_WALL"),
            Button((WINDOW_WIDTH // 2, 500), "SPEED_BOOST"),
            Button((WINDOW_WIDTH // 2, 600), "BOMB"),
            Button((WINDOW_WIDTH // 2, 700), "BACK")
        ]

    def draw_background(self):
        # Vẽ ảnh nền
        screen.blit(self.background, (0, 0))
        
        # Thêm lớp overlay để làm tối ảnh nền một chút
        overlay = pg.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Màu đen với độ trong suốt 50%
        screen.blit(overlay, (0, 0))

    def handle_events(self):
        """Xử lý sự kiện cho menu"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                return False
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.running = False
                return False
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pg.mouse.get_pos()
                if self.current_state == "MAIN":
                    for button in self.main_buttons:
                        if button.is_clicked(mouse_pos):
                            if 'CLICK' in SOUNDS:
                                SOUNDS['CLICK'].play()
                            if button.text == "START":
                                print(f"Starting game with difficulty: {self.difficulty}, mode: {self.game_mode}")
                                return ("START", self.difficulty, self.game_mode)
                            elif button.text == "SPEED":
                                self.current_state = "SPEED"
                                return "SPEED"
                            elif button.text == "MODE":
                                self.current_state = "MODE"
                                return "MODE"
                            elif button.text == "QUIT":
                                self.running = False
                                return False
                elif self.current_state == "SPEED":
                    for button in self.speed_buttons:
                        if button.is_clicked(mouse_pos):
                            if 'CLICK' in SOUNDS:
                                SOUNDS['CLICK'].play()
                            if button.text in ["EASY", "MEDIUM", "HARD"]:
                                self.difficulty = button.text
                                self.current_state = "MAIN"
                                return "MAIN"
                            elif button.text == "BACK":
                                self.current_state = "MAIN"
                                return "MAIN"
                elif self.current_state == "MODE":
                    for button in self.mode_buttons:
                        if button.is_clicked(mouse_pos):
                            if 'CLICK' in SOUNDS:
                                SOUNDS['CLICK'].play()
                            if button.text in ["NORMAL", "OBSTACLE", "NO_WALL", "SPEED_BOOST", "BOMB"]:
                                self.game_mode = button.text
                                print(f"Game mode changed to: {self.game_mode}")
                                self.current_state = "MAIN"
                                return "MAIN"
                            elif button.text == "BACK":
                                self.current_state = "MAIN"
                                return "MAIN"
        return True

    def run_main_menu(self):
        self.draw_background()
        
        mouse_pos = pg.mouse.get_pos()
        for button in self.main_buttons:
            button.check_hover(mouse_pos)
            button.update()
        
        pg.display.flip()
        return self.handle_events()

    def run_speed_menu(self):
        self.draw_background()
        
        mouse_pos = pg.mouse.get_pos()
        for button in self.speed_buttons:
            button.check_hover(mouse_pos)
            button.update()
        
        pg.display.flip()
        return self.handle_events()

    def run_mode_menu(self):
        self.draw_background()
        
        mouse_pos = pg.mouse.get_pos()
        for button in self.mode_buttons:
            button.check_hover(mouse_pos)
            button.update()
        
        pg.display.flip()
        return self.handle_events()

    def run(self):
        while self.running:
            if self.current_state == "MAIN":
                result = self.run_main_menu()
                if result == "SPEED":
                    self.current_state = "SPEED"
                elif result == "MODE":
                    self.current_state = "MODE"
                elif isinstance(result, tuple) and result[0] == "START":
                    return result
                elif result is False:
                    return False
            elif self.current_state == "SPEED":
                result = self.run_speed_menu()
                if result == "MAIN":
                    self.current_state = "MAIN"
                elif result is False:
                    return False
            elif self.current_state == "MODE":
                result = self.run_mode_menu()
                if result == "MAIN":
                    self.current_state = "MAIN"
                elif result is False:
                    return False

    def draw_menu(self):
        """Vẽ menu chính"""
        # Vẽ nền menu
        s = pg.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pg.SRCALPHA)
        pg.draw.rect(s, (*COLORS['LIGHT_BLUE'], 200), s.get_rect(), border_radius=10)
        screen.blit(s, (0, 0))
        
        # Vẽ tiêu đề
        title = FONTS['LARGE'].render("SNAKE GAME", True, COLORS['BROWN'])
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 100))
        screen.blit(title, title_rect)
        
        # Vẽ các nút
        button_width = 300
        button_height = 50
        button_margin = 20
        start_y = 200
        
        # Nút chọn độ khó
        difficulty_text = f"Difficulty: {self.difficulty}"
        difficulty_rect = pg.Rect(
            (WINDOW_WIDTH - button_width)//2,
            start_y,
            button_width,
            button_height
        )
        self.draw_button(difficulty_text, difficulty_rect)
        
        # Nút chọn chế độ chơi
        mode_text = f"Game Mode: {self.game_mode}"
        mode_rect = pg.Rect(
            (WINDOW_WIDTH - button_width)//2,
            start_y + button_height + button_margin,
            button_width,
            button_height
        )
        self.draw_button(mode_text, mode_rect)
        
        # Nút Start
        start_rect = pg.Rect(
            (WINDOW_WIDTH - button_width)//2,
            start_y + (button_height + button_margin) * 2,
            button_width,
            button_height
        )
        self.draw_button("START", start_rect)
        
        # Nút Quit
        quit_rect = pg.Rect(
            (WINDOW_WIDTH - button_width)//2,
            start_y + (button_height + button_margin) * 3,
            button_width,
            button_height
        )
        self.draw_button("QUIT", quit_rect)
        
        # Lưu vị trí các nút để xử lý click
        self.buttons = {
            'difficulty': difficulty_rect,
            'mode': mode_rect,
            'start': start_rect,
            'quit': quit_rect
        }

    def handle_click(self, pos):
        """Xử lý sự kiện click chuột"""
        for button_name, rect in self.buttons.items():
            if rect.collidepoint(pos):
                if button_name == 'difficulty':
                    # Chuyển đổi độ khó
                    difficulties = list(GAME_CONFIG['SPEEDS'].keys())
                    current_index = difficulties.index(self.difficulty)
                    self.difficulty = difficulties[(current_index + 1) % len(difficulties)]
                elif button_name == 'mode':
                    # Chuyển đổi chế độ chơi
                    modes = ["NORMAL", "OBSTACLE", "NO_WALL", "SPEED_BOOST", "BOMB"]
                    current_index = modes.index(self.game_mode) if self.game_mode in modes else 0
                    self.game_mode = modes[(current_index + 1) % len(modes)]
                elif button_name == 'start':
                    return ("START", self.difficulty, self.game_mode)
                elif button_name == 'quit':
                    return False
        return None 