import pygame
import sys
import random
import math
from pygame import gfxdraw

# Инициализация Pygame
pygame.init()
pygame.display.set_caption("Змейка")

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = (SCREEN_HEIGHT - 60) // GRID_SIZE
FPS = 10

# Цвета
BACKGROUND = (25, 25, 35)
GRID_COLOR = (40, 40, 55)
SNAKE_COLOR = (65, 195, 150)
SNAKE_HEAD_COLOR = (85, 230, 180)
FOOD_COLOR = (240, 100, 100)
TEXT_COLOR = (220, 220, 240)
UI_BACKGROUND = (35, 35, 45)
PORTAL_COLOR = (150, 100, 220)
SPEED_BOOST_COLOR = (100, 200, 255)
MENU_COLOR = (30, 30, 45)
BUTTON_COLOR = (70, 150, 200)
BUTTON_HOVER_COLOR = (90, 170, 220)

# Создание экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Шрифты
title_font = pygame.font.SysFont("Arial", 48, bold=True)
font = pygame.font.SysFont("Arial", 24)
small_font = pygame.font.SysFont("Arial", 20)

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(3, 8)
        self.speed_x = random.uniform(-2, 2)
        self.speed_y = random.uniform(-2, 2)
        self.life = random.randint(20, 40)
        
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.life -= 1
        self.size = max(0, self.size - 0.1)
        
    def draw(self, surface):
        alpha = min(255, self.life * 6)
        color = (self.color[0], self.color[1], self.color[2], alpha)
        gfxdraw.filled_circle(surface, int(self.x), int(self.y), int(self.size), color)

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.hovered = False
        
    def draw(self, surface):
        color = BUTTON_HOVER_COLOR if self.hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, (180, 220, 255), self.rect, 2, border_radius=10)
        
        text_surf = font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        
    def check_click(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.score = 0
        self.grow_to = 3
        self.speed_boost = 0
        
    def get_head_position(self):
        return self.positions[0]
    
    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        self.direction = point
    
    def move(self):
        head = self.get_head_position()
        x, y = self.direction
        new_x = (head[0] + x) % GRID_WIDTH
        new_y = (head[1] + y) % GRID_HEIGHT
        
        # Проверка столкновения с собой
        if (new_x, new_y) in self.positions[1:]:
            return False
        
        self.positions.insert(0, (new_x, new_y))
        
        if len(self.positions) > self.grow_to:
            self.positions.pop()
            
        if self.speed_boost > 0:
            self.speed_boost -= 1
            
        return True
    
    def grow(self):
        self.grow_to += 1
        self.score += 10
        
    def draw(self, surface):
        for i, pos in enumerate(self.positions):
            rect = pygame.Rect(
                pos[0] * GRID_SIZE, 
                pos[1] * GRID_SIZE, 
                GRID_SIZE, 
                GRID_SIZE
            )
            
            # Рисуем голову и тело разными цветами
            if i == 0:
                pygame.draw.rect(surface, SNAKE_HEAD_COLOR, rect, border_radius=8)
                # Глаза
                eye_size = GRID_SIZE // 6
                offset = GRID_SIZE // 4
                direction_offset = {
                    (1, 0): (offset*1.5, offset),
                    (-1, 0): (-offset/2, offset),
                    (0, 1): (offset, offset*1.5),
                    (0, -1): (offset, -offset/2)
                }
                
                dx, dy = direction_offset[self.direction]
                pygame.draw.circle(
                    surface, (30, 30, 50), 
                    (int(rect.centerx + dx), int(rect.centery + dy)), 
                    eye_size
                )
            else:
                # Градиент для тела
                color_factor = min(1.0, i / (self.length * 0.5))
                r = int(SNAKE_COLOR[0] * color_factor)
                g = int(SNAKE_COLOR[1] * color_factor)
                b = int(SNAKE_COLOR[2] * color_factor)
                pygame.draw.rect(surface, (r, g, b), rect, border_radius=6)
                
            # Тонкая обводка для каждого сегмента
            pygame.draw.rect(surface, (40, 80, 70), rect, 1, border_radius=6)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = FOOD_COLOR
        self.particles = []
        self.spawn()
        
    def spawn(self):
        self.position = (
            random.randint(0, GRID_WIDTH - 1),
            random.randint(0, GRID_HEIGHT - 1)
        )
        self.particles = []
        
    def create_particles(self):
        for _ in range(15):
            x = self.position[0] * GRID_SIZE + GRID_SIZE // 2
            y = self.position[1] * GRID_SIZE + GRID_SIZE // 2
            self.particles.append(Particle(x, y, FOOD_COLOR))
            
    def update_particles(self):
        for particle in self.particles[:]:
            particle.update()
            if particle.life <= 0:
                self.particles.remove(particle)
                
    def draw(self, surface):
        # Анимированная еда
        x, y = self.position
        rect = pygame.Rect(
            x * GRID_SIZE + 2, 
            y * GRID_SIZE + 2, 
            GRID_SIZE - 4, 
            GRID_SIZE - 4
        )
        
        # Пульсирующий эффект
        pulse = abs(math.sin(pygame.time.get_ticks() * 0.005)) * 0.3 + 0.7
        r = int(self.color[0] * pulse)
        g = int(self.color[1] * pulse)
        b = int(self.color[2] * pulse)
        
        pygame.draw.rect(surface, (r, g, b), rect, border_radius=10)
        
        # Рисуем частицы
        for particle in self.particles:
            particle.draw(surface)

class Portal:
    def __init__(self):
        self.pair = []
        self.spawn()
        
    def spawn(self):
        # Создаем два портала
        self.pair = [
            (random.randint(1, GRID_WIDTH - 2), random.randint(1, GRID_HEIGHT - 2)),
            (random.randint(1, GRID_WIDTH - 2), random.randint(1, GRID_HEIGHT - 2))
        ]
        
    def draw(self, surface):
        for i, pos in enumerate(self.pair):
            x, y = pos
            center = (
                x * GRID_SIZE + GRID_SIZE // 2,
                y * GRID_SIZE + GRID_SIZE // 2
            )
            
            # Внешний круг
            pygame.draw.circle(surface, PORTAL_COLOR, center, GRID_SIZE // 2)
            # Внутренний круг
            pygame.draw.circle(surface, (90, 60, 150), center, GRID_SIZE // 3)
            
            # Анимация вращения
            angle = pygame.time.get_ticks() * 0.01
            radius = GRID_SIZE // 2 - 2
            points = []
            for i in range(6):
                px = center[0] + math.cos(angle + i * math.pi/3) * radius
                py = center[1] + math.sin(angle + i * math.pi/3) * radius
                points.append((px, py))
                
            pygame.draw.polygon(surface, (200, 180, 255), points)

class SpeedBoost:
    def __init__(self):
        self.position = (0, 0)
        self.active = False
        self.timer = 0
        self.spawn()
        
    def spawn(self):
        if not self.active:
            self.position = (
                random.randint(1, GRID_WIDTH - 2),
                random.randint(1, GRID_HEIGHT - 2)
            )
            self.active = True
            self.timer = 300  # 5 секунд при 60 FPS
            
    def update(self):
        if self.active:
            self.timer -= 1
            if self.timer <= 0:
                self.active = False
                
    def draw(self, surface):
        if self.active:
            x, y = self.position
            center = (
                x * GRID_SIZE + GRID_SIZE // 2,
                y * GRID_SIZE + GRID_SIZE // 2
            )
            
            # Вращающаяся звезда
            size = GRID_SIZE // 2
            angle = pygame.time.get_ticks() * 0.01
            points = []
            for i in range(5):
                # Внешняя точка
                px = center[0] + math.cos(angle + i * 2*math.pi/5) * size
                py = center[1] + math.sin(angle + i * 2*math.pi/5) * size
                points.append((px, py))
                
                # Внутренняя точка
                px = center[0] + math.cos(angle + (i+0.5) * 2*math.pi/5) * size/2
                py = center[1] + math.sin(angle + (i+0.5) * 2*math.pi/5) * size/2
                points.append((px, py))
                
            pygame.draw.polygon(surface, SPEED_BOOST_COLOR, points)

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.portal = Portal()
        self.speed_boost = SpeedBoost()
        self.level = 1
        self.game_state = "menu"  # menu, playing, paused, game_over
        self.difficulty = "medium"  # easy, medium, hard
        self.init_menu()
        
    def init_menu(self):
        # Создаем кнопки меню
        button_width = 200
        button_height = 50
        center_x = SCREEN_WIDTH // 2
        self.menu_buttons = [
            Button(center_x - button_width//2, 200, button_width, button_height, "Начать игру"),
            Button(center_x - button_width//2, 270, button_width, button_height, "Сложность: Средняя"),
            Button(center_x - button_width//2, 340, button_width, button_height, "Выход")
        ]
        
    def handle_menu_events(self, event):
        mouse_pos = pygame.mouse.get_pos()
        
        for button in self.menu_buttons:
            button.check_hover(mouse_pos)
            
            if button.check_click(mouse_pos, event):
                if button.text == "Начать игру":
                    self.start_game()
                elif button.text.startswith("Сложность"):
                    self.toggle_difficulty()
                elif button.text == "Выход":
                    pygame.quit()
                    sys.exit()
                    
    def toggle_difficulty(self):
        difficulties = ["easy", "medium", "hard"]
        current_idx = difficulties.index(self.difficulty)
        next_idx = (current_idx + 1) % len(difficulties)
        self.difficulty = difficulties[next_idx]
        
        # Обновляем текст кнопки
        difficulty_names = {
            "easy": "Легкая",
            "medium": "Средняя",
            "hard": "Тяжелая"
        }
        self.menu_buttons[1].text = f"Сложность: {difficulty_names[self.difficulty]}"
        
    def start_game(self):
        self.game_state = "playing"
        self.snake.reset()
        self.food.spawn()
        self.portal.spawn()
        self.speed_boost.spawn()
        self.level = 1
        
        # Настройка сложности
        global FPS
        if self.difficulty == "easy":
            FPS = 8
        elif self.difficulty == "medium":
            FPS = 10
        else:  # hard
            FPS = 14
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if self.game_state == "menu":
                self.handle_menu_events(event)
                
            elif self.game_state == "playing" or self.game_state == "paused":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.snake.turn((0, -1))
                    elif event.key == pygame.K_DOWN:
                        self.snake.turn((0, 1))
                    elif event.key == pygame.K_LEFT:
                        self.snake.turn((-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        self.snake.turn((1, 0))
                    elif event.key == pygame.K_SPACE:
                        self.game_state = "playing" if self.game_state == "paused" else "paused"
                    elif event.key == pygame.K_ESCAPE:
                        self.game_state = "menu"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Левая кнопка мыши
                        mouse_pos = pygame.mouse.get_pos()
                        if self.pause_button.collidepoint(mouse_pos):
                            self.game_state = "paused" if self.game_state == "playing" else "playing"
            elif self.game_state == "game_over":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.start_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.game_state = "menu"
    
    def update(self):
        if self.game_state == "playing":
            # Движение змеи
            if not self.snake.move():
                self.game_state = "game_over"
                return
            
            head_pos = self.snake.get_head_position()
            
            # Проверка съедания еды
            if head_pos == self.food.position:
                self.food.create_particles()
                self.snake.grow()
                self.food.spawn()
                
                # Увеличение уровня каждые 5 съеденных еды
                if self.snake.score % 50 == 0:
                    self.level += 1
                    global FPS
                    FPS = min(20, FPS + 1)  # Ограничим максимальную скорость
            
            # Проверка попадания на портал
            for portal in self.portal.pair:
                if head_pos == portal:
                    # Телепортируем в другой портал
                    other_portal = self.portal.pair[0] if portal == self.portal.pair[1] else self.portal.pair[1]
                    self.snake.positions[0] = other_portal
                    # Перемещаем порталы
                    self.portal.spawn()
                    break
                    
            # Проверка взятия бонуса скорости
            if self.speed_boost.active and head_pos == self.speed_boost.position:
                self.snake.speed_boost = 60  # 1 секунда ускорения
                self.speed_boost.active = False
                
            # Обновление объектов
            self.food.update_particles()
            self.speed_boost.update()
            
            # Спавн бонуса скорости, если он не активен
            if not self.speed_boost.active and random.random() < 0.005:
                self.speed_boost.spawn()
    
    def draw(self):
        # Отрисовка фона
        screen.fill(BACKGROUND)
        
        # Отрисовка игровой области
        game_area = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT - 60)
        pygame.draw.rect(screen, UI_BACKGROUND, game_area)
        
        # Отрисовка сетки
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT - 60), 1)
        for y in range(0, SCREEN_HEIGHT - 60, GRID_SIZE):
            pygame.draw.line(screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y), 1)
        
        if self.game_state == "menu":
            self.draw_menu()
        elif self.game_state in ["playing", "paused", "game_over"]:
            # Отрисовка объектов игры
            self.food.draw(screen)
            self.portal.draw(screen)
            if self.speed_boost.active:
                self.speed_boost.draw(screen)
            self.snake.draw(screen)
            
            # Отрисовка UI
            self.draw_ui()
            
            # Сообщение о паузе
            if self.game_state == "paused":
                pause_text = font.render("ПАУЗА - Нажмите SPACE для продолжения", True, TEXT_COLOR)
                text_rect = pause_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 30))
                pygame.draw.rect(screen, (0, 0, 0, 180), text_rect.inflate(20, 20))
                screen.blit(pause_text, text_rect)
            
            # Сообщение о конце игры
            if self.game_state == "game_over":
                game_over_text = title_font.render("ИГРА ОКОНЧЕНА!", True, (240, 100, 100))
                score_text = font.render(f"Счет: {self.snake.score}", True, TEXT_COLOR)
                restart_text = font.render("Нажмите ENTER для рестарта или ESC для меню", True, TEXT_COLOR)
                
                # Затемнение экрана
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                overlay.set_alpha(180)
                overlay.fill((0, 0, 0))
                screen.blit(overlay, (0, 0))
                
                screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, 150))
                screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 220))
                screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, 270))
    
    def draw_menu(self):
        # Заголовок
        title = title_font.render("ЗМЕЙКА", True, (100, 220, 150))
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 80))
        
        # Описание
        desc = font.render("Используйте стрелки для управления, SPACE для паузы", True, TEXT_COLOR)
        screen.blit(desc, (SCREEN_WIDTH//2 - desc.get_width()//2, 140))
        
        # Кнопки
        for button in self.menu_buttons:
            button.draw(screen)
            
        # Подсказка
        hint = small_font.render("Изюминка: порталы, бонусы скорости, уровни сложности", True, (150, 150, 170))
        screen.blit(hint, (SCREEN_WIDTH//2 - hint.get_width()//2, 420))
        
        # Автор
        author = small_font.render("Сделано с использованием PyGame", True, (120, 120, 140))
        screen.blit(author, (SCREEN_WIDTH//2 - author.get_width()//2, 500))
    
    def draw_ui(self):
        # Панель внизу экрана
        ui_panel = pygame.Rect(0, SCREEN_HEIGHT - 60, SCREEN_WIDTH, 60)
        pygame.draw.rect(screen, UI_BACKGROUND, ui_panel)
        pygame.draw.line(screen, (70, 70, 90), (0, SCREEN_HEIGHT - 60), (SCREEN_WIDTH, SCREEN_HEIGHT - 60), 2)
        
        # Счет
        score_text = font.render(f"Счет: {self.snake.score}", True, TEXT_COLOR)
        screen.blit(score_text, (20, SCREEN_HEIGHT - 45))
        
        # Длина змеи
        length_text = font.render(f"Длина: {self.snake.grow_to}", True, TEXT_COLOR)
        screen.blit(length_text, (200, SCREEN_HEIGHT - 45))
        
        # Уровень
        level_text = font.render(f"Уровень: {self.level}", True, TEXT_COLOR)
        screen.blit(level_text, (380, SCREEN_HEIGHT - 45))
        
        # Кнопка паузы
        self.pause_button = pygame.Rect(SCREEN_WIDTH - 120, SCREEN_HEIGHT - 45, 100, 30)
        pygame.draw.rect(screen, BUTTON_COLOR, self.pause_button, border_radius=6)
        pause_text = font.render("Пауза", True, TEXT_COLOR)
        screen.blit(pause_text, (self.pause_button.centerx - pause_text.get_width()//2, 
                                self.pause_button.centery - pause_text.get_height()//2))
        
        # Бонус скорости (если активен)
        if self.snake.speed_boost > 0:
            boost_text = font.render("Ускорение!", True, (100, 200, 255))
            screen.blit(boost_text, (SCREEN_WIDTH//2 - boost_text.get_width()//2, SCREEN_HEIGHT - 45))

# Создание и запуск игры
game = Game()

while True:
    game.handle_events()
    game.update()
    game.draw()
    
    pygame.display.flip()
    clock.tick(6)  # Фиксированное обновление для плавной анимации
