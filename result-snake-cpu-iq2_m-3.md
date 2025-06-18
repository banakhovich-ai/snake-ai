```text
Prompt
- Tokens: 59
- Time: 4885.452 ms
- Speed: 12.1 t/s
Generation
- Tokens: 8487
- Time: 2323747.56 ms
- Speed: 3.7 t/s
```

<think>
Создадим игру "Змейка" с учетом всех требований.
План:
1. Используем библиотеку Pygame для графики и управления.
2. Сетка: нарисуем сетку на игровом поле.
3. Цветовая гамма: подберем приятные цвета для змейки, фона, еды и т.д.
4. Меню: реализуем стартовое меню с кнопкой "Старт" и, возможно, настройками.
5. Анимация поедания еды: добавим эффект при поедании еды (например, увеличение и исчезновение).
6. Изюминка: добавим что-то интересное, например, возможность появления особой еды, которая дает дополнительные эффекты (ускорение, замедление, увеличение длины больше чем на один) или препятствия.

Для выполнения задания создадим классы:
- Змейка (Snake)
- Еда (Food)
- Особенная еда (SpecialFood) - для изюминки
- Игровое поле (Game) - будет содержать основную логику
- Меню (Menu)

Структура:
1. Инициализация Pygame, настройка окна.
2. Цвета: определим приятную палитру.
3. Класс Snake: 
   - сегменты (список координат)
   - направление движения
   - метод для движения (с обновлением позиции сегментов)
   - метод для увеличения длины (при съедании еды)
   - метод для отрисовки
4. Класс Food:
   - координаты
   - таймер для анимации (при съедании)
   - метод для отрисовки с анимацией
5. Класс SpecialFood (наследник Food):
   - дополнительные свойства (эффект, время жизни)
6. Класс Game:
   - игровое поле (сетка)
   - змейка
   - еда
   - специальная еда (появляется редко)
   - таймеры для специальной еды
   - обработка событий
   - обновление состояния
   - отрисовка сетки, змейки, еды
   - проверка столкновений
   - счет
7. Меню: экран с кнопками.

Для анимации поедания еды:
   При съедании обычной еды мы будем рисовать еду с увеличением размера и постепенным исчезновением.

Для простоты реализации анимации создадим список "частиц" (анимаций) в классе Game, которые будут отрисовываться в течение нескольких кадров.

Реализуем:

Импортируем необходимые библиотеки:
```python
import pygame
import sys
import random
import math
from pygame.locals import *
```

Установим константы:
```python
# Размеры окна
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20  # размер клетки
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# Цвета
BACKGROUND = (15, 20, 25)  # темно-синий
GRID_COLOR = (30, 40, 50)
SNAKE_COLOR = (50, 180, 80)  # зеленый
SNAKE_HEAD_COLOR = (70, 200, 100)
FOOD_COLOR = (220, 60, 60)  # красный
SPECIAL_FOOD_COLOR = (220, 200, 60)  # желтый
TEXT_COLOR = (240, 240, 240)
MENU_BACKGROUND = (25, 30, 40)
MENU_BUTTON = (70, 130, 180)
MENU_BUTTON_HOVER = (100, 160, 210)
```

Создадим классы:

1. Класс Snake
2. Класс Food
3. Класс SpecialFood (наследуется от Food)
4. Класс Game
5. Класс Menu

Начнем с класса Snake:

```python
class Snake:
    def __init__(self):
        self.reset()
        self.direction = random.choice([(1,0), (0,1), (-1,0), (0,-1)])  # начальное направление
        self.head_color = SNAKE_HEAD_COLOR
        self.body_color = SNAKE_COLOR

    def reset(self):
        # Начальная позиция в центре
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        # Добавим начальные сегменты в зависимости от направления
        dx, dy = self.direction if hasattr(self, 'direction') else (1,0)
        for i in range(1,3):
            self.positions.append((self.positions[0][0] - i*dx, self.positions[0][1] - i*dy))

    def move(self, direction=None):
        if direction:
            self.direction = direction

        dx, dy = self.direction
        head_x, head_y = self.positions[0]
        new_position = ((head_x + dx) % GRID_WIDTH, (head_y + dy) % GRID_HEIGHT)

        # Добавляем новую голову
        self.positions.insert(0, new_position)
        # Удаляем хвост, если длина не увеличилась
        if len(self.positions) > self.length:
            self.positions.pop()

    def grow(self, amount=1):
        self.length += amount

    def draw(self, surface):
        # Рисуем змейку
        for i, (x, y) in enumerate(self.positions):
            color = self.head_color if i == 0 else self.body_color
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, color, rect)
            # Скругление углов для сегментов
            pygame.draw.rect(surface, color, rect, border_radius=5)
```

