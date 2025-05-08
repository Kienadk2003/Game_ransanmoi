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
            Button((WINDOW_WIDTH // 2, 400), "BACK")
        ]

    def draw_background(self):
        # Vẽ nền với hiệu ứng gradient động
        for y in range(WINDOW_HEIGHT):
            color = (
                int(COLORS['ORANGE'][0] * (1 - y/WINDOW_HEIGHT) + COLORS['BROWN'][0] * (y/WINDOW_HEIGHT)),
                int(COLORS['ORANGE'][1] * (1 - y/WINDOW_HEIGHT) + COLORS['BROWN'][1] * (y/WINDOW_HEIGHT)),
                int(COLORS['ORANGE'][2] * (1 - y/WINDOW_HEIGHT) + COLORS['BROWN'][2] * (y/WINDOW_HEIGHT))
            )
            pg.draw.line(screen, color, (0, y), (WINDOW_WIDTH, y))

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
                            if button.text in ["NORMAL", "OBSTACLE"]:
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