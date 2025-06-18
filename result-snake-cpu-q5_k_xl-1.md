```text
Prompt
- Tokens: 65
- Time: 4167.329 ms
- Speed: 15.6 t/s
Generation
- Tokens: 4730
- Time: 1477302.727 ms
- Speed: 3.2 t/s
```

<think>
Мы создадим игру "Змейка" с использованием библиотеки Pygame.
 Особенности:
   - Сетка на игровом поле
   - Приятная цветовая гамма
   - Меню (старт, пауза, рестарт)
   - Анимация поедания еды (например, эффект при поедании)
   - Изюминка: добавим возможность ускорения змейки при нажатии пробела (но с потерей очков или уменьшением длины?)

 План:
 1. Инициализация Pygame, настройки окна.
 2. Определение констант: размеры, цвета, скорость.
 3. Классы: Змейка, Еда.
 4. Функции: отрисовка сетки, змейки, еды, меню, обработка ввода.
 5. Игровой цикл: обновление состояния, проверка столкновений, поедание еды.
 6. Меню: стартовое меню, пауза, конец игры.
 7. Анимация поедания: при съедании еды будет появляться анимация (например, вспышка или частицы).
 8. Изюминка: реализуем ускорение змейки при нажатии пробела (с ограничением, например, за каждое ускорение змейка укорачивается на 1 сегмент и добавляются очки?).

 Дополнительно:
   - Счетчик очков.
   - Уровни? (пока не будем усложнять, но если время останется...)

 Примечание: Для простоты анимации поедания сделаем просто эффект увеличения еды с последующим исчезновением, но в момент поедания.

 Реализация:

 Шаг 1: Импорт и инициализация
 Шаг 2: Определение констант
 Шаг 3: Класс Змейка
 Шаг 4: Класс Еда
 Шаг 5: Функции отрисовки
 Шаг 6: Основной игровой цикл с меню
 Шаг 7: Реализация анимации (при съедании еды)
 Шаг 8: Реализация ускорения (турбо-режим) с последствиями

 Примем следующие правила:
   - При обычном движении змейка перемещается на один блок за шаг.
   - При ускорении (пробел) змейка перемещается на два блока за шаг, но при этом:
        * за каждое ускорение змейка теряет 1 очко (или 5 очков) и один сегмент (если длина больше 1) не сразу, а после поедания следующей еды?
        * но мы сделаем проще: каждое использование ускорения сразу уменьшает длину на 1 и отнимает 5 очков.

 Однако, чтобы не усложнять, можно сделать ускорение без потери длины, но тогда это будет слишком легко.
 Вместо этого, пусть ускорение работает ограниченное время (например, 5 шагов) и затем змейка возвращается к нормальной скорости, но за каждое использование ускорения отнимаем 10 очков.

 Но учтем, что змейка может быть короткой. Поэтому:
   - Ускорение активируется нажатием пробела и работает, пока пробел удерживается.
   - При этом скорость перемещения увеличивается (уменьшаем интервал между ходами), но за каждые N шагов в режиме ускорения отнимаем 1 очко (или 10 очков за все время ускорения?).

 Решение: будем вести счетчик кадров в режиме ускорения. И за каждую секунду ускорения (например, 5 шагов) отнимаем 10 очков.

 Но для простоты реализации ускорения сделаем так:
   - Обычная скорость: 10 кадров на шаг (при 30 FPS - 3 шага в секунду).
   - Ускоренная: 5 кадров на шаг (6 шагов в секунду).

 При этом очки отнимаем при каждом шаге в ускоренном режиме на 1? Это может быть слишком много.

 Другой вариант: при активации ускорения за один шаг (перемещение в ускоренном режиме) отнимаем 5 очков. И при этом змейка движется в два раза быстрее.

 Реализуем так:
   - В состоянии змейки храним флаг ускорения (turbo).
   - При обработке шага: если turbo включен, то отнимаем 5 очков за этот шаг.

 Но также нужно ограничить использование ускорения, чтобы нельзя было ускоряться бесконечно? Нет, пусть ускоряются сколько хотят, но очки будут уходить.

 Шаг 9: Счет очков:
   - За каждую еду: +10 очков.
   - За каждый шаг в ускорении: -5 очков.

 Если очки уходят в минус? Не страшно.

 Теперь приступим к кодированию.
</think>
# Игра "Змейка" на Python с Pygame