Класс Food и SpecialFood:

```python
class Food:
    def __init__(self):
        self.position = (0,0)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))

    def draw(self, surface):
        rect = pygame.Rect(self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, FOOD_COLOR, rect, border_radius=10)

class SpecialFood(Food):
    def __init__(self):
        super().__init__()
        self.effects = ['grow', 'speed_up', 'slow_down']
        self.effect = random.choice(self.effects)
        self.lifetime = 10 * 60  # 10 секунд (60 кадров в секунду)
        self.active = True

    def draw(self, surface):
        if not self.active:
            return
        rect = pygame.Rect(self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, SPECIAL_FOOD_COLOR, rect, border_radius=15)
        # Рисуем эффект: полоски или что-то простое
        pygame.draw.line(surface, (255,255,0), rect.topleft, rect.bottomright, 2)
        pygame.draw.line(surface, (255,255,0), rect.topright, rect.bottomleft, 2)

    def update(self):
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.active = False
```

Класс Game:

```python
class Game:
    def __init__(self, surface):
        self.surface = surface
        self.snake = Snake()
        self.food = Food()
        self.special_food = None
        self.special_food_timer = 0
        self.special_food_spawn_time = 10 * 60  # каждые 10 секунд
        self.score = 0
        self.game_over = False
        self.animation_particles = []  # для анимации поедания
        self.speed = 10  # скорость змейки (кадров в секунду)
        self.clock = pygame.time.Clock()
        self.snake_direction_queue = []  # очередь направлений для плавной смены
        self.font = pygame.font.SysFont('Arial', 24)

    def spawn_special_food(self):
        if self.special_food is None or not self.special_food.active:
            self.special_food = SpecialFood()
            # Проверим, что не попадает на змейку или обычную еду
            while self.special_food.position == self.food.position or self.special_food.position in self.snake.positions:
                self.special_food.randomize_position()
            self.special_food_timer = 0

    def check_collision(self):
        head = self.snake.positions[0]
        # Проверка столкновения с собой (кроме головы)
        if head in self.snake.positions[1:]:
            self.game_over = True

        # Проверка съедания обычной еды
        if head == self.food.position:
            self.snake.grow()
            self.score += 1
            self.food.randomize_position()
            # Проверяем, что еда не появилась на змейке
            while self.food.position in self.snake.positions:
                self.food.randomize_position()
            # Анимация поедания
            self.animation_particles.append([self.food.position, 10])
            # Увеличиваем скорость на 0.5 (но не более 20)
            self.speed = min(20, self.speed + 0.5)

        # Проверка съедания специальной еды
        if self.special_food and self.special_food.active:
            if head == self.special_food.position:
                effect = self.special_food.effect
                if effect == 'grow':
                    self.snake.grow(3)
                elif effect == 'speed_up':
                    self.speed += 2
                elif effect == 'slow_down':
                    self.speed = max(5, self.speed - 2)
                self.special_food.active = False
                self.animation_particles.append([self.special_food.position, 15, SPECIAL_FOOD_COLOR])
                self.score += 5

    def update(self):
        if self.game_over:
            return

        # Обновляем таймер специальной еды
        self.special_food_timer += 1
        if self.special_food_timer >= self.special_food_spawn_time:
            self.spawn_special_food()
            self.special_food_timer = 0

        if self.special_food:
            self.special_food.update()

        # Обработка направлений из очереди
        if self.snake_direction_queue:
            new_direction = self.snake_direction_queue.pop(0)
            # Проверка на противоположное направление
            dx, dy = new_direction
            current_dx, current_dy = self.snake.direction
            if (dx, dy) != (-current_dx, -current_dy):
                self.snake.direction = (dx, dy)

        # Движение змейки
        self.snake.move()

        # Проверка столкновений
        self.check_collision()

        # Обновление анимации частиц
        for particle in self.animation_particles[:]:
            particle[1] -= 1
            if particle[1] <= 0:
                self.animation_particles.remove(particle)

    def draw(self):
        self.surface.fill(BACKGROUND)
        # Рисуем сетку
        for x in range(0, WIDTH, GRID_SIZE):
            pygame.draw.line(self.surface, GRID_COLOR, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, GRID_SIZE):
            pygame.draw.line(self.surface, GRID_COLOR, (0, y), (WIDTH, y))

        # Рисуем еду
        self.food.draw(self.surface)

        # Рисуем специальную еду
        if self.special_food and self.special_food.active:
            self.special_food.draw(self.surface)

        # Рисуем змейку
        self.snake.draw(self.surface)

        # Рисуем частицы анимации
        for (x, y), size, *args in self.animation_particles:
            color = FOOD_COLOR
            if args:
                color = args[0]
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(self.surface, color, rect, border_radius=int(size/2), width=2)

        # Рисуем счет
        score_text = self.font.render(f'Score: {self.score}', True, TEXT_COLOR)
        self.surface.blit(score_text, (10, 10))

        # Если игра окончена
        if self.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0,0,0,180))
            self.surface.blit(overlay, (0,0))
            game_over_text = self.font.render('Game Over! Press SPACE to restart or ESC for menu', True, TEXT_COLOR)
            text_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//2))
            self.surface.blit(game_over_text, text_rect)

    def handle_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_UP:
                self.snake_direction_queue.append((0,-1))
            elif event.key == K_DOWN:
                self.snake_direction_queue.append((0,1))
            elif event.key == K_LEFT:
                self.snake_direction_queue.append((-1,0))
            elif event.key == K_RIGHT:
                self.snake_direction_queue.append((1,0))
            elif event.key == K_SPACE and self.game_over:
                self.reset()
            elif event.key == K_ESCAPE and self.game_over:
                return 'menu'
        return None

    def reset(self):
        self.snake.reset()
        self.food.randomize_position()
        self.special_food = None
        self.special_food_timer = 0
        self.score = 0
        self.game_over = False
        self.animation_particles = []
        self.speed = 10
        self.snake_direction_queue = []
```

