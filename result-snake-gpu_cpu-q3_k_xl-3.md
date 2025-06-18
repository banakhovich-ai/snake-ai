```text
Prompt
- Tokens: 59
- Time: 22895.384 ms
- Speed: 2.6 t/s
Generation
- Tokens: 6259
- Time: 985364.553 ms
- Speed: 6.4 t/s
```

<think>
Мы создадим игру "Змейка" с использованием библиотеки Pygame.
 Игровое поле будет иметь сетку.
 Цветовая гамма: зеленый (змейка), красный (еда), черный (фон), серый (сетка).
 Меню: старт, пауза, рестарт.
 Анимация поедания еды: при поедании еды змейка будет увеличиваться и покажем небольшой эффект (например, вспышку).
 Изюминка: добавим два режима:
   - Обычный режим.
   - Режим с препятствиями (стенами) на поле.

 План:
 1. Инициализация Pygame, настройка экрана.
 2. Определение цветов.
 3. Класс Змейки:
    - Содержит список сегментов (координаты).
    - Направление движения.
    - Метод для движения: обновляем позиции сегментов.
    - Метод для роста: при съедании еды добавляем новый сегмент.
    - Метод для отрисовки.
    - Метод проверки столкновений с собой и границами (и препятствиями, если есть).
 4. Класс Еды:
    - Позиция.
    - Метод для генерации случайной позиции (не на змейке и не на препятствиях).
    - Метод отрисовки.
 5. Класс Игры:
    - Состояние: меню, игра, пауза, конец игры.
    - Счет.
    - Режимы: обычный, с препятствиями.
    - Генерация препятствий (в режиме препятствий).
 6. Основной игровой цикл:
    - Обработка событий (выход, нажатия клавиш).
    - Отрисовка в зависимости от состояния:
        - Меню: кнопки выбора режима.
        - Игра: змейка, еда, препятствия, сетка.
        - Пауза: затемнение и надпись.
        - Конец игры: вывод сообщения и кнопка рестарта.
    - Обновление объектов и проверка условий.

 7. Анимация поедания: при съедании еды, покажем анимацию (например, мигание еды и увеличение змейки с задержкой).

 8. Сетка: отрисовываем сетку на фоне.

 9. Дополнительно: звуковые эффекты.

 Однако, по условию, нам не нужно использовать слишком сложные вещи, поэтому звуки опционально.

 Реализуем по шагам.
</think>
# Игра "Змейка" на Python с PyGame

Вот полная реализация игры "Змейка" с сеткой, приятной цветовой гаммой, меню, анимацией поедания еды и интересной изюминкой - временными бонусами.

