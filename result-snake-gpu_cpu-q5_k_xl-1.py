import pygame
import sys
import random
import math
from pygame.locals import *

# Инициализация Pygame
pygame.init()
pygame.mixer.init()

# Размеры окна
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = (HEIGHT - 60) // GRID_SIZE  # Оставляем место для панели управления

# Цветовая палитра
BACKGROUND = (15, 20, 25)
GRID_COLOR = (30, 35, 40)
SNAKE_COLOR = (50, 205, 50)
SNAKE_HEAD_COLOR = (34, 139, 34)
FOOD_COLOR = (220, 20, 60)
OBSTACLE_COLOR = (70, 130, 180)
TEXT_COLOR = (240, 240, 240)
BUTTON_COLOR = (75, 105, 135)
BUTTON_HOVER_COLOR = (95, 125, 155)
PANEL_COLOR = (25, 35, 45)
GOLD_COLOR = (255, 215, 0)
SPECIAL_FOOD_COLOR = (255, 165, 0)

# Создаем окно
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка с изюминкой")

# Шрифты
font_small = pygame.font.SysFont("Arial", 20)
font_medium = pygame.font.SysFont("Arial", 28)
font_large = pygame.font.SysFont("Arial", 48)
font_title = pygame.font.SysFont("Arial", 64, bold=True)

# Звуки
try:
    eat_sound = pygame.mixer.Sound(pygame.mixer.Sound(bytearray([0]*44)))  # Пустой звук
    crash_sound = pygame.mixer.Sound(pygame.mixer.Sound(bytearray([0]*44)))
except:
    # Заглушка, если звуки не работают
    class DummySound:
        def play(self): pass
    eat_sound = DummySound()
    crash_sound = DummySound()

# Класс для кнопок
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = BUTTON_COLOR
        self.hover_color = BUTTON_HOVER_COLOR
        self.current_color = self.color
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.current_color, self.rect, border_radius=8)
        pygame.draw.rect(surface, (120, 160, 200), self.rect, 2, border_radius=8)
        
        text_surf = font_medium.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)
    
    def handle_event(self, event):
        if event.type == MOUSEMOTION:
            self.current_color = self.hover_color if self.is_hovered(event.pos) else self.color
        if event.type == MOUSEBUTTONDOWN and self.is_hovered(event.pos):
            return True
        return False

# Класс для частиц (для анимации)
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 6)
        self.speed_x = random.uniform(-2, 2)
        self.speed_y = random.uniform(-2, 2)
        self.lifetime = random.randint(20, 40)
        
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.lifetime -= 1
        self.size = max(0, self.size - 0.1)
        
    def draw(self, surface):
        alpha = min(255, self.lifetime * 6)
        color = (self.color[0], self.color[1], self.color[2], int(alpha))
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), int(self.size))

# Класс для змейки
class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        self.score = 0
        self.grow_pending = 2  # Начальная длина
        self.speed = 10
        self.invincible = 0
        self.golden_food_active = False
        self.golden_food_timer = 0
        
    def get_head_position(self):
        return self.positions[0]
    
    def update(self):
        # Обновление таймеров
        if self.invincible > 0:
            self.invincible -= 1
            
        if self.golden_food_active:
            self.golden_food_timer -= 1
            if self.golden_food_timer <= 0:
                self.golden_food_active = False
        
        # Движение змейки
        head = self.get_head_position()
        x, y = self.direction
        new_x = (head[0] + x) % GRID_WIDTH
        new_y = (head[1] + y) % GRID_HEIGHT
        new_position = (new_x, new_y)
        
        # Проверка на столкновение с самой собой
        if new_position in self.positions[1:] and self.invincible <= 0:
            return False
        
        self.positions.insert(0, new_position)
        
        # Увеличение длины при необходимости
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.positions.pop()
            
        return True
    
    def grow(self):
        self.grow_pending += 1
        self.length += 1
    
    def activate_golden_food(self):
        self.golden_food_active = True
        self.golden_food_timer = 300  # 5 секунд при 60 FPS
    
    def draw(self, surface):
        for i, pos in enumerate(self.positions):
            # Рисование сегментов змейки
            color = SNAKE_HEAD_COLOR if i == 0 else SNAKE_COLOR
            rect = pygame.Rect(
                pos[0] * GRID_SIZE, 
                pos[1] * GRID_SIZE + 30,  # Сдвиг вниз для панели управления
                GRID_SIZE, 
                GRID_SIZE
            )
            pygame.draw.rect(surface, color, rect, 0, 5)
            
            # Рисование контура
            pygame.draw.rect(surface, (30, 100, 30), rect, 1, 5)
            
            # Если змейка "золотая", добавляем эффект
            if self.golden_food_active:
                glow_rect = pygame.Rect(
                    rect.x - 2, 
                    rect.y - 2, 
                    rect.width + 4, 
                    rect.height + 4
                )
                pygame.draw.rect(surface, GOLD_COLOR, glow_rect, 1, 7)
                
        # Эффект неуязвимости
        if self.invincible > 0:
            for pos in self.positions:
                alpha = min(255, self.invincible * 3)
                s = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
                pygame.draw.rect(s, (255, 255, 0, alpha), (0, 0, GRID_SIZE, GRID_SIZE), border_radius=5)
                surface.blit(s, (pos[0] * GRID_SIZE, pos[1] * GRID_SIZE + 30))

