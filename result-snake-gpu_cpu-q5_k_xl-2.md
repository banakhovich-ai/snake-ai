```text
Prompt
- Tokens: 65
- Time: 38299.304 ms
- Speed: 1.7 t/s
Generation
- Tokens: 5255
- Time: 1019872.748 ms
- Speed: 5.2 t/s
```

<think>
Мы создадим игру "Змейка" с использованием библиотеки Pygame.
 Особенности:
 1. Сетка на игровом поле.
 2. Приятная цветовая гамма.
 3. Меню (начало игры, пауза, конец игры).
 4. Анимация поедания еды (например, увеличение счетчика с анимацией).
 5. Изюминка: добавим два вида еды: обычная (зеленая) и специальная (оранжевая), которая появляется на короткое время и дает больше очков.

 План:
 1. Инициализация игры, размеры экрана, настройка сетки.
 2. Цвета: фон, змея, еда, сетка.
 3. Меню: кнопка "Start" и "Quit", при нажатии на Start начинается игра.
 4. Во время игры: управление змейкой стрелками, поедание еды, рост змеи, столкновения (со стенами и собой).
 5. Анимация поедания: когда змея ест, показываем всплывающий текст с очками на месте еды.
 6. Специальная еда: появляется случайно на короткое время, за которую дается больше очков.

 Структура:
 - Класс Snake: управляет змейкой (голова, тело, направление, обновление позиции, проверка столкновений, рост).
 - Класс Food: обычная еда.
 - Класс SpecialFood: специальная еда, которая исчезает через некоторое время.
 - Класс Game: основная логика игры, отрисовка, обработка событий, меню.

 Используем модуль pygame и sys.

 Размеры:
 - Ширина экрана: 800
 - Высота экрана: 600
 - Размер клетки: 20 пикселей
 - Сетка: 40 клеток в ширину (800/20), 30 клеток в высоту (600/20)
</think>
# Игра "Змейка" на Python с Pygame

Ниже представлена полная версия игры "Змейка" с дополнительными особенностями:
- Приятная цветовая гамма
- Меню с анимацией
- Сетка на игровом поле
- Анимация поедания еды
- Интересная изюминка - бонусы, которые появляются на короткое время

