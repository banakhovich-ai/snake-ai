import pygame
import sys
import random
import math

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

# Цветовая гамма
BACKGROUND = (15, 20, 30)
GRID_COLOR = (30, 35, 45)
SNAKE_COLOR = (100, 255, 150)
SNAKE_HEAD_COLOR = (70, 220, 120)
FOOD_COLOR = (255, 80, 80)
TEXT_COLOR = (220, 220, 220)
BUTTON_COLOR = (60, 150, 200)
BUTTON_HOVER = (80, 170, 220)
ANIMATION_COLORS = [(255, 215, 0), (255, 165, 0), (255, 100, 0)]

# Класс змейки
class Snake:
    def __init__(self):
        self.reset()
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.grow = False
        
    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        for i in range(1, self.length):
            self.positions.append((self.positions[0][0] - i, self.positions[0][1]))
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.grow = False
        
    def get_head_position(self):
        return self.positions[0]
    
    def update(self):
        # Обновление направления
        self.direction = self.next_direction
        
        # Получение текущей позиции головы
        head = self.get_head_position()
        
        # Расчет новой позиции головы
        dx, dy = self.direction
        new_x = (head[0] + dx) % GRID_WIDTH
        new_y = (head[1] + dy) % GRID_HEIGHT
        new_head = (new_x, new_y)
        
        # Проверка столкновения с собой
        if new_head in self.positions[1:]:
            return False
        
        # Добавление новой головы
        self.positions.insert(0, new_head)
        
        # Удаление хвоста, если не нужно расти
        if not self.grow:
            self.positions.pop()
        else:
            self.grow = False
            self.length += 1
            
        return True
    
    def change_direction(self, direction):
        # Запрет поворота на 180 градусов
        if (self.direction[0] * -1, self.direction[1] * -1) != direction:
            self.next_direction = direction
    
    def draw(self, surface):
        for i, pos in enumerate(self.positions):
            # Рисование сегментов змейки
            rect = pygame.Rect(pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            
            # Голова
            if i == 0:
                color = SNAKE_HEAD_COLOR
            # Тело
            else:
                color = SNAKE_COLOR
            
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, (40, 80, 60), rect, 1)
            
            # Глаза на голове
            if i == 0:
                eye_size = GRID_SIZE // 4
                # Левый глаз (относительно направления движения)
                if self.direction == (1, 0):  # вправо
                    left_eye = (rect.left + GRID_SIZE * 3//4, rect.top + GRID_SIZE // 3)
                elif self.direction == (-1, 0): # влево
                    left_eye = (rect.left + GRID_SIZE // 4, rect.top + GRID_SIZE // 3)
                elif self.direction == (0, 1):  # вниз
                    left_eye = (rect.left + GRID_SIZE // 3, rect.top + GRID_SIZE * 3//4)
                else:  # вверх
                    left_eye = (rect.left + GRID_SIZE // 3, rect.top + GRID_SIZE // 4)
                
                # Правый глаз
                if self.direction == (1, 0) or self.direction == (-1, 0):
                    right_eye = (left_eye[0], left_eye[1] + GRID_SIZE // 3)
                else:
                    right_eye = (left_eye[0] + GRID_SIZE // 3, left_eye[1])
                
                pygame.draw.circle(surface, (20, 20, 30), left_eye, eye_size)
                pygame.draw.circle(surface, (20, 20, 30), right_eye, eye_size)

# Класс еды
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = FOOD_COLOR
        self.randomize_position()
        self.animation_timer = 0
        self.animation_radius = 0
        self.max_radius = GRID_SIZE * 1.5
        
    def randomize_position(self, snake_positions=None):
        while True:
            self.position = (random.randint(0, GRID_WIDTH - 1), 
                            random.randint(0, GRID_HEIGHT - 1))
            if snake_positions is None or self.position not in snake_positions:
                break
    
    def start_animation(self):
        self.animation_timer = 20  # Длительность анимации
        self.animation_radius = 0
    
    def update_animation(self):
        if self.animation_timer > 0:
            self.animation_timer -= 1
            self.animation_radius = self.max_radius * (1 - self.animation_timer / 20)
    
    def draw(self, surface):
        # Рисование основного объекта еды
        rect = pygame.Rect(self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, 
                          GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, (180, 50, 50), rect, 2)
        
        # Рисование анимации поедания
        if self.animation_timer > 0:
            center = (rect.centerx, rect.centery)
            for i in range(3):
                radius = self.animation_radius * (1 + i * 0.3)
                alpha = 200 - i * 50
                color_idx = min(i, len(ANIMATION_COLORS)-1)
                color = ANIMATION_COLORS[color_idx]
                s = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
                pygame.draw.circle(s, (*color, alpha), (radius, radius), radius)
                surface.blit(s, (center[0] - radius, center[1] - radius))

# Класс кнопки
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.hovered = False
        
    def draw(self, surface, font):
        color = BUTTON_HOVER if self.hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, (120, 180, 220), self.rect, 2, border_radius=10)
        
        text_surf = font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
    
    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        return self.hovered
    
    def check_click(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

# Основной класс игры
class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Змейка с изюминкой")
        self.clock = pygame.time.Clock()
        
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 24)
        
        self.snake = Snake()
        self.food = Food()
        self.food.randomize_position(self.snake.positions)
        
        self.score = 0
        self.game_over = False
        self.in_menu = True
        self.special_mode = False
        self.special_timer = 0
        
        # Создание кнопок меню
        button_width, button_height = 200, 50
        center_x = WIDTH // 2 - button_width // 2
        self.start_button = Button(center_x, HEIGHT // 2 - 40, button_width, button_height, "Начать игру")
        self.quit_button = Button(center_x, HEIGHT // 2 + 40, button_width, button_height, "Выход")
        
        # Создание кнопок после игры
        self.restart_button = Button(center_x, HEIGHT // 2 + 20, button_width, button_height, "Играть снова")
        self.menu_button = Button(center_x, HEIGHT // 2 + 90, button_width, button_height, "Меню")
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if self.in_menu:
                # Обработка событий меню
                pos = pygame.mouse.get_pos()
                self.start_button.check_hover(pos)
                self.quit_button.check_hover(pos)
                
                if self.start_button.check_click(pos, event):
                    self.in_menu = False
                    self.game_over = False
                    self.reset_game()
                elif self.quit_button.check_click(pos, event):
                    pygame.quit()
                    sys.exit()
            
            elif self.game_over:
                # Обработка событий после игры
                pos = pygame.mouse.get_pos()
                self.restart_button.check_hover(pos)
                self.menu_button.check_hover(pos)
                
                if self.restart_button.check_click(pos, event):
                    self.reset_game()
                    self.game_over = False
                elif self.menu_button.check_click(pos, event):
                    self.in_menu = True
            
            elif not self.game_over:
                # Обработка событий игры
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction((0, -1))
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction((0, 1))
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction((-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction((1, 0))
                    elif event.key == pygame.K_SPACE:
                        self.special_mode = not self.special_mode
                        self.special_timer = 0
    
    def reset_game(self):
        self.snake.reset()
        self.food.randomize_position(self.snake.positions)
        self.score = 0
        self.game_over = False
        self.special_mode = False
        self.special_timer = 0
    
    def update(self):
        if not self.game_over and not self.in_menu:
            # Обновление змейки
            if not self.snake.update():
                self.game_over = True
                return
            
            # Обновление анимации еды
            self.food.update_animation()
            
            # Проверка съедания еды
            if self.snake.get_head_position() == self.food.position:
                # Анимация поедания
                self.food.start_animation()
                
                # Увеличение счета
                self.score += 1
                
                # Запуск специального режима с шансом 20%
                if random.random() < 0.2 and not self.special_mode:
                    self.special_mode = True
                    self.special_timer = 0
                
                # Змейка растет
                self.snake.grow = True
                
                # Появление новой еды
                self.food.randomize_position(self.snake.positions)
            
            # Обновление специального режима
            if self.special_mode:
                self.special_timer += 1
                if self.special_timer > 150:  # Специальный режим длится 15 секунд
                    self.special_mode = False
    
    def draw_grid(self):
        # Рисование сетки игрового поля
        for x in range(0, WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, HEIGHT), 1)
        for y in range(0, HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (WIDTH, y), 1)
    
    def draw(self):
        self.screen.fill(BACKGROUND)
        
        if self.in_menu:
            # Отрисовка меню
            title = self.font.render("ЗМЕЙКА", True, TEXT_COLOR)
            self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
            
            # Отрисовка кнопок
            self.start_button.draw(self.screen, self.font)
            self.quit_button.draw(self.screen, self.font)
            
            # Подсказка
            hint = self.small_font.render("Управление: стрелки, Специальный режим: пробел", True, (180, 180, 180))
            self.screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 50))
            
            # Изиминка: плавающая змейка
            time = pygame.time.get_ticks() / 1000
            offset_x = math.sin(time * 2) * 50
            offset_y = math.cos(time) * 30
            
            # Рисуем мини-змейку в меню
            positions = [(GRID_WIDTH // 2 + i, GRID_HEIGHT // 4) for i in range(5)]
            for i, pos in enumerate(positions):
                rect = pygame.Rect(
                    pos[0] * GRID_SIZE + offset_x, 
                    pos[1] * GRID_SIZE + offset_y, 
                    GRID_SIZE, GRID_SIZE
                )
                color = SNAKE_HEAD_COLOR if i == 0 else SNAKE_COLOR
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (40, 80, 60), rect, 1)
                
                # Рисуем мини-еду
                food_rect = pygame.Rect(
                    (positions[-1][0] + 3) * GRID_SIZE + offset_x, 
                    positions[-1][1] * GRID_SIZE + offset_y, 
                    GRID_SIZE, GRID_SIZE
                )
                pygame.draw.rect(self.screen, FOOD_COLOR, food_rect)
                pygame.draw.rect(self.screen, (180, 50, 50), food_rect, 2)
        
        elif self.game_over:
            # Отрисовка экрана завершения игры
            self.draw_grid()
            
            # Отрисовка змейки и еды (для визуализации)
            self.snake.draw(self.screen)
            self.food.draw(self.screen)
            
            game_over_text = self.font.render("ИГРА ОКОНЧЕНА", True, (255, 100, 100))
            self.screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 4))
            
            score_text = self.font.render(f"Счет: {self.score}", True, TEXT_COLOR)
            self.screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 3))
            
            # Отрисовка кнопок
            self.restart_button.draw(self.screen, self.font)
            self.menu_button.draw(self.screen, self.font)
        
        else:
            # Отрисовка игрового поля
            self.draw_grid()
            
            # Отрисовка змейки
            self.snake.draw(self.screen)
            
            # Отрисовка еды
            self.food.draw(self.screen)
            
            # Отрисовка счета
            score_text = self.font.render(f"Счет: {self.score}", True, TEXT_COLOR)
            self.screen.blit(score_text, (10, 10))
            
            # Отрисовка специального режима
            if self.special_mode:
                # Специальный эффект: меняющийся фон
                pulse = abs(math.sin(pygame.time.get_ticks() / 200))
                color_value = int(100 + 155 * pulse)
                overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                overlay.fill((255, 255, 100, 30))
                self.screen.blit(overlay, (0, 0))
                
                # Текст специального режима
                mode_text = self.small_font.render("СПЕЦИАЛЬНЫЙ РЕЖИМ!", True, (255, 255, 100))
                self.screen.blit(mode_text, (WIDTH - mode_text.get_width() - 10, 10))
                
                # Таймер
                time_left = (150 - self.special_timer) // 10
                timer_text = self.small_font.render(f"Осталось: {time_left}", True, (255, 255, 100))
                self.screen.blit(timer_text, (WIDTH - timer_text.get_width() - 10, 40))
            
            # Изиминка: случайные эффекты в специальном режиме
            if self.special_mode and random.random() < 0.05:
                # Создание случайных частиц
                for _ in range(20):
                    x = random.randint(0, WIDTH)
                    y = random.randint(0, HEIGHT)
                    size = random.randint(2, 5)
                    color = random.choice(ANIMATION_COLORS)
                    pygame.draw.circle(self.screen, color, (x, y), size)
        
        pygame.display.flip()
    
    def run(self):
        while True:
            self.handle_events()
            if not self.in_menu and not self.game_over:
                self.update()
            self.draw()
            self.clock.tick(FPS)

# Запуск игры
if __name__ == "__main__":
    game = SnakeGame()
    game.run()