# Класс для еды
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.spawn()
        self.particles = []
        self.special = False
        self.special_timer = 0
        
    def spawn(self, snake_positions=None, obstacles=None):
        # Генерация новой позиции
        valid_positions = []
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                pos = (x, y)
                if snake_positions and pos in snake_positions:
                    continue
                if obstacles and pos in obstacles:
                    continue
                valid_positions.append(pos)
                
        if valid_positions:
            self.position = random.choice(valid_positions)
            # Случайно делаем еду "особой" с вероятностью 15%
            self.special = random.random() < 0.15
            if self.special:
                self.special_timer = 300  # 5 секунд при 60 FPS
            return True
        return False
    
    def update(self):
        if self.special:
            self.special_timer -= 1
            if self.special_timer <= 0:
                self.special = False
                
        # Обновление частиц
        for particle in self.particles[:]:
            particle.update()
            if particle.lifetime <= 0:
                self.particles.remove(particle)
                
    def draw(self, surface):
        # Рисование еды
        x, y = self.position
        rect = pygame.Rect(
            x * GRID_SIZE, 
            y * GRID_SIZE + 30,  # Сдвиг вниз для панели управления
            GRID_SIZE, 
            GRID_SIZE
        )
        
        # Особая еда рисуется по-другому
        if self.special:
            pygame.draw.rect(surface, SPECIAL_FOOD_COLOR, rect, 0, 10)
            
            # Анимация пульсации
            pulse = abs(math.sin(pygame.time.get_ticks() / 200)) * 5
            glow_rect = pygame.Rect(
                rect.x - pulse, 
                rect.y - pulse, 
                rect.width + pulse * 2, 
                rect.height + pulse * 2
            )
            pygame.draw.rect(surface, (255, 215, 0, 100), glow_rect, 2, 15)
            
            # Добавление частиц
            if random.random() < 0.3:
                self.particles.append(Particle(
                    rect.centerx, 
                    rect.centery, 
                    SPECIAL_FOOD_COLOR
                ))
        else:
            pygame.draw.rect(surface, FOOD_COLOR, rect, 0, 10)
            
        # Рисование частиц
        for particle in self.particles:
            particle.draw(surface)
            
        # Контур
        pygame.draw.rect(surface, (180, 40, 60), rect, 2, 10)

# Класс для препятствий
class Obstacle:
    def __init__(self):
        self.positions = []
        
    def generate(self, snake_positions, food_position):
        # Очистка старых препятствий
        self.positions = []
        
        # Генерация новых препятствий (количество зависит от счета)
        num_obstacles = min(10 + len(snake_positions) // 5, 30)
        
        for _ in range(num_obstacles):
            while True:
                x = random.randint(0, GRID_WIDTH - 1)
                y = random.randint(0, GRID_HEIGHT - 1)
                pos = (x, y)
                
                # Убедимся, что препятствие не на змейке и не на еде
                if pos in snake_positions:
                    continue
                if pos == food_position:
                    continue
                if pos in self.positions:
                    continue
                    
                self.positions.append(pos)
                break
                
    def draw(self, surface):
        for pos in self.positions:
            x, y = pos
            rect = pygame.Rect(
                x * GRID_SIZE, 
                y * GRID_SIZE + 30,  # Сдвиг вниз для панели управления
                GRID_SIZE, 
                GRID_SIZE
            )
            pygame.draw.rect(surface, OBSTACLE_COLOR, rect, 0, 5)
            pygame.draw.rect(surface, (50, 90, 130), rect, 2, 5)

# Игровые состояния
MENU = 0
PLAYING = 1
GAME_OVER = 2
PAUSED = 3

# Создаем объекты игры
snake = Snake()
food = Food()
obstacles = Obstacle()

# Кнопки меню
start_button = Button(WIDTH // 2 - 100, HEIGHT // 2, 200, 50, "Начать игру")
restart_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 60, 200, 50, "Играть снова")
quit_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 120, 200, 50, "Выход")

# Генерация препятствий в первый раз
obstacles.generate(snake.positions, food.position)

# Начальное состояние
game_state = MENU
game_speed = 10
clock = pygame.time.Clock()