```python
import pygame
import sys
import random
import math
from enum import Enum

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
FPS = 10

# Цветовая палитра
BACKGROUND = (15, 20, 25)
GRID_COLOR = (30, 35, 40)
SNAKE_COLOR = (70, 200, 150)
SNAKE_HEAD_COLOR = (100, 230, 180)
FOOD_COLOR = (255, 80, 80)
TEXT_COLOR = (220, 220, 220)
BUTTON_COLOR = (80, 150, 200)
BUTTON_HOVER_COLOR = (100, 170, 220)
BONUS_COLOR = (255, 215, 0)
PARTICLE_COLORS = [
    (255, 100, 100),
    (255, 150, 100),
    (255, 200, 100),
    (255, 255, 100)
]

# Создание экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Змейка с Изюминкой")
clock = pygame.time.Clock()

# Шрифты
title_font = pygame.font.SysFont("Arial", 64, bold=True)
menu_font = pygame.font.SysFont("Arial", 36)
game_font = pygame.font.SysFont("Arial", 24)
small_font = pygame.font.SysFont("Arial", 18)

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class GameState(Enum):
    MENU = 0
    PLAYING = 1
    GAME_OVER = 2

class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.score = 0
        self.growth_pending = 0
        self.bonus_active = False
        self.bonus_timer = 0
        
    def get_head_position(self):
        return self.positions[0]
        
    def update(self):
        # Обновление направления
        self.direction = self.next_direction
        
        # Обновление позиции головы
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction.value
        new_head = (
            (head_x + dx) % GRID_WIDTH, 
            (head_y + dy) % GRID_HEIGHT
        )
        
        # Проверка столкновения с самой собой
        if new_head in self.positions[1:]:
            return False
            
        # Добавление новой головы
        self.positions.insert(0, new_head)
        
        # Удаление хвоста, если не нужно расти
        if self.growth_pending > 0:
            self.growth_pending -= 1
        else:
            self.positions.pop()
            
        # Обновление бонусного таймера
        if self.bonus_active:
            self.bonus_timer -= 1
            if self.bonus_timer <= 0:
                self.bonus_active = False
                
        return True
        
    def grow(self):
        self.growth_pending += 1
        self.length += 1
        
    def change_direction(self, direction):
        # Предотвращение разворота на 180 градусов
        if (direction == Direction.UP and self.direction != Direction.DOWN) or \
           (direction == Direction.DOWN and self.direction != Direction.UP) or \
           (direction == Direction.LEFT and self.direction != Direction.RIGHT) or \
           (direction == Direction.RIGHT and self.direction != Direction.LEFT):
            self.next_direction = direction
            
    def activate_bonus(self):
        self.bonus_active = True
        self.bonus_timer = 100  # 10 секунд при 10 FPS
        
    def draw(self, surface):
        for i, pos in enumerate(self.positions):
            color = SNAKE_HEAD_COLOR if i == 0 else SNAKE_COLOR
            rect = pygame.Rect(pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, (color[0]//2, color[1]//2, color[2]//2), rect, 1)
            
            # Рисуем глаза на голове
            if i == 0:
                eye_size = GRID_SIZE // 5
                eye_offset = GRID_SIZE // 3
                
                # Направление глаз
                if self.direction == Direction.RIGHT:
                    left_eye = (pos[0]*GRID_SIZE + GRID_SIZE - eye_offset, pos[1]*GRID_SIZE + eye_offset)
                    right_eye = (pos[0]*GRID_SIZE + GRID_SIZE - eye_offset, pos[1]*GRID_SIZE + GRID_SIZE - eye_offset)
                elif self.direction == Direction.LEFT:
                    left_eye = (pos[0]*GRID_SIZE + eye_offset, pos[1]*GRID_SIZE + eye_offset)
                    right_eye = (pos[0]*GRID_SIZE + eye_offset, pos[1]*GRID_SIZE + GRID_SIZE - eye_offset)
                elif self.direction == Direction.UP:
                    left_eye = (pos[0]*GRID_SIZE + eye_offset, pos[1]*GRID_SIZE + eye_offset)
                    right_eye = (pos[0]*GRID_SIZE + GRID_SIZE - eye_offset, pos[1]*GRID_SIZE + eye_offset)
                else:  # DOWN
                    left_eye = (pos[0]*GRID_SIZE + eye_offset, pos[1]*GRID_SIZE + GRID_SIZE - eye_offset)
                    right_eye = (pos[0]*GRID_SIZE + GRID_SIZE - eye_offset, pos[1]*GRID_SIZE + GRID_SIZE - eye_offset)
                
                pygame.draw.circle(surface, (0, 0, 0), left_eye, eye_size)
                pygame.draw.circle(surface, (0, 0, 0), right_eye, eye_size)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = FOOD_COLOR
        self.randomize_position()
        
    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), 
                        random.randint(0, GRID_HEIGHT - 1))
        
    def draw(self, surface):
        rect = pygame.Rect(
            self.position[0] * GRID_SIZE,
            self.position[1] * GRID_SIZE,
            GRID_SIZE, GRID_SIZE
        )
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, (180, 40, 40), rect, 1)
        
        # Рисуем сердцевину яблока
        center_x = self.position[0] * GRID_SIZE + GRID_SIZE // 2
        center_y = self.position[1] * GRID_SIZE + GRID_SIZE // 2
        radius = GRID_SIZE // 4
        pygame.draw.circle(surface, (255, 255, 255), (center_x, center_y), radius)

class Bonus:
    def __init__(self):
        self.position = (0, 0)
        self.color = BONUS_COLOR
        self.active = False
        self.timer = 0
        self.spawn_timer = 0
        
    def spawn(self):
        if not self.active and self.spawn_timer <= 0:
            self.position = (random.randint(0, GRID_WIDTH - 1), 
                            random.randint(0, GRID_HEIGHT - 1))
            self.active = True
            self.timer = 200  # 20 секунд при 10 FPS
            return True
        return False
        
    def update(self):
        if self.active:
            self.timer -= 1
            if self.timer <= 0:
                self.active = False
                self.spawn_timer = 300  # 30 секунд до следующего появления
        else:
            self.spawn_timer -= 1
            
    def draw(self, surface):
        if self.active:
            x, y = self.position
            rect = pygame.Rect(
                x * GRID_SIZE,
                y * GRID_SIZE,
                GRID_SIZE, GRID_SIZE
            )
            
            # Рисуем звезду
            center_x = x * GRID_SIZE + GRID_SIZE // 2
            center_y = y * GRID_SIZE + GRID_SIZE // 2
            radius = GRID_SIZE // 2 - 2
            
            points = []
            for i in range(5):
                # Внешние точки
                angle = math.pi/2 + i * 2*math.pi/5
                points.append((
                    center_x + radius * math.cos(angle),
                    center_y - radius * math.sin(angle)
                ))
                # Внутренние точки
                angle += math.pi/5
                points.append((
                    center_x + radius/2 * math.cos(angle),
                    center_y - radius/2 * math.sin(angle)
                ))
                
            pygame.draw.polygon(surface, self.color, points)
            
            # Анимация сияния
            pulse = math.sin(pygame.time.get_ticks() * 0.01) * 0.3 + 0.7
            pulse_color = (
                min(255, int(self.color[0] * pulse)),
                min(255, int(self.color[1] * pulse)),
                min(255, int(self.color[2] * pulse))
            )
            
            pygame.draw.polygon(surface, pulse_color, points)

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
        pygame.draw.circle(
            surface, 
            self.color, 
            (int(self.x), int(self.y)), 
            int(self.size)
        )
        
    def is_alive(self):
        return self.lifetime > 0

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.hovered = False
        
    def draw(self, surface):
        color = BUTTON_HOVER_COLOR if self.hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, (200, 230, 255), self.rect, 2, border_radius=10)
        
        text_surf = menu_font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        
    def check_click(self, pos):
        return self.rect.collidepoint(pos)

class Game:
    def __init__(self):
        self.state = GameState.MENU
        self.snake = Snake()
        self.food = Food()
        self.bonus = Bonus()
        self.particles = []
        self.play_button = Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2, 200, 50, "Играть")
        self.quit_button = Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 70, 200, 50, "Выход")
        self.restart_button = Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 50, 200, 50, "Играть снова")
        self.last_score = 0
        
    def reset(self):
        self.snake.reset()
        self.food.randomize_position()
        self.bonus.active = False
        self.bonus.timer = 0
        self.bonus.spawn_timer = 0
        self.particles = []
        
    def draw_grid(self, surface):
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(surface, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))
            
    def draw_menu(self, surface):
        surface.fill(BACKGROUND)
        
        # Заголовок
        title_text = title_font.render("ЗМЕЙКА", True, SNAKE_COLOR)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4))
        surface.blit(title_text, title_rect)
        
        # Подзаголовок
        subtitle = small_font.render("с временными бонусами", True, TEXT_COLOR)
        sub_rect = subtitle.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4 + 60))
        surface.blit(subtitle, sub_rect)
        
        # Кнопки
        self.play_button.draw(surface)
        self.quit_button.draw(surface)
        
        # Управление
        controls = [
            "Управление:",
            "Стрелки - Движение змейки",
            "Пробел - Пауза во время игры"
        ]
        
        for i, text in enumerate(controls):
            control_text = small_font.render(text, True, TEXT_COLOR)
            control_rect = control_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 100 + i*25))
            surface.blit(control_text, control_rect)
        
        # Декоративная змейка
        snake_length = 15
        snake_positions = [(SCREEN_WIDTH//2 - i*GRID_SIZE, SCREEN_HEIGHT//3 + 100) for i in range(snake_length)]
        for i, pos in enumerate(snake_positions):
            color = SNAKE_HEAD_COLOR if i == 0 else SNAKE_COLOR
            pygame.draw.rect(surface, color, pygame.Rect(pos[0], pos[1], GRID_SIZE, GRID_SIZE))
            
    def draw_game(self, surface):
        surface.fill(BACKGROUND)
        self.draw_grid(surface)
        
        # Рисуем еду
        self.food.draw(surface)
        
        # Рисуем бонус (если активен)
        if self.bonus.active:
            self.bonus.draw(surface)
            
        # Рисуем змейку
        self.snake.draw(surface)
        
        # Рисуем частицы
        for particle in self.particles:
            particle.draw(surface)
            
        # Рисуем интерфейс
        score_text = game_font.render(f"Счет: {self.snake.score}", True, TEXT_COLOR)
        surface.blit(score_text, (10, 10))
        
        length_text = game_font.render(f"Длина: {self.snake.length}", True, TEXT_COLOR)
        surface.blit(length_text, (10, 40))
        
        # Таймер бонуса
        if self.snake.bonus_active:
            bonus_text = game_font.render(f"Бонус: {self.snake.bonus_timer//10}с", True, BONUS_COLOR)
            surface.blit(bonus_text, (SCREEN_WIDTH - 120, 10))
            
    def draw_game_over(self, surface):
        self.draw_game(surface)
        
        # Затемнение экрана
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))
        
        # Текст "Игра окончена"
        game_over_text = title_font.render("Игра Окончена", True, (220, 80, 80))
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
        surface.blit(game_over_text, text_rect)
        
        # Счет
        score_text = menu_font.render(f"Ваш счет: {self.snake.score}", True, TEXT_COLOR)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 30))
        surface.blit(score_text, score_rect)
        
        # Лучший счет
        if self.snake.score > self.last_score:
            self.last_score = self.snake.score
            
        best_text = game_font.render(f"Лучший счет: {self.last_score}", True, TEXT_COLOR)
        best_rect = best_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 10))
        surface.blit(best_text, best_rect)
        
        # Кнопка перезапуска
        self.restart_button.draw(surface)
        
    def check_collisions(self):
        # Проверка столкновения с едой
        if self.snake.get_head_position() == self.food.position:
            # Создаем частицы для эффекта поедания
            head_x, head_y = self.snake.get_head_position()
            center_x = head_x * GRID_SIZE + GRID_SIZE // 2
            center_y = head_y * GRID_SIZE + GRID_SIZE // 2
            
            for _ in range(20):
                color = random.choice(PARTICLE_COLORS)
                self.particles.append(Particle(center_x, center_y, color))
            
            # Увеличиваем змейку
            self.snake.grow()
            self.snake.score += 2 if self.snake.bonus_active else 1
            
            # Перемещаем еду
            self.food.randomize_position()
            
            # С шансом 20% спавним бонус
            if random.random() < 0.2:
                self.bonus.spawn()
        
        # Проверка столкновения с бонусом
        if self.bonus.active and self.snake.get_head_position() == self.bonus.position:
            self.snake.activate_bonus()
            self.bonus.active = False
            self.snake.score += 5
            
    def update_particles(self):
        # Обновляем частицы
        self.particles = [p for p in self.particles if p.is_alive()]
        for particle in self.particles:
            particle.update()
            
    def run(self):
        paused = False
        
        while True:
            mouse_pos = pygame.mouse.get_pos()
            
            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if self.state == GameState.PLAYING and not paused:
                        if event.key == pygame.K_UP:
                            self.snake.change_direction(Direction.UP)
                        elif event.key == pygame.K_DOWN:
                            self.snake.change_direction(Direction.DOWN)
                        elif event.key == pygame.K_LEFT:
                            self.snake.change_direction(Direction.LEFT)
                        elif event.key == pygame.K_RIGHT:
                            self.snake.change_direction(Direction.RIGHT)
                        elif event.key == pygame.K_SPACE:
                            paused = not paused
                    elif event.key == pygame.K_SPACE and self.state == GameState.PLAYING:
                        paused = not paused
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.state == GameState.MENU:
                        if self.play_button.check_click(mouse_pos):
                            self.state = GameState.PLAYING
                            self.reset()
                        elif self.quit_button.check_click(mouse_pos):
                            pygame.quit()
                            sys.exit()
                            
                    elif self.state == GameState.GAME_OVER:
                        if self.restart_button.check_click(mouse_pos):
                            self.state = GameState.PLAYING
                            self.reset()
            
            # Обновление состояния кнопок
            if self.state == GameState.MENU:
                self.play_button.check_hover(mouse_pos)
                self.quit_button.check_hover(mouse_pos)
            elif self.state == GameState.GAME_OVER:
                self.restart_button.check_hover(mouse_pos)
            
            # Обновление игры
            if self.state == GameState.PLAYING and not paused:
                # Обновляем змейку
                if not self.snake.update():
                    self.state = GameState.GAME_OVER
                
                # Обновляем бонус
                self.bonus.update()
                
                # Проверяем столкновения
                self.check_collisions()
                
                # Обновляем частицы
                self.update_particles()
            
            # Отрисовка
            if self.state == GameState.MENU:
                self.draw_menu(screen)
            elif self.state == GameState.PLAYING:
                self.draw_game(screen)
                
                # Отрисовка паузы
                if paused:
                    pause_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                    pause_overlay.fill((0, 0, 0, 150))
                    screen.blit(pause_overlay, (0, 0))
                    
                    pause_text = menu_font.render("ПАУЗА", True, TEXT_COLOR)
                    pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
                    screen.blit(pause_text, pause_rect)
            elif self.state == GameState.GAME_OVER:
                self.draw_game_over(screen)
                
            pygame.display.update()
            clock.tick(FPS)

# Запуск игры
if __name__ == "__main__":
    game = Game()
    game.run()
```

## Особенности реализации:

1. **Приятная цветовая гамма**:
   - Тёмно-синий фон с серой сеткой
   - Зелено-бирюзовая змейка с выделенной головой
   - Красная еда с белой сердцевиной
   - Золотой бонус с анимацией пульсации

2. **Полноценное меню**:
   - Экран с заголовком и кнопками "Играть" и "Выход"
   - Подсказки по управлению

3. **Анимация поедания еды**:
   - Эффект частиц при съедании еды
   - Анимация пульсации бонуса

4. **Изюминка - временные бонусы**:
   - Случайное появление золотых звёзд
   - При съедании бонуса игрок получает +5 очков
   - На 10 секунд активируется бонусный режим (удвоение очков за еду)

5. **Дополнительные функции**:
   - Пауза во время игры (пробел)
   - Лучший счёт
   - Подсветка кнопок при наведении
   - Отскок от стен (телепортация)
   - Анимация глаз у змейки

6. **Графические элементы**:
   - Сетка игрового поля
   - Детализированное яблоко
   - Звёздчатый бонус
   - Частицы при поедании еды
   - Эффектные надписи

Для запуска игры просто выполните скрипт. Управление осуществляется стрелками, пауза - пробелом.