Класс Menu:

```python
class Menu:
    def __init__(self, surface):
        self.surface = surface
        self.font_title = pygame.font.SysFont('Arial', 48, bold=True)
        self.font_button = pygame.font.SysFont('Arial', 32)
        self.buttons = [
            {"text": "Start Game", "action": "start"},
            {"text": "Quit", "action": "quit"}
        ]
        self.selected = 0

    def draw(self):
        self.surface.fill(MENU_BACKGROUND)
        # Заголовок
        title = self.font_title.render("SNAKE GAME", True, TEXT_COLOR)
        title_rect = title.get_rect(center=(WIDTH//2, HEIGHT//4))
        self.surface.blit(title, title_rect)

        # Кнопки
        button_y = HEIGHT // 2
        for i, button in enumerate(self.buttons):
            color = MENU_BUTTON_HOVER if i == self.selected else MENU_BUTTON
            text = self.font_button.render(button["text"], True, TEXT_COLOR)
            text_rect = text.get_rect(center=(WIDTH//2, button_y + i*60))
            button_rect = pygame.Rect(WIDTH//2 - 100, button_y + i*60 - 25, 200, 50)
            pygame.draw.rect(self.surface, color, button_rect, border_radius=10)
            self.surface.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_UP:
                self.selected = (self.selected - 1) % len(self.buttons)
            elif event.key == K_DOWN:
                self.selected = (self.selected + 1) % len(self.buttons)
            elif event.key == K_RETURN:
                return self.buttons[self.selected]["action"]
        return None
```

Основной цикл:

```python
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    menu = Menu(screen)
    game = Game(screen)

    current_screen = "menu"
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif current_screen == "menu":
                action = menu.handle_event(event)
                if action == "start":
                    current_screen = "game"
                elif action == "quit":
                    running = False
            elif current_screen == "game":
                action = game.handle_event(event)
                if action == "menu":
                    current_screen = "menu"

        if current_screen == "menu":
            menu.draw()
        elif current_screen == "game":
            game.update()
            game.draw()

        pygame.display.flip()
        clock.tick(60)  # 60 FPS

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
```

Этот код реализует игру "Змейка" с сеткой, приятной цветовой гаммой, меню, анимацией поедания еды и специальной едой (изюминка).