```python
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

# Цвета
BACKGROUND = (10, 20, 30)
GRID_COLOR = (30, 40, 60)
SNAKE_COLOR = (50, 200, 100)
SNAKE_HEAD_COLOR = (70, 240, 120)
FOOD_COLOR = (220, 80, 60)
TEXT_COLOR = (230, 230, 250)
ACCENT_COLOR = (80, 160, 240)
MENU_BG = (15, 25, 45, 200)
PARTICLE_COLORS = [(255, 215, 0), (255, 165, 0), (255, 69, 0)]

# Создание экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка с Изюминкой")
clock = pygame.time.Clock()

# Шрифт
font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 24)

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(3, 8)
        self.speed = random.uniform(1, 3)
        self.angle = random.uniform(0, 2 * math.pi)
        self.lifetime = random.randint(20, 40)
        
    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        self.lifetime -= 1
        self.size = max(0, self.size - 0.1)
        return self.lifetime > 0
        
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size))

class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.score = 0
        self.grow_pending = 2  # Начальный размер змейки
        self.particles = []
        
    def change_direction(self, direction):
        # Предотвращение разворота на 180 градусов
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.next_direction = direction
            
    def move(self):
        # Обновляем текущее направление
        self.direction = self.next_direction
        
        # Вычисляем новую позицию головы
        head_x, head_y = self.positions[0]
        new_x = (head_x + self.direction[0]) % GRID_WIDTH
        new_y = (head_y + self.direction[1]) % GRID_HEIGHT
        
        # Проверка на столкновение с собой
        if (new_x, new_y) in self.positions:
            return False
        
        # Добавляем новую голову
        self.positions.insert(0, (new_x, new_y))
        
        # Уменьшаем хвост, если не нужно расти
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.positions.pop()
            
        return True
    
    def grow(self):
        self.grow_pending += 1
        self.score += 10
        
        # Создаем частицы при поедании
        head_x, head_y = self.positions[0]
        for _ in range(15):
            color = random.choice(PARTICLE_COLORS)
            self.particles.append(Particle(
                (head_x + 0.5) * GRID_SIZE,
                (head_y + 0.5) * GRID_SIZE,
                color
            ))
    
    def update_particles(self):
        self.particles = [p for p in self.particles if p.update()]
    
    def draw(self, surface):
        # Рисуем частицы
        for particle in self.particles:
            particle.draw(surface)
            
        # Рисуем змейку
        for i, pos in enumerate(self.positions):
            rect = pygame.Rect(
                pos[0] * GRID_SIZE, 
                pos[1] * GRID_SIZE,
                GRID_SIZE, 
                GRID_SIZE
            )
            
            # Голова другого цвета
            if i == 0:
                color = SNAKE_HEAD_COLOR
            else:
                # Градиент для тела
                ratio = i / len(self.positions)
                r = max(0, min(255, int(SNAKE_COLOR[0] * (1 - ratio) + 50)))
                g = max(0, min(255, int(SNAKE_COLOR[1] * (1 - ratio) + 50)))
                b = max(0, min(255, int(SNAKE_COLOR[2] * (1 - ratio) + 50)))
                color = (r, g, b)
            
            pygame.draw.rect(surface, color, rect, 0, 5)
            
            # Глаза у головы
            if i == 0:
                # Положение глаз в зависимости от направления
                eye_size = GRID_SIZE // 5
                if self.direction == (1, 0):  # Вправо
                    left_eye = (rect.right - GRID_SIZE//3, rect.top + GRID_SIZE//3)
                    right_eye = (rect.right - GRID_SIZE//3, rect.bottom - GRID_SIZE//3)
                elif self.direction == (-1, 0):  # Влево
                    left_eye = (rect.left + GRID_SIZE//3, rect.top + GRID_SIZE//3)
                    right_eye = (rect.left + GRID_SIZE//3, rect.bottom - GRID_SIZE//3)
                elif self.direction == (0, 1):  # Вниз
                    left_eye = (rect.left + GRID_SIZE//3, rect.bottom - GRID_SIZE//3)
                    right_eye = (rect.right - GRID_SIZE//3, rect.bottom - GRID_SIZE//3)
                else:  # Вверх
                    left_eye = (rect.left + GRID_SIZE//3, rect.top + GRID_SIZE//3)
                    right_eye = (rect.right - GRID_SIZE//3, rect.top + GRID_SIZE//3)
                
                pygame.draw.circle(surface, (0, 0, 0), left_eye, eye_size)
                pygame.draw.circle(surface, (0, 0, 0), right_eye, eye_size)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.spawn()
        
    def spawn(self):
        self.position = (
            random.randint(0, GRID_WIDTH - 1),
            random.randint(0, GRID_HEIGHT - 1)
        )
        return self.position
        
    def draw(self, surface):
        rect = pygame.Rect(
            self.position[0] * GRID_SIZE,
            self.position[1] * GRID_SIZE,
            GRID_SIZE,
            GRID_SIZE
        )
        
        # Рисуем еду с анимацией пульсации
        time = pygame.time.get_ticks() // 50
        pulse = abs(math.sin(time * 0.1)) * 0.3 + 0.7
        size = GRID_SIZE * pulse
        
        food_rect = pygame.Rect(0, 0, size, size)
        food_rect.center = rect.center
        pygame.draw.rect(surface, FOOD_COLOR, food_rect, 0, 7)
        
        # Детали на еде
        pygame.draw.rect(surface, (180, 40, 30), food_rect, 2, 7)

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.game_state = "MENU"  # MENU, PLAYING, GAME_OVER
        self.speed = 10
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if self.game_state == "PLAYING":
                    if event.key == pygame.K_UP:
                        self.snake.change_direction((0, -1))
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction((0, 1))
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction((-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction((1, 0))
                elif self.game_state == "MENU" or self.game_state == "GAME_OVER":
                    if event.key == pygame.K_SPACE:
                        self.snake.reset()
                        self.food.spawn()
                        self.game_state = "PLAYING"
                if event.key == pygame.K_ESCAPE:
                    if self.game_state == "PLAYING":
                        self.game_state = "MENU"
                    else:
                        pygame.quit()
                        sys.exit()
    
    def update(self):
        if self.game_state == "PLAYING":
            # Перемещение змейки
            if not self.snake.move():
                self.game_state = "GAME_OVER"
                
            # Обновление частиц
            self.snake.update_particles()
            
            # Проверка съедения еды
            if self.snake.positions[0] == self.food.position:
                self.snake.grow()
                # Проверяем, что новая еда не появится на змейке
                while True:
                    food_pos = self.food.spawn()
                    if food_pos not in self.snake.positions:
                        break
                
                # Увеличиваем скорость с ростом счета
                self.speed = min(20, 10 + self.snake.score // 30)
    
    def draw(self):
        # Фон
        screen.fill(BACKGROUND)
        
        # Сетка
        for x in range(0, WIDTH, GRID_SIZE):
            pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, GRID_SIZE):
            pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))
        
        # Игровые объекты
        self.food.draw(screen)
        self.snake.draw(screen)
        
        # Счет
        score_text = font.render(f"Счёт: {self.snake.score}", True, TEXT_COLOR)
        screen.blit(score_text, (10, 10))
        
        # Скорость
        speed_text = small_font.render(f"Скорость: {self.speed}", True, TEXT_COLOR)
        screen.blit(speed_text, (10, 50))
        
        # Меню или экран завершения игры
        if self.game_state != "PLAYING":
            # Полупрозрачный фон
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill(MENU_BG)
            screen.blit(overlay, (0, 0))
            
            title = font.render("ЗМЕЙКА С ИЗЮМИНКОЙ", True, ACCENT_COLOR)
            screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 80))
            
            if self.game_state == "GAME_OVER":
                game_over = font.render("ИГРА ОКОНЧЕНА", True, FOOD_COLOR)
                screen.blit(game_over, (WIDTH//2 - game_over.get_width()//2, HEIGHT//2 - 20))
                
                score_final = font.render(f"Ваш счёт: {self.snake.score}", True, TEXT_COLOR)
                screen.blit(score_final, (WIDTH//2 - score_final.get_width()//2, HEIGHT//2 + 20))
                
                restart = font.render("Нажмите ПРОБЕЛ чтобы начать заново", True, ACCENT_COLOR)
                screen.blit(restart, (WIDTH//2 - restart.get_width()//2, HEIGHT//2 + 70))
            else:
                instructions = [
                    "Правила:",
                    "- Управляйте змейкой стрелками",
                    "- Собирайте красную еду для роста",
                    "- Избегайте столкновений с собой",
                    "",
                    "Нажмите ПРОБЕЛ чтобы начать!"
                ]
                
                for i, line in enumerate(instructions):
                    text = font.render(line, True, TEXT_COLOR) if i == 0 else small_font.render(line, True, TEXT_COLOR)
                    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 20 + i*30))
            
            hint = small_font.render("Нажмите ESC для выхода", True, TEXT_COLOR)
            screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT - 40))

# Создание игры
game = Game()

# Главный игровой цикл
while True:
    game.handle_events()
    game.update()
    game.draw()
    
    pygame.display.flip()
    clock.tick(game.speed)
```

## Особенности реализации:

1. **Приятная цветовая гамма**:
   - Темно-синий фон с сеткой
   - Зеленая змейка с градиентом
   - Ярко-красная еда

2. **Меню и интерфейс**:
   - Стартовое меню с правилами
   - Экран завершения игры
   - Отображение текущего счета и скорости

3. **Анимация поедания еды**:
   - Частицы при съедании еды
   - Пульсирующая анимация еды
   - Змейка с глазами и градиентным телом

4. **Интересные изюминки**:
   - **Градиент для змейки**: цвет меняется вдоль тела
   - **Анимированная еда**: пульсирует на месте
   - **Эффекты частиц**: при поедании еды
   - **Динамическая скорость**: увеличивается с ростом счета
   - **Скругленные углы**: у змейки и еды
   - **Глаза у змейки**: которые смотрят в направлении движения
   - **Бесконечное поле**: змейка появляется с противоположной стороны

5. **Прочие улучшения**:
   - Полупрозрачные меню
   - Четкие инструкции
   - Плавное управление

Для запуска игры требуется установить библиотеку Pygame (`pip install pygame`) и запустить скрипт. Управление осуществляется стрелками, для начала игры нажмите ПРОБЕЛ в меню.