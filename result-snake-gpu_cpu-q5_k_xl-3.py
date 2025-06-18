import pygame
import sys
import random
import math
from pygame import mixer

# Инициализация Pygame
pygame.init()
mixer.init()

# Размеры экрана
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# Цвета
BACKGROUND = (15, 20, 30)
GRID_COLOR = (30, 35, 45)
SNAKE_COLOR = (0, 230, 150)
SNAKE_HEAD_COLOR = (0, 255, 180)
FOOD_COLOR = (255, 70, 90)
OBSTACLE_COLOR = (170, 100, 240)
TEXT_COLOR = (230, 230, 255)
MENU_BG = (20, 25, 40, 200)
BUTTON_COLOR = (80, 180, 250)
BUTTON_HOVER = (100, 200, 255)

# Создание экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Улучшенная Змейка")
clock = pygame.time.Clock()

# Загрузка звуков
try:
    eat_sound = mixer.Sound("eat.wav")  # Создайте файл eat.wav для звука или закомментируйте
    crash_sound = mixer.Sound("crash.wav")
except:
    # Заглушка, если звуки не найдены
    class DummySound:
        def play(self): pass
    eat_sound = DummySound()
    crash_sound = DummySound()

# Шрифты
font_large = pygame.font.SysFont("arial", 50, bold=True)
font_medium = pygame.font.SysFont("arial", 36)
font_small = pygame.font.SysFont("arial", 24)