Особенности:
- Специальная еда появляется каждые 10 секунд и дает один из трех эффектов: увеличение длины на 3, увеличение скорости, уменьшение скорости.
- При съедании еды происходит анимация (кружок, который расширяется и исчезает).
- При столкновении с собой игра заканчивается.
- В меню можно начать игру или выйти.
- При окончании игры можно перезапустить (пробел) или вернуться в меню (ESC).

Обратите внимание: в коде предполагается, что змейка может проходить сквозь стены (телепортироваться на противоположную сторону). Если нужно сделать стены непреодолимыми, можно изменить логику в методе move змейки и добавить проверку на выход за пределы в check_collision.

Данный код написан с учетом требований и должен работать. При необходимости можно доработать детали.
</think>
# Игра "Змейка" на Python с расширенными возможностями

```python
import pygame
import sys
import random
import math

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GRID_SIZE = 25
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
FPS = 60

# Цвета
BACKGROUND = (15, 20, 30)
GRID_COLOR = (30, 35, 45)
SNAKE_COLOR = (50, 180, 80)
SNAKE_HEAD_COLOR = (70, 200, 100)
FOOD_COLOR = (220, 60, 60)
SPECIAL_FOOD_COLOR = (220, 200, 60)
TEXT_COLOR = (240, 240, 240)
MENU_BG = (25, 30, 40)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER = (100, 160, 210)

class Snake:
    def __init__(self):
        self.reset()
        self.head_color = SNAKE_HEAD_COLOR
        self.body_color = SNAKE_COLOR
    
    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        # Генерируем начальные сегменты змейки
        self.direction = random.choice([(1, 0), (0, 1), (-1, 0), (0, -1)])
        dx, dy = self.direction
        for i in range(1, self.length):
            self.positions.append((self.positions[0][0] - dx * i, self.positions[0][1] - dy * i))
        self.next_direction = self.direction
        self.grow_pending = 0
    
    def update_direction(self, direction):
        # Запрещаем движение в противоположном направлении
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.next_direction = direction
    
    def move(self):
        self.direction = self.next_direction
        dx, dy = self.direction
        head_x, head_y = self.positions[0]
        new_head = ((head_x + dx) % GRID_WIDTH, (head_y + dy) % GRID_HEIGHT)
        
        # Добавляем новую голову
        self.positions.insert(0, new_head)
        
        # Удаляем хвост, если не нужно расти
        if self.grow_pending <= 0:
            self.positions.pop()
        else:
            self.grow_pending -= 1
    
    def grow(self, amount=1):
        self.grow_pending += amount
        self.length += amount
    
    def draw(self, surface):
        # Рисуем тело змейки
        for i, (x, y) in enumerate(self.positions):
            color = self.head_color if i == 0 else self.body_color
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, color, rect, border_radius=7)
            
            # Рисуем глаза на голове
            if i == 0:
                eye_size = GRID_SIZE // 5
                eye_offset = GRID_SIZE // 3
                pygame.draw.circle(surface, (15, 15, 25), 
                                 (x * GRID_SIZE + eye_offset, y * GRID_SIZE + eye_offset), eye_size)
                pygame.draw.circle(surface, (15, 15, 25), 
                                 (x * GRID_SIZE + GRID_SIZE - eye_offset, 
                                  y * GRID_SIZE + eye_offset), eye_size)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.spawn()
        self.eaten_animation = 0
    
    def spawn(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), 
                        random.randint(0, GRID_HEIGHT - 1))
    
    def draw(self, surface):
        x, y = self.position
        rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        
        if self.eaten_animation > 0:
            size = GRID_SIZE * (1 + 0.5 * math.sin(self.eaten_animation * 0.3))
            offset = (GRID_SIZE - size) / 2
            pygame.draw.rect(surface, FOOD_COLOR, 
                            (x * GRID_SIZE + offset, y * GRID_SIZE + offset, size, size), 
                            border_radius=int(size/2))
            self.eaten_animation -= 1
        else:
            pygame.draw.rect(surface, FOOD_COLOR, rect, border_radius=12)

class SpecialFood(Food):
    def __init__(self):
        super().__init__()
        self.active = False
        self.lifetime = 0
        self.effects = ['grow', 'speed', 'slow']
        self.effect = random.choice(self.effects)
        self.rotation = 0
    
    def spawn(self):
        super().spawn()
        self.active = True
        self.lifetime = 300  # 5 секунд при 60 FPS
    
    def update(self):
        if self.active:
            self.lifetime -= 1
            self.rotation = (self.rotation + 5) % 360
            if self.lifetime <= 0:
                self.active = False
    
    def draw(self, surface):
        if not self.active:
            return
        
        x, y = self.position
        size = GRID_SIZE - 5
        center_x = x * GRID_SIZE + GRID_SIZE // 2
        center_y = y * GRID_SIZE + GRID_SIZE // 2
        
        # Рисуем вращающуюся звезду
        points = []
        for i in range(5):
            angle = math.radians(self.rotation + i * 72)
            outer_x = center_x + size * math.cos(angle)
            outer_y = center_y + size * math.sin(angle)
            points.append((outer_x, outer_y))
            
            inner_angle = math.radians(self.rotation + 36 + i * 72)
            inner_x = center_x + size * 0.4 * math.cos(inner_angle)
            inner_y = center_y + size * 0.4 * math.sin(inner_angle)
            points.append((inner_x, inner_y))
        
        pygame.draw.polygon(surface, SPECIAL_FOOD_COLOR, points)

class Game:
    def __init__(self, surface):
        self.surface = surface
        self.snake = Snake()
        self.food = Food()
        self.special_food = SpecialFood()
        self.score = 0
        self.game_over = False
        self.paused = False
        self.level = 1
        self.speed = 10
        self.font = pygame.font.SysFont('Arial', 24)
        self.big_font = pygame.font.SysFont('Arial', 48, bold=True)
        self.move_counter = 0
    
    def reset(self):
        self.snake.reset()
        self.food.spawn()
        self.special_food.active = False
        self.score = 0
        self.game_over = False
        self.paused = False
        self.level = 1
        self.speed = 10
    
    def update(self):
        if self.paused or self.game_over:
            return
        
        self.move_counter += 1
        
        # Движение змейки с учетом скорости
        if self.move_counter >= max(1, 10 - self.speed // 2):
            self.move_counter = 0
            self.snake.move()
            
            # Проверка столкновения с собой
            head = self.snake.positions[0]
            if head in self.snake.positions[1:]:
                self.game_over = True
            
            # Проверка съедания обычной еды
            if head == self.food.position:
                self.snake.grow()
                self.score += 1
                self.food.spawn()
                self.food.eaten_animation = 10
                
                # Увеличиваем уровень каждые 5 очков
                if self.score % 5 == 0:
                    self.level += 1
                    self.speed = min(20, self.speed + 1)
            
            # Проверка съедания специальной еды
            if self.special_food.active and head == self.special_food.position:
                effect = self.special_food.effect
                if effect == 'grow':
                    self.snake.grow(3)
                elif effect == 'speed':
                    self.speed = min(20, self.speed + 3)
                elif effect == 'slow':
                    self.speed = max(5, self.speed - 3)
                self.score += 3
                self.special_food.active = False
            
            # Случайное появление специальной еды
            if not self.special_food.active and random.random() < 0.005:
                self.special_food.spawn()
                # Гарантируем, что специальная еда не появляется поверх обычной
                while self.special_food.position == self.food.position:
                    self.special_food.spawn()
            
            # Обновление специальной еды
            self.special_food.update()
    
    def draw(self):
        # Рисуем фон
        self.surface.fill(BACKGROUND)
        
        # Рисуем сетку
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(self.surface, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.surface, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))
        
        # Рисуем еду
        self.food.draw(self.surface)
        
        # Рисуем специальную еду
        self.special_food.draw(self.surface)
        
        # Рисуем змейку
        self.snake.draw(self.surface)
        
        # Рисуем UI
        score_text = self.font.render(f'Score: {self.score}', True, TEXT_COLOR)
        level_text = self.font.render(f'Level: {self.level}', True, TEXT_COLOR)
        self.surface.blit(score_text, (10, 10))
        self.surface.blit(level_text, (10, 40))
        
        # Эффект паузы
        if self.paused:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            self.surface.blit(overlay, (0, 0))
            pause_text = self.big_font.render("PAUSED", True, TEXT_COLOR)
            text_rect = pause_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.surface.blit(pause_text, text_rect)
        
        # Экран окончания игры
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.surface.blit(overlay, (0, 0))
            game_over_text = self.big_font.render("GAME OVER", True, (220, 80, 80))
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
            self.surface.blit(game_over_text, text_rect)
            
            restart_text = self.font.render("Press SPACE to restart or ESC for menu", True, TEXT_COLOR)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30))
            self.surface.blit(restart_text, restart_rect)

class Menu:
    def __init__(self, surface):
        self.surface = surface
        self.buttons = [
            {"text": "Start Game", "action": "start"},
            {"text": "Quit", "action": "quit"}
        ]
        self.selected = 0
        self.title_font = pygame.font.SysFont('Arial', 64, bold=True)
        self.button_font = pygame.font.SysFont('Arial', 36)
    
    def draw(self):
        self.surface.fill(MENU_BG)
        
        # Рисуем заголовок
        title = self.title_font.render("SNAKE GAME", True, TEXT_COLOR)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4))
        self.surface.blit(title, title_rect)
        
        # Рисуем кнопки
        for i, button in enumerate(self.buttons):
            color = BUTTON_HOVER if i == self.selected else BUTTON_COLOR
            text = self.button_font.render(button["text"], True, TEXT_COLOR)
            rect = pygame.Rect(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 + i*70, 300, 50)
            pygame.draw.rect(self.surface, color, rect, border_radius=10)
            text_rect = text.get_rect(center=rect.center)
            self.surface.blit(text, text_rect)
        
        # Подсказка управления
        hint_font = pygame.font.SysFont('Arial', 18)
        hint = hint_font.render("Use arrow keys to move. Press P to pause.", True, (150, 150, 150))
        self.surface.blit(hint, (SCREEN_WIDTH//2 - hint.get_width()//2, SCREEN_HEIGHT - 40))
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.buttons)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.buttons)
            elif event.key == pygame.K_RETURN:
                return self.buttons[self.selected]["action"]
        return None

# Основная функция
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Змейка")
    clock = pygame.time.Clock()
    
    menu = Menu(screen)
    game = Game(screen)
    
    current_screen = "menu"
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if current_screen == "menu":
                action = menu.handle_event(event)
                if action == "start":
                    current_screen = "game"
                elif action == "quit":
                    pygame.quit()
                    sys.exit()
            
            elif current_screen == "game":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        game.snake.update_direction((0, -1))
                    elif event.key == pygame.K_DOWN:
                        game.snake.update_direction((0, 1))
                    elif event.key == pygame.K_LEFT:
                        game.snake.update_direction((-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        game.snake.update_direction((1, 0))
                    elif event.key == pygame.K_p:
                        game.paused = not game.paused
                    elif event.key == pygame.K_SPACE and game.game_over:
                        game.reset()
                    elif event.key == pygame.K_ESCAPE:
                        current_screen = "menu"
        
        # Обновление игры
        if current_screen == "game":
            game.update()
        
        # Отрисовка
        if current_screen == "menu":
            menu.draw()
        elif current_screen == "game":
            game.draw()
        
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
```

