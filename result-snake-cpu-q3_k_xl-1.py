import pygame
import sys
import random
import math

# Инициализация Pygame
pygame.init()

# Размеры экрана
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# Цветовая гамма
BACKGROUND = (15, 30, 45)
GRID_COLOR = (25, 45, 65)
SNAKE_HEAD = (0, 200, 150)
SNAKE_BODY = (0, 180, 120)
FOOD_COLOR = (220, 80, 60)
SPECIAL_FOOD_COLOR = (255, 215, 0)
TEXT_COLOR = (230, 230, 230)
BUTTON_COLOR = (0, 150, 120)
BUTTON_HOVER = (0, 180, 150)
MENU_BG = (20, 40, 60, 200)

# Скорость игры
FPS = 10

class Snake:
    def __init__(self):
        self.reset()
        self.direction = "RIGHT"
        self.next_direction = "RIGHT"
    
    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        for i in range(1, 3):
            self.positions.append((GRID_WIDTH // 2 - i, GRID_HEIGHT // 2))
        self.score = 0
        self.growth_pending = 0
        self.glow_effect = 0
        self.speed_boost = 0
    
    def get_head_position(self):
        return self.positions[0]
    
    def update(self):
        # Обновление направления
        self.direction = self.next_direction
        
        # Получение позиции головы
        head = self.get_head_position()
        
        # Расчет новой позиции головы
        if self.direction == "UP":
            new_pos = (head[0], head[1] - 1)
        elif self.direction == "DOWN":
            new_pos = (head[0], head[1] + 1)
        elif self.direction == "LEFT":
            new_pos = (head[0] - 1, head[1])
        elif self.direction == "RIGHT":
            new_pos = (head[0] + 1, head[1])
        
        # Добавление новой позиции головы
        self.positions.insert(0, new_pos)
        
        # Удаление хвоста, если змея не растет
        if self.growth_pending > 0:
            self.growth_pending -= 1
        else:
            self.positions.pop()
        
        # Обновление эффекта свечения
        self.glow_effect = max(0, self.glow_effect - 1)
        
        # Обновление ускорения
        if self.speed_boost > 0:
            self.speed_boost -= 1
    
    def grow(self):
        self.growth_pending += 1
        self.glow_effect = 15  # Эффект свечения при поедании
    
    def draw(self, surface):
        for i, pos in enumerate(self.positions):
            # Определение цвета сегмента змеи
            color = SNAKE_HEAD if i == 0 else SNAKE_BODY
            
            # Эффект свечения для головы при поедании
            if i == 0 and self.glow_effect > 0:
                glow = min(255, 150 + self.glow_effect * 5)
                color = (min(255, color[0] + glow//3), 
                         min(255, color[1] + glow//3), 
                         min(255, color[2] + glow//3))
            
            # Рисование сегмента змеи
            rect = pygame.Rect(pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, (color[0]//2, color[1]//2, color[2]//2), rect, 1)
            
            # Рисование глаз
            if i == 0:
                # Определение позиции глаз в зависимости от направления
                eye_size = GRID_SIZE // 5
                if self.direction == "UP":
                    left_eye = (rect.left + rect.width//3, rect.top + rect.height//3)
                    right_eye = (rect.left + 2*rect.width//3, rect.top + rect.height//3)
                elif self.direction == "DOWN":
                    left_eye = (rect.left + rect.width//3, rect.top + 2*rect.height//3)
                    right_eye = (rect.left + 2*rect.width//3, rect.top + 2*rect.height//3)
                elif self.direction == "LEFT":
                    left_eye = (rect.left + rect.width//3, rect.top + rect.height//3)
                    right_eye = (rect.left + rect.width//3, rect.top + 2*rect.height//3)
                else:  # RIGHT
                    left_eye = (rect.left + 2*rect.width//3, rect.top + rect.height//3)
                    right_eye = (rect.left + 2*rect.width//3, rect.top + 2*rect.height//3)
                
                pygame.draw.circle(surface, (30, 30, 50), left_eye, eye_size)
                pygame.draw.circle(surface, (30, 30, 50), right_eye, eye_size)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = FOOD_COLOR
        self.spawn()
        self.pulse = 0
        self.special = False
        self.lifetime = 0
    
    def spawn(self, snake_positions=None):
        # Создаем новую еду, избегая позиций змеи
        if snake_positions is None:
            snake_positions = []
            
        available_positions = [
            (x, y) 
            for x in range(GRID_WIDTH) 
            for y in range(GRID_HEIGHT) 
            if (x, y) not in snake_positions
        ]
        
        if available_positions:
            self.position = random.choice(available_positions)
            self.pulse = 0
            # Случайно определяем, будет ли это специальная еда
            self.special = random.random() < 0.2
            self.lifetime = 100 if self.special else 0
            self.color = SPECIAL_FOOD_COLOR if self.special else FOOD_COLOR
            return True
        return False
    
    def update(self):
        # Пульсация еды
        self.pulse = (self.pulse + 0.1) % (2 * math.pi)
        
        # Уменьшение времени жизни для специальной еды
        if self.special:
            self.lifetime -= 1
            if self.lifetime <= 0:
                self.spawn()
    
    def draw(self, surface):
        # Расчет эффекта пульсации
        pulse_offset = math.sin(self.pulse) * 3
        
        # Рисование еды
        rect = pygame.Rect(
            self.position[0] * GRID_SIZE + GRID_SIZE//2,
            self.position[1] * GRID_SIZE + GRID_SIZE//2,
            GRID_SIZE - 4,
            GRID_SIZE - 4
        )
        
        # Цвет для пульсации
        pulse_color = (
            min(255, self.color[0] + 50 * math.sin(self.pulse)),
            min(255, self.color[1] + 50 * math.sin(self.pulse)),
            min(255, self.color[2] + 50 * math.sin(self.pulse))
        )
        
        pygame.draw.circle(surface, pulse_color, rect.center, GRID_SIZE//2 - 2)
        
        # Обводка для специальной еды
        if self.special:
            pygame.draw.circle(surface, (255, 255, 200, 150), rect.center, GRID_SIZE//2 - 1, 2)
            
            # Таймер для специальной еды
            timer_rect = pygame.Rect(
                self.position[0] * GRID_SIZE + 2,
                self.position[1] * GRID_SIZE - 8,
                GRID_SIZE - 4,
                4
            )
            pygame.draw.rect(surface, (200, 200, 200), timer_rect)
            pygame.draw.rect(surface, (255, 215, 0), (
                timer_rect.x,
                timer_rect.y,
                (GRID_SIZE - 4) * self.lifetime / 100,
                4
            ))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Змейка")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 24)
        self.title_font = pygame.font.SysFont('Arial', 48, bold=True)
        self.small_font = pygame.font.SysFont('Arial', 16)
        
        self.snake = Snake()
        self.food = Food()
        self.food.spawn(self.snake.positions)
        
        self.game_state = "MENU"  # MENU, PLAYING, GAME_OVER, PAUSE
        self.score = 0
        self.high_score = 0
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if self.game_state == "PLAYING":
                    if event.key == pygame.K_UP and self.snake.direction != "DOWN":
                        self.snake.next_direction = "UP"
                    elif event.key == pygame.K_DOWN and self.snake.direction != "UP":
                        self.snake.next_direction = "DOWN"
                    elif event.key == pygame.K_LEFT and self.snake.direction != "RIGHT":
                        self.snake.next_direction = "LEFT"
                    elif event.key == pygame.K_RIGHT and self.snake.direction != "LEFT":
                        self.snake.next_direction = "RIGHT"
                    elif event.key == pygame.K_ESCAPE:
                        self.game_state = "PAUSE"
                
                elif self.game_state == "MENU" or self.game_state == "GAME_OVER":
                    if event.key == pygame.K_RETURN:
                        self.reset_game()
                        self.game_state = "PLAYING"
                
                elif self.game_state == "PAUSE":
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = "PLAYING"
                    elif event.key == pygame.K_m:
                        self.game_state = "MENU"
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # Обработка кнопок в меню
                if self.game_state == "MENU" or self.game_state == "GAME_OVER":
                    if self.play_button.collidepoint(mouse_pos):
                        self.reset_game()
                        self.game_state = "PLAYING"
                    elif self.quit_button.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
                
                # Обработка кнопок в паузе
                elif self.game_state == "PAUSE":
                    if self.resume_button.collidepoint(mouse_pos):
                        self.game_state = "PLAYING"
                    elif self.menu_button.collidepoint(mouse_pos):
                        self.game_state = "MENU"

    def update(self):
        if self.game_state == "PLAYING":
            self.snake.update()
            
            # Проверка столкновения с едой
            if self.snake.get_head_position() == self.food.position:
                self.snake.grow()
                self.score += 10 if self.food.special else 1
                self.high_score = max(self.high_score, self.score)
                
                # Ускорение змеи при поедании специальной еды
                if self.food.special:
                    self.snake.speed_boost = 30
                
                # Спавн новой еды
                self.food.spawn(self.snake.positions)
            
            # Обновление еды
            self.food.update()
            
            # Проверка столкновения с границами
            head = self.snake.get_head_position()
            if (head[0] < 0 or head[0] >= GRID_WIDTH or 
                head[1] < 0 or head[1] >= GRID_HEIGHT):
                self.game_state = "GAME_OVER"
            
            # Проверка столкновения с телом
            for position in self.snake.positions[1:]:
                if position == head:
                    self.game_state = "GAME_OVER"

    def draw(self):
        # Отрисовка фона
        self.screen.fill(BACKGROUND)
        
        # Отрисовка сетки
        for x in range(0, WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (WIDTH, y))
        
        # Отрисовка змеи и еды
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        
        # Отрисовка счета
        score_text = self.font.render(f"Счет: {self.score}", True, TEXT_COLOR)
        high_score_text = self.font.render(f"Рекорд: {self.high_score}", True, TEXT_COLOR)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(high_score_text, (10, 40))
        
        # Указание на специальную еду
        if self.food.special:
            special_text = self.small_font.render("Желтая еда дает 10 очков!", True, SPECIAL_FOOD_COLOR)
            self.screen.blit(special_text, (WIDTH // 2 - special_text.get_width() // 2, 40))
        
        # Отрисовка меню
        if self.game_state == "MENU":
            self.draw_menu()
        elif self.game_state == "GAME_OVER":
            self.draw_game_over()
        elif self.game_state == "PAUSE":
            self.draw_pause_menu()
        
        pygame.display.flip()
    
    def draw_menu(self):
        # Полупрозрачный фон меню
        s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        s.fill(MENU_BG)
        self.screen.blit(s, (0, 0))
        
        # Заголовок
        title = self.title_font.render("ЗМЕЙКА", True, TEXT_COLOR)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
        
        # Кнопка "Играть"
        self.play_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
        pygame.draw.rect(self.screen, BUTTON_COLOR, self.play_button, border_radius=10)
        pygame.draw.rect(self.screen, TEXT_COLOR, self.play_button, 2, border_radius=10)
        
        if self.play_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.screen, BUTTON_HOVER, self.play_button, border_radius=10)
        
        play_text = self.font.render("Играть", True, TEXT_COLOR)
        self.screen.blit(play_text, (self.play_button.centerx - play_text.get_width() // 2, 
                                      self.play_button.centery - play_text.get_height() // 2))
        
        # Кнопка "Выход"
        self.quit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 70, 200, 50)
        pygame.draw.rect(self.screen, BUTTON_COLOR, self.quit_button, border_radius=10)
        pygame.draw.rect(self.screen, TEXT_COLOR, self.quit_button, 2, border_radius=10)
        
        if self.quit_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.screen, BUTTON_HOVER, self.quit_button, border_radius=10)
        
        quit_text = self.font.render("Выход", True, TEXT_COLOR)
        self.screen.blit(quit_text, (self.quit_button.centerx - quit_text.get_width() // 2, 
                                     self.quit_button.centery - quit_text.get_height() // 2))
        
        # Управление
        controls = [
            "Управление:",
            "Стрелки - движение",
            "ESC - пауза",
            "Меню - кнопки мыши"
        ]
        
        for i, text in enumerate(controls):
            c_text = self.small_font.render(text, True, TEXT_COLOR)
            self.screen.blit(c_text, (WIDTH // 2 - c_text.get_width() // 2, 
                                     HEIGHT - 150 + i * 25))
    
    def draw_game_over(self):
        # Полупрозрачный фон
        s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        s.fill(MENU_BG)
        self.screen.blit(s, (0, 0))
        
        # Текст "Игра окончена"
        game_over = self.title_font.render("ИГРА ОКОНЧЕНА", True, TEXT_COLOR)
        self.screen.blit(game_over, (WIDTH // 2 - game_over.get_width() // 2, HEIGHT // 3))
        
        # Счет
        score_text = self.font.render(f"Ваш счет: {self.score}", True, TEXT_COLOR)
        self.screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
        
        # Рекорд
        high_score_text = self.font.render(f"Рекорд: {self.high_score}", True, TEXT_COLOR)
        self.screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2 + 40))
        
        # Кнопка "Играть снова"
        self.play_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50)
        pygame.draw.rect(self.screen, BUTTON_COLOR, self.play_button, border_radius=10)
        pygame.draw.rect(self.screen, TEXT_COLOR, self.play_button, 2, border_radius=10)
        
        if self.play_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.screen, BUTTON_HOVER, self.play_button, border_radius=10)
        
        play_text = self.font.render("Играть снова", True, TEXT_COLOR)
        self.screen.blit(play_text, (self.play_button.centerx - play_text.get_width() // 2, 
                                     self.play_button.centery - play_text.get_height() // 2))
        
        # Кнопка "Меню"
        self.menu_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 170, 200, 50)
        pygame.draw.rect(self.screen, BUTTON_COLOR, self.menu_button, border_radius=10)
        pygame.draw.rect(self.screen, TEXT_COLOR, self.menu_button, 2, border_radius=10)
        
        if self.menu_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.screen, BUTTON_HOVER, self.menu_button, border_radius=10)
        
        menu_text = self.font.render("Меню", True, TEXT_COLOR)
        self.screen.blit(menu_text, (self.menu_button.centerx - menu_text.get_width() // 2, 
                                   self.menu_button.centery - menu_text.get_height() // 2))
    
    def draw_pause_menu(self):
        # Полупрозрачный фон
        s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        s.fill(MENU_BG)
        self.screen.blit(s, (0, 0))
        
        # Текст "Пауза"
        pause = self.title_font.render("ПАУЗА", True, TEXT_COLOR)
        self.screen.blit(pause, (WIDTH // 2 - pause.get_width() // 2, HEIGHT // 3))
        
        # Кнопка "Продолжить"
        self.resume_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
        pygame.draw.rect(self.screen, BUTTON_COLOR, self.resume_button, border_radius=10)
        pygame.draw.rect(self.screen, TEXT_COLOR, self.resume_button, 2, border_radius=10)
        
        if self.resume_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.screen, BUTTON_HOVER, self.resume_button, border_radius=10)
        
        resume_text = self.font.render("Продолжить", True, TEXT_COLOR)
        self.screen.blit(resume_text, (self.resume_button.centerx - resume_text.get_width() // 2, 
                                      self.resume_button.centery - resume_text.get_height() // 2))
        
        # Кнопка "Меню"
        self.menu_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 70, 200, 50)
        pygame.draw.rect(self.screen, BUTTON_COLOR, self.menu_button, border_radius=10)
        pygame.draw.rect(self.screen, TEXT_COLOR, self.menu_button, 2, border_radius=10)
        
        if self.menu_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.screen, BUTTON_HOVER, self.menu_button, border_radius=10)
        
        menu_text = self.font.render("Меню", True, TEXT_COLOR)
        self.screen.blit(menu_text, (self.menu_button.centerx - menu_text.get_width() // 2, 
                                   self.menu_button.centery - menu_text.get_height() // 2))
    
    def reset_game(self):
        self.snake.reset()
        self.food.spawn(self.snake.positions)
        self.score = 0
    
    def run(self):
        while True:
            self.handle_events()
            
            # Регулировка скорости в зависимости от ускорения
            if self.snake.speed_boost > 0:
                self.clock.tick(FPS * 1.5)
            else:
                self.clock.tick(FPS)
            
            if self.game_state == "PLAYING":
                self.update()
            
            self.draw()

# Запуск игры
if __name__ == "__main__":
    game = Game()
    game.run()