class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        self.score = 0
        self.speed = 10
        self.grow_pending = 2  # Начальная длина
        
    def get_head_position(self):
        return self.positions[0]
    
    def update(self):
        head = self.get_head_position()
        dx, dy = self.direction
        new_x = (head[0] + dx) % GRID_WIDTH
        new_y = (head[1] + dy) % GRID_HEIGHT
        new_position = (new_x, new_y)
        
        # Проверка на столкновение с собой
        if new_position in self.positions[1:]:
            return False
        
        self.positions.insert(0, new_position)
        
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.positions.pop()
        
        return True
    
    def grow(self, amount=1):
        self.grow_pending += amount
        self.score += amount * 10
        self.length += amount
        
        # Увеличиваем скорость каждые 5 очков
        if self.score % 50 == 0 and self.speed < 20:
            self.speed += 1
    
    def change_direction(self, direction):
        # Предотвращение движения в противоположном направлении
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction
    
    def draw(self, surface):
        # Рисуем змейку с градиентом
        for i, pos in enumerate(self.positions):
            color_ratio = i / max(1, len(self.positions) - 1)
            r = int(SNAKE_COLOR[0] * (1 - color_ratio) + SNAKE_HEAD_COLOR[0] * color_ratio)
            g = int(SNAKE_COLOR[1] * (1 - color_ratio) + SNAKE_HEAD_COLOR[1] * color_ratio)
            b = int(SNAKE_COLOR[2] * (1 - color_ratio) + SNAKE_HEAD_COLOR[2] * color_ratio)
            
            rect = pygame.Rect(pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, (r, g, b), rect)
            pygame.draw.rect(surface, (r//1.2, g//1.2, b//1.2), rect, 2)
            
            # Рисуем глаза на голове
            if i == 0:
                eye_size = GRID_SIZE // 5
                # Определение направления для правильного размещения глаз
                dx, dy = self.direction
                offset_x = 3 if dx == 1 else -3 if dx == -1 else 0
                offset_y = 3 if dy == 1 else -3 if dy == -1 else 0
                
                # Левый глаз
                left_eye = pygame.Rect(
                    pos[0] * GRID_SIZE + GRID_SIZE//3 + offset_x, 
                    pos[1] * GRID_SIZE + GRID_SIZE//3 + offset_y,
                    eye_size, eye_size
                )
                # Правый глаз
                right_eye = pygame.Rect(
                    pos[0] * GRID_SIZE + 2*GRID_SIZE//3 + offset_x, 
                    pos[1] * GRID_SIZE + GRID_SIZE//3 + offset_y,
                    eye_size, eye_size
                )
                
                pygame.draw.ellipse(surface, (20, 20, 40), left_eye)
                pygame.draw.ellipse(surface, (20, 20, 40), right_eye)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = FOOD_COLOR
        self.randomize_position()
        self.animation_timer = 0
    
    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), 
                        random.randint(0, GRID_HEIGHT - 1))
    
    def draw(self, surface):
        self.animation_timer += 0.1
        size_factor = abs(math.sin(self.animation_timer)) * 0.2 + 0.8
        
        x = self.position[0] * GRID_SIZE + GRID_SIZE // 2
        y = self.position[1] * GRID_SIZE + GRID_SIZE // 2
        
        # Рисуем еду как яблоко
        radius = int(GRID_SIZE * 0.4 * size_factor)
        pygame.draw.circle(surface, self.color, (x, y), radius)
        
        # Рисуем блик
        pygame.draw.circle(surface, (255, 200, 200), 
                          (x - radius//3, y - radius//3), radius//3)

class Obstacle:
    def __init__(self):
        self.positions = []
        self.generate_obstacles()
    
    def generate_obstacles(self):
        # Генерируем случайные препятствия
        self.positions = []
        num_obstacles = random.randint(3, 6)
        
        for _ in range(num_obstacles):
            # Выбираем случайную позицию
            x, y = random.randint(1, GRID_WIDTH - 2), random.randint(1, GRID_HEIGHT - 2)
            
            # Выбираем случайную форму (вертикальная или горизонтальная линия)
            if random.random() > 0.5:
                # Горизонтальная линия (длина 3-6 клеток)
                length = random.randint(3, 6)
                for i in range(length):
                    if 0 <= x + i < GRID_WIDTH:
                        self.positions.append((x + i, y))
            else:
                # Вертикальная линия
                length = random.randint(3, 6)
                for i in range(length):
                    if 0 <= y + i < GRID_HEIGHT:
                        self.positions.append((x, y + i))
    
    def draw(self, surface):
        for pos in self.positions:
            rect = pygame.Rect(pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, OBSTACLE_COLOR, rect)
            
            # Добавляем текстуру
            pygame.draw.line(surface, (140, 70, 220), 
                            (rect.left, rect.top), 
                            (rect.right, rect.bottom), 2)
            pygame.draw.line(surface, (140, 70, 220), 
                            (rect.right, rect.top), 
                            (rect.left, rect.bottom), 2)

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.obstacles = Obstacle()
        self.game_state = "menu"  # menu, playing, game_over
        self.particles = []
    
    def check_collision(self):
        # Проверка столкновения с едой
        if self.snake.get_head_position() == self.food.position:
            self.snake.grow(2)  # Змейка растет на 2 сегмента
            self.food.randomize_position()
            eat_sound.play()
            
            # Проверка, чтобы еда не появилась на змейке или препятствии
            while (self.food.position in self.snake.positions or 
                   self.food.position in self.obstacles.positions):
                self.food.randomize_position()
            
            # Создаем эффект частиц
            self.create_particles(self.food.position)
            
            # Каждые 50 очков меняем препятствия
            if self.snake.score % 50 == 0:
                self.obstacles.generate_obstacles()
        
        # Проверка столкновения с препятствиями
        if self.snake.get_head_position() in self.obstacles.positions:
            crash_sound.play()
            self.game_state = "game_over"
    
    def create_particles(self, position):
        # Создание частиц для эффекта съедания еды
        for _ in range(15):
            particle = {
                'pos': (position[0] * GRID_SIZE + GRID_SIZE//2, 
                       position[1] * GRID_SIZE + GRID_SIZE//2),
                'vel': (random.uniform(-2, 2), random.uniform(-2, 2)),
                'color': (random.randint(200, 255), random.randint(70, 120), random.randint(80, 150)),
                'size': random.randint(3, 8),
                'life': random.randint(20, 40)
            }
            self.particles.append(particle)
    
    def update_particles(self):
        for particle in self.particles[:]:
            particle['pos'] = (particle['pos'][0] + particle['vel'][0], 
                             particle['pos'][1] + particle['vel'][1])
            particle['life'] -= 1
            
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def draw_particles(self, surface):
        for particle in self.particles:
            alpha = min(255, particle['life'] * 6)
            color = (*particle['color'], alpha)
            pygame.draw.circle(
                surface, 
                color,
                (int(particle['pos'][0]), int(particle['pos'][1])),
                particle['size']
            )
    
    def draw_grid(self, surface):
        for x in range(0, WIDTH, GRID_SIZE):
            pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, HEIGHT), 1)
        for y in range(0, HEIGHT, GRID_SIZE):
            pygame.draw.line(surface, GRID_COLOR, (0, y), (WIDTH, y), 1)
    
    def draw_menu(self, surface):
        # Полупрозрачный фон меню
        menu_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        menu_surface.fill(MENU_BG)
        surface.blit(menu_surface, (0, 0))
        
        # Заголовок
        title = font_large.render("ЗМЕЙКА", True, TEXT_COLOR)
        surface.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        
        # Кнопки
        mouse_pos = pygame.mouse.get_pos()
        
        # Кнопка "Начать игру"
        start_button = pygame.Rect(WIDTH//2 - 100, 250, 200, 50)
        start_color = BUTTON_HOVER if start_button.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(surface, start_color, start_button, border_radius=10)
        pygame.draw.rect(surface, TEXT_COLOR, start_button, 3, border_radius=10)
        start_text = font_small.render("Начать игру", True, TEXT_COLOR)
        surface.blit(start_text, (WIDTH//2 - start_text.get_width()//2, 265))
        
        # Кнопка "Выход"
        exit_button = pygame.Rect(WIDTH//2 - 100, 320, 200, 50)
        exit_color = BUTTON_HOVER if exit_button.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(surface, exit_color, exit_button, border_radius=10)
        pygame.draw.rect(surface, TEXT_COLOR, exit_button, 3, border_radius=10)
        exit_text = font_small.render("Выход", True, TEXT_COLOR)
        surface.blit(exit_text, (WIDTH//2 - exit_text.get_width()//2, 335))
        
        # Управление
        controls = [
            "Управление:",
            "Стрелки - Движение",
            "Пробел - Пауза",
            "",
            "Особенности:",
            "- Избегай препятствий",
            "- Телепортация через границы",
            "- Частицы при поедании"
        ]
        
        for i, line in enumerate(controls):
            text = font_small.render(line, True, TEXT_COLOR)
            surface.blit(text, (WIDTH//2 - text.get_width()//2, 400 + i * 30))
        
        return start_button, exit_button
    
    def draw_game_over(self, surface):
        # Полупрозрачный фон
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))
        
        # Текст
        game_over = font_large.render("ИГРА ОКОНЧЕНА", True, (255, 100, 100))
        surface.blit(game_over, (WIDTH//2 - game_over.get_width()//2, HEIGHT//2 - 100))
        
        score_text = font_medium.render(f"Счет: {self.snake.score}", True, TEXT_COLOR)
        surface.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
        
        restart_text = font_small.render("Нажмите R для перезапуска", True, TEXT_COLOR)
        surface.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 80))
        
        menu_text = font_small.render("Нажмите M для возврата в меню", True, TEXT_COLOR)
        surface.blit(menu_text, (WIDTH//2 - menu_text.get_width()//2, HEIGHT//2 + 120))
    
    def draw(self, surface):
        # Отрисовка фона
        surface.fill(BACKGROUND)
        
        # Отрисовка сетки
        self.draw_grid(surface)
        
        # Отрисовка препятствий
        self.obstacles.draw(surface)
        
        # Отрисовка еды
        self.food.draw(surface)
        
        # Отрисовка змейки
        self.snake.draw(surface)
        
        # Отрисовка частиц
        self.draw_particles(surface)
        
        # Отрисовка счета
        score_text = font_medium.render(f"Счет: {self.snake.score}", True, TEXT_COLOR)
        surface.blit(score_text, (10, 10))
        
        # Отрисовка скорости
        speed_text = font_small.render(f"Скорость: {self.snake.speed}", True, TEXT_COLOR)
        surface.blit(speed_text, (WIDTH - 150, 10))
        
        # Отрисовка длины
        length_text = font_small.render(f"Длина: {self.snake.length}", True, TEXT_COLOR)
        surface.blit(length_text, (WIDTH - 150, 40))
        
        # Отрисовка меню или экрана окончания игры
        if self.game_state == "menu":
            return self.draw_menu(surface)
        elif self.game_state == "game_over":
            self.draw_game_over(surface)
        
        return None, None
    
    def reset(self):
        self.snake.reset()
        self.food.randomize_position()
        self.obstacles.generate_obstacles()
        self.particles = []

# Основная функция игры
def main():
    game = Game()
    
    # Переменные для отслеживания времени
    last_move_time = pygame.time.get_ticks()
    
    # Основной игровой цикл
    while True:
        current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                # Управление в игре
                if game.game_state == "playing":
                    if event.key == pygame.K_UP:
                        game.snake.change_direction((0, -1))
                    elif event.key == pygame.K_DOWN:
                        game.snake.change_direction((0, 1))
                    elif event.key == pygame.K_LEFT:
                        game.snake.change_direction((-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        game.snake.change_direction((1, 0))
                    elif event.key == pygame.K_SPACE:
                        game.game_state = "menu"
                
                # Перезапуск игры
                elif game.game_state == "game_over":
                    if event.key == pygame.K_r:
                        game.reset()
                        game.game_state = "playing"
                    elif event.key == pygame.K_m:
                        game.reset()
                        game.game_state = "menu"
            
            # Обработка кликов в меню
            if event.type == pygame.MOUSEBUTTONDOWN and game.game_state == "menu":
                start_button, exit_button = game.draw(screen)
                if start_button.collidepoint(event.pos):
                    game.reset()
                    game.game_state = "playing"
                elif exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        
        # Обновление частиц
        game.update_particles()
        
        # Обновление игры
        if game.game_state == "playing":
            # Движение змейки с учетом скорости
            if current_time - last_move_time > 1000 / game.snake.speed:
                if not game.snake.update():
                    crash_sound.play()
                    game.game_state = "game_over"
                game.check_collision()
                last_move_time = current_time
        
        # Отрисовка
        start_button, exit_button = game.draw(screen)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