# Главный игровой цикл
while True:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
        # Обработка нажатия клавиш
        if event.type == KEYDOWN:
            if game_state == PLAYING or game_state == PAUSED:
                # Управление змейкой
                if event.key == K_UP and snake.direction != (0, 1):
                    snake.direction = (0, -1)
                elif event.key == K_DOWN and snake.direction != (0, -1):
                    snake.direction = (0, 1)
                elif event.key == K_LEFT and snake.direction != (1, 0):
                    snake.direction = (-1, 0)
                elif event.key == K_RIGHT and snake.direction != (-1, 0):
                    snake.direction = (1, 0)
                    
                # Пауза
                if event.key == K_p:
                    game_state = PAUSED if game_state == PLAYING else PLAYING
                    
            if event.key == K_ESCAPE:
                if game_state == PLAYING or game_state == PAUSED:
                    game_state = MENU
                    
        # Обработка кнопок
        if game_state == MENU:
            if start_button.handle_event(event):
                game_state = PLAYING
                snake.reset()
                food.spawn(snake.positions, obstacles.positions)
                obstacles.generate(snake.positions, food.position)
                
        elif game_state == GAME_OVER:
            if restart_button.handle_event(event):
                game_state = PLAYING
                snake.reset()
                food.spawn(snake.positions, obstacles.positions)
                obstacles.generate(snake.positions, food.position)
            if quit_button.handle_event(event):
                game_state = MENU
                
    # Обновление игрового состояния
    if game_state == PLAYING:
        # Обновление змейки
        if not snake.update():
            crash_sound.play()
            game_state = GAME_OVER
            
        # Обновление еды
        food.update()
        
        # Проверка съедания еды
        head = snake.get_head_position()
        if head == food.position:
            eat_sound.play()
            snake.grow()
            snake.score += 10 if food.special else 5
            
            # Если съедена особая еда
            if food.special:
                snake.activate_golden_food()
                snake.invincible = 60  # Неуязвимость на 1 секунду
                
            food.spawn(snake.positions, obstacles.positions)
            
            # Генерация препятствий каждые 30 очков
            if snake.score % 30 == 0:
                obstacles.generate(snake.positions, food.position)
                
        # Проверка столкновения с препятствиями
        if head in obstacles.positions and snake.invincible <= 0 and not snake.golden_food_active:
            crash_sound.play()
            game_state = GAME_OVER
            
    # Отрисовка
    # Фон
    screen.fill(BACKGROUND)
    
    # Сетка игрового поля
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 30), (x, HEIGHT), 1)
    for y in range(30, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y), 1)
        
    # Панель управления
    pygame.draw.rect(screen, PANEL_COLOR, (0, 0, WIDTH, 30))
    score_text = font_medium.render(f"Счет: {snake.score}", True, TEXT_COLOR)
    screen.blit(score_text, (20, 5))
    
    # Рисование игровых объектов
    obstacles.draw(screen)
    food.draw(screen)
    snake.draw(screen)
    
    # Отображение состояния игры
    if game_state == MENU:
        # Затемнение игрового поля
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        # Заголовок
        title = font_title.render("ЗМЕЙКА", True, SNAKE_COLOR)
        title_shadow = font_title.render("ЗМЕЙКА", True, (20, 80, 20))
        screen.blit(title_shadow, (WIDTH//2 - title.get_width()//2 + 3, 103))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        
        subtitle = font_medium.render("Особая версия с препятствиями и бонусами", True, (200, 200, 200))
        screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, 180))
        
        # Подсказки управления
        controls = font_small.render("Управление: Стрелки | Пауза: P | Меню: ESC", True, TEXT_COLOR)
        screen.blit(controls, (WIDTH//2 - controls.get_width()//2, 250))
        
        # Кнопки
        start_button.draw(screen)
        quit_button.draw(screen)
        
    elif game_state == GAME_OVER:
        # Затемнение игрового поля
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        # Сообщение о конце игры
        game_over = font_large.render("ИГРА ОКОНЧЕНА", True, (220, 20, 20))
        screen.blit(game_over, (WIDTH//2 - game_over.get_width()//2, HEIGHT//2 - 100))
        
        final_score = font_medium.render(f"Ваш счет: {snake.score}", True, TEXT_COLOR)
        screen.blit(final_score, (WIDTH//2 - final_score.get_width()//2, HEIGHT//2 - 30))
        
        # Кнопки
        restart_button.draw(screen)
        quit_button.draw(screen)
        
    elif game_state == PAUSED:
        # Затемнение игрового поля
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        
        # Сообщение о паузе
        paused = font_large.render("ПАУЗА", True, (255, 215, 0))
        screen.blit(paused, (WIDTH//2 - paused.get_width()//2, HEIGHT//2 - 50))
        
        # Подсказка
        hint = font_small.render("Нажмите P для продолжения", True, TEXT_COLOR)
        screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT//2 + 20))
    
    # Обновление экрана
    pygame.display.flip()
    
    # Управление скоростью игры
    clock.tick(snake.speed)