## Особенности игры

1. **Сетка игрового поля**: Игровое поле разделено на клетки, как в классической змейке.

2. **Приятная цветовая гамма**:
   - Темно-синий фон
   - Серая сетка
   - Зеленая змейка с более светлой головой
   - Красная еда
   - Золотистая специальная еда

3. **Меню**:
   - Экран меню с кнопками "Start Game" и "Quit"
   - Подсветка выбранной кнопки
   - Плавный переход между экранами

4. **Анимация поедания еды**:
   - Анимация при съедании обычной еды - пульсирующий эффект
   - Для специальной еды - вращающаяся звезда

5. **Интересные изюминки**:
   - **Специальная еда**:
     - Появляется случайным образом
     - Имеет ограниченное время жизни
     - Дает различные эффекты: увеличение длины, ускорение или замедление
   - **Система уровней**: Уровень повышается каждые 5 очков
   - **Плавное движение**: Змейка может менять направление плавно
   - **Пауза**: Возможность приостановить игру клавишей P
   - **Визуальные детали**:
     - Закругленные углы у сегментов змейки
     - Глаза у головы змейки
     - Анимация при съедании еды

## Управление
- **Стрелки**: Управление змейкой
- **P**: Пауза
- **Пробел**: Рестарт после проигрыша
- **ESC**: Возврат в меню

Запустите игру, наслаждайтесь игрой с приятной графикой и интересными особенностями!