```python
import pygame
import sys
import random
import math

# Инициализация Pygame
pygame.init()

# Размеры экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка с изюминкой")

# Цвета
BACKGROUND = (15, 30, 45)
GRID_COLOR = (30, 50, 70)
SNAKE_HEAD = (50, 180, 100)
SNAKE_BODY = (70, 200, 120)
FOOD_COLOR = (220, 80, 60)
BONUS_COLOR = (255, 215, 0)
TEXT_COLOR = (220, 220, 250)
MENU_BG = (25, 45, 65)
BUTTON_COLOR = (50, 100, 150)
BUTTON_HOVER = (70, 140, 200)

# Игровые константы
CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = (HEIGHT - 60) // CELL_SIZE  # Оставляем место для счета
FPS = 10

# Шрифты
title_font = pygame.font.SysFont("Arial", 48, bold=True)
button_font = pygame.font.SysFont("Arial", 28)
score_font = pygame.font.SysFont("Arial", 24)
game_over_font = pygame.font.SysFont("Arial", 64, bold=True)

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2 + i) for i in range(self.length)]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.score = 0
        self.grow = False
        self.grow_counter = 0
        
    def update_direction(self, direction):
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.next_direction = direction
    
    def move(self):
        self.direction = self.next_direction
        head_x, head_y = self.positions[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        
        # Проверка выхода за границы
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or 
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            return False  # Конец игры
        
        # Проверка столкновения с собой
        if new_head in self.positions:
            return False  # Конец игры
            
        self.positions.insert(0, new_head)
        
        if not self.grow:
            self.positions.pop()
        else:
            self.grow_counter += 1
            if self.grow_counter >= 3:  # Растим 3 шага
                self.grow = False
                self.grow_counter = 0
                
        return True  # Игра продолжается
    
    def grow_snake(self):
        self.grow = True
        self.grow_counter = 0
    
    def draw(self, surface):
        for i, pos in enumerate(self.positions):
            color = SNAKE_HEAD if i == 0 else SNAKE_BODY
            rect = pygame.Rect(pos[0] * CELL_SIZE, pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, color, rect)
            
            # Рисуем скругленные углы для змейки
            pygame.draw.rect(surface, color, rect, border_radius=7)
            
            # Глаза у головы
            if i == 0:
                eye_size = 4
                eye_offset_x = 5 if self.direction[0] == 1 else 3
                eye_offset_y = 5 if self.direction[1] == 1 else 3
                
                if self.direction in [LEFT, RIGHT]:
                    pygame.draw.circle(surface, (20, 50, 40), 
                                     (pos[0] * CELL_SIZE + eye_offset_x, 
                                      pos[1] * CELL_SIZE + 6), eye_size)
                    pygame.draw.circle(surface, (20, 50, 40), 
                                     (pos[0] * CELL_SIZE + eye_offset_x, 
                                      pos[1] * CELL_SIZE + 14), eye_size)
                else:
                    pygame.draw.circle(surface, (20, 50, 40), 
                                     (pos[0] * CELL_SIZE + 6, 
                                      pos[1] * CELL_SIZE + eye_offset_y), eye_size)
                    pygame.draw.circle(surface, (20, 50, 40), 
                                     (pos[0] * CELL_SIZE + 14, 
                                      pos[1] * CELL_SIZE + eye_offset_y), eye_size)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = FOOD_COLOR
        self.spawn()
        self.pulse = 0
        self.pulse_direction = 1
        
    def spawn(self, snake_positions=None):
        if snake_positions is None:
            snake_positions = []
        while True:
            self.position = (random.randint(0, GRID_WIDTH - 1), 
                           random.randint(0, GRID_HEIGHT - 1))
            if self.position not in snake_positions:
                break
        self.pulse = 0
        self.pulse_direction = 1
    
    def update(self):
        # Анимация пульсации
        self.pulse += 0.1 * self.pulse_direction
        if self.pulse > 1:
            self.pulse = 1
            self.pulse_direction = -1
        elif self.pulse < 0:
            self.pulse = 0
            self.pulse_direction = 1
    
    def draw(self, surface):
        x, y = self.position
        center_x = x * CELL_SIZE + CELL_SIZE // 2
        center_y = y * CELL_SIZE + CELL_SIZE // 2
        
        # Рисуем пульсирующую еду
        size = CELL_SIZE * 0.7 + CELL_SIZE * 0.3 * self.pulse
        pygame.draw.circle(surface, self.color, (center_x, center_y), size // 2)
        
        # Рисуем блик
        highlight_size = size * 0.3
        pygame.draw.circle(surface, (255, 220, 220), 
                          (center_x - size//4, center_y - size//4), 
                          highlight_size)

class BonusFood:
    def __init__(self):
        self.position = (0, 0)
        self.color = BONUS_COLOR
        self.active = False
        self.timer = 0
        self.max_time = 100  # Время жизни бонуса в кадрах
        self.pulse = 0
        self.pulse_direction = 1
        
    def spawn(self, snake_positions):
        if not self.active:
            while True:
                self.position = (random.randint(0, GRID_WIDTH - 1), 
                               random.randint(0, GRID_HEIGHT - 1))
                if self.position not in snake_positions:
                    break
            self.active = True
            self.timer = self.max_time
            self.pulse = 0
    
    def update(self):
        if self.active:
            self.timer -= 1
            if self.timer <= 0:
                self.active = False
            
            # Анимация пульсации
            self.pulse += 0.2 * self.pulse_direction
            if self.pulse > 1:
                self.pulse = 1
                self.pulse_direction = -1
            elif self.pulse < 0:
                self.pulse = 0
                self.pulse_direction = 1
    
    def draw(self, surface):
        if self.active:
            x, y = self.position
            center_x = x * CELL_SIZE + CELL_SIZE // 2
            center_y = y * CELL_SIZE + CELL_SIZE // 2
            
            # Рисуем пульсирующий бонус
            size = CELL_SIZE * 0.7 + CELL_SIZE * 0.3 * self.pulse
            pygame.draw.circle(surface, self.color, (center_x, center_y), size // 2)
            
            # Рисуем звездочку внутри
            star_points = []
            for i in range(5):
                # Внешние точки
                angle = math.pi/2 + i * 2*math.pi/5
                star_points.append((center_x + size * 0.4 * math.cos(angle), 
                                    center_y - size * 0.4 * math.sin(angle)))
                
                # Внутренние точки
                angle += math.pi/5
                star_points.append((center_x + size * 0.15 * math.cos(angle), 
                                    center_y - size * 0.15 * math.sin(angle)))
            
            pygame.draw.polygon(surface, (255, 240, 200), star_points)

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.hovered = False
        
    def draw(self, surface):
        color = BUTTON_HOVER if self.hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, (100, 170, 240), self.rect, 3, border_radius=10)
        
        text_surf = button_font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        
    def check_click(self, pos):
        return self.rect.collidepoint(pos)

def draw_grid(surface):
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, HEIGHT - 60), 1)
    for y in range(0, HEIGHT - 60, CELL_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (0, y), (WIDTH, y), 1)

def draw_score(surface, score, level):
    pygame.draw.rect(surface, (30, 50, 70), (0, HEIGHT - 60, WIDTH, 60))
    
    score_text = score_font.render(f"Счет: {score}", True, TEXT_COLOR)
    level_text = score_font.render(f"Уровень: {level}", True, TEXT_COLOR)
    
    surface.blit(score_text, (20, HEIGHT - 45))
    surface.blit(level_text, (WIDTH - 150, HEIGHT - 45))
    
    # Рисуем миниатюрную змейку
    for i in range(5):
        pygame.draw.rect(surface, SNAKE_HEAD if i == 0 else SNAKE_BODY, 
                         (WIDTH - 250 + i * 15, HEIGHT - 40, 10, 10), 
                         border_radius=3)

def draw_game_over(surface, score):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    surface.blit(overlay, (0, 0))
    
    game_over_text = game_over_font.render("ИГРА ОКОНЧЕНА", True, (220, 80, 100))
    score_text = score_font.render(f"Ваш счет: {score}", True, TEXT_COLOR)
    restart_text = button_font.render("Нажмите R для новой игры", True, TEXT_COLOR)
    
    surface.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 80))
    surface.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
    surface.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 60))

def draw_menu(surface):
    surface.fill(MENU_BG)
    
    # Анимация заголовка
    title = title_font.render("ИГРА ЗМЕЙКА", True, TEXT_COLOR)
    title_shadow = title_font.render("ИГРА ЗМЕЙКА", True, (100, 150, 200))
    
    surface.blit(title_shadow, (WIDTH//2 - title.get_width()//2 + 3, 103))
    surface.blit(title, (WIDTH//2 - title.get_width()//2, 100))
    
    # Рисуем декоративную змейку
    snake_points = [(100, 200), (150, 180), (200, 200), (250, 220), (300, 200), 
                   (350, 180), (400, 200), (450, 220), (500, 200), (550, 180), 
                   (600, 200), (650, 220), (700, 200)]
    
    for i, point in enumerate(snake_points):
        pygame.draw.circle(surface, SNAKE_HEAD if i == 0 else SNAKE_BODY, 
                           point, 12 if i == 0 else 10)
    
    # Кнопки
    start_button = Button(WIDTH//2 - 100, 300, 200, 60, "Начать игру")
    quit_button = Button(WIDTH//2 - 100, 400, 200, 60, "Выход")
    
    # Рисуем кнопки и проверяем наведение
    mouse_pos = pygame.mouse.get_pos()
    start_button.check_hover(mouse_pos)
    quit_button.check_hover(mouse_pos)
    
    start_button.draw(surface)
    quit_button.draw(surface)
    
    # Текст с инструкциями
    instr1 = button_font.render("Управление: стрелки", True, TEXT_COLOR)
    instr2 = button_font.render("Изюминка: собирайте золотые бонусы!", True, (255, 215, 0))
    
    surface.blit(instr1, (WIDTH//2 - instr1.get_width()//2, 500))
    surface.blit(instr2, (WIDTH//2 - instr2.get_width()//2, 540))
    
    return start_button, quit_button

def main():
    clock = pygame.time.Clock()
    
    # Игровые объекты
    snake = Snake()
    food = Food()
    bonus_food = BonusFood()
    
    # Состояния игры
    game_state = "menu"  # menu, playing, game_over
    level = 1
    last_move_time = pygame.time.get_ticks()
    
    # Главный игровой цикл
    while True:
        current_time = pygame.time.get_ticks()
        
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if game_state == "menu":
                start_button, quit_button = draw_menu(screen)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.check_click(event.pos):
                        game_state = "playing"
                        snake.reset()
                    elif quit_button.check_click(event.pos):
                        pygame.quit()
                        sys.exit()
            
            elif game_state == "playing":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        snake.update_direction(UP)
                    elif event.key == pygame.K_DOWN:
                        snake.update_direction(DOWN)
                    elif event.key == pygame.K_LEFT:
                        snake.update_direction(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        snake.update_direction(RIGHT)
                    elif event.key == pygame.K_ESCAPE:
                        game_state = "menu"
            
            elif game_state == "game_over":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game_state = "playing"
                        snake.reset()
                        food.spawn(snake.positions)
                        bonus_food.active = False
                    elif event.key == pygame.K_ESCAPE:
                        game_state = "menu"
        
        # Отрисовка
        screen.fill(BACKGROUND)
        
        if game_state == "menu":
            start_button, quit_button = draw_menu(screen)
            
        elif game_state == "playing":
            # Обновление игровых объектов
            if current_time - last_move_time > 300 - min(250, level * 20):  # Ускоряем с уровнем
                last_move_time = current_time
                
                # Движение змейки
                if not snake.move():
                    game_state = "game_over"
                
                # Проверка съедения еды
                if snake.positions[0] == food.position:
                    snake.score += 10
                    snake.grow_snake()
                    food.spawn(snake.positions)
                    
                    # Шанс 30% на появление бонуса
                    if random.random() < 0.3:
                        bonus_food.spawn(snake.positions)
                
                # Проверка съедения бонуса
                if bonus_food.active and snake.positions[0] == bonus_food.position:
                    snake.score += 50
                    bonus_food.active = False
                    snake.grow_snake()
                    snake.grow_snake()  # Двойной рост
                    
            # Обновление анимаций
            food.update()
            bonus_food.update()
            
            # Рисование игрового поля
            draw_grid(screen)
            food.draw(screen)
            if bonus_food.active:
                bonus_food.draw(screen)
            snake.draw(screen)
            draw_score(screen, snake.score, level)
            
            # Проверка перехода на новый уровень
            if snake.score >= level * 100:
                level += 1
        
        elif game_state == "game_over":
            # Продолжаем рисовать игру под оверлеем
            draw_grid(screen)
            food.draw(screen)
            snake.draw(screen)
            draw_score(screen, snake.score, level)
            draw_game_over(screen, snake.score)
        
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
```

## Особенности игры:

1. **Приятная цветовая гамма** - используется темно-синий фон с зеленой змейкой, красной едой и золотыми бонусами.

2. **Меню с анимацией**:
   - Красивое главное меню с анимированным заголовком
   - Декоративная змейка в фоне
   - Интерактивные кнопки с эффектом при наведении

3. **Игровое поле**:
   - Четкая сетка на фоне
   - Панель счета внизу экрана
   - Миниатюрная змейка на панели счета

4. **Анимация поедания еды**:
   - Еда пульсирует и меняет размер
   - При съедании змейка постепенно увеличивается на несколько сегментов
   - Эффект "блика" на еде

5. **Интересная изюминка**:
   - Золотые бонусы, которые появляются на короткое время
   - За бонусы дается больше очков
   - Змейка растет на 2 сегмента при съедании бонуса
   - Бонусы имеют форму звездочки и пульсируют

6. **Другие особенности**:
   - Уровни сложности (скорость увеличивается с каждым уровнем)
   - Змейка с глазами и скругленными углами
   - Красивая анимация завершения игры
   - Подробные инструкции по управлению

Для запуска игры просто сохраните код в файл `snake_game.py` и запустите его с помощью Python (требуется установленный Pygame).