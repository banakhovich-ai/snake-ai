```text
Prompt
- Tokens: 61
- Time: 22990.282 ms
- Speed: 2.7 t/s
Generation
- Tokens: 5211
- Time: 787872.522 ms
- Speed: 6.6 t/s
```

<think>
Создадим игру "Змейка" с использованием библиотеки Pygame.
 План:
 1. Инициализация игры, создание окна.
 2. Определение цветов.
 3. Создание сетки.
 4. Реализация меню.
 5. Реализация змейки, еды и механики движения.
 6. Анимация поедания еды (например, вспышка или эффект).
 7. Изюминка: добавим особые виды еды, которые дают разные эффекты (например, ускорение, замедление, увеличение длины и т.д.)

 Для простоты будем использовать:
   - Обычную еду (зеленый квадрат) - добавляет 1 сегмент и 10 очков.
   - Особые виды еды (разные цвета) с разными эффектами.

 Эффекты особой еды:
   - Красная: ускорение змеи на некоторое время.
   - Синяя: замедление змеи на некоторое время.
   - Желтая: добавляет сразу 3 сегмента и 30 очков.
   - Фиолетовая: уменьшает длину змеи на 2 сегмента (но не меньше 1) и добавляет 5 очков.

 Особую еду будем генерировать реже и она будет исчезать через некоторое время.

 Также добавим меню:
   - Начальное меню: кнопки "Играть", "Настройки", "Выход". В настройках пока можно только изменить сложность (скорость змеи).
   - Пауза во время игры: нажатие ESC или P.
   - Экран окончания игры.

 Анимация поедания: при поедании еды сделаем эффект расширяющегося круга вокруг змеиной головы.

 Реализуем классы:
   - Snake
   - Food (обычная и особые)
   - Game

 Шаги выполнения:

 1. Установка Pygame (если не установлен): pip install pygame
 2. Импорт модулей.
 3. Инициализация Pygame.

 Приятная цветовая гамма (например, темно-зеленый фон, светло-зеленый для змеи, красный для обычной еды, и другие для особой).

 Сетка: нарисуем сетку на фоне.

 Изюминка: разные виды еды с разными эффектами.

 Давайте начнем писать код.
</think>
# Игра "Змейка" с изюминкой - Специальные бонусы

Вот полная реализация игры "Змейка" на Python с использованием библиотеки Pygame. Игра включает:
- Сетку игрового поля
- Приятную цветовую гамму
- Меню с выбором сложности
- Анимацию поедания еды
- Изюминку - специальные бонусы с эффектами

```python
import pygame
import sys
import random
import math
from pygame.locals import *

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
FPS = 60

# Цвета
BACKGROUND = (15, 56, 15)
GRID_COLOR = (40, 80, 40)
SNAKE_COLOR = (50, 168, 82)
SNAKE_HEAD_COLOR = (35, 140, 65)
FOOD_COLOR = (231, 76, 60)
TEXT_COLOR = (236, 240, 241)
UI_BG = (30, 60, 30, 180)
UI_BORDER = (70, 120, 70)

# Специальные бонусы (изюминка)
BONUS_COLORS = [
    (41, 128, 185),  # Синий - замедление времени
    (155, 89, 182),  # Фиолетовый - ускорение змейки
    (243, 156, 18),  # Оранжевый - телепорт
]
BONUS_EFFECTS = ["slow_time", "speed_boost", "teleport"]

# Направления
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Инициализация экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Змейка с Бонусами')
clock = pygame.time.Clock()

# Шрифты
font_large = pygame.font.Font(None, 72)
font_medium = pygame.font.Font(None, 48)
font_small = pygame.font.Font(None, 36)

class Snake:
    def __init__(self):
        self.reset()
        self.growth_pending = 0
        
    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.score = 0
        self.growth_pending = 0
        self.speed = 8  # Скорость по умолчанию
        self.speed_boost_timer = 0
        self.slow_time_factor = 1.0
        
    def update_direction(self, direction):
        # Запрещаем разворот на 180 градусов
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.next_direction = direction
            
    def move(self):
        self.direction = self.next_direction
        head_x, head_y = self.positions[0]
        new_x = (head_x + self.direction[0]) % GRID_WIDTH
        new_y = (head_y + self.direction[1]) % GRID_HEIGHT
        new_head = (new_x, new_y)
        
        # Проверка столкновения с собой
        if new_head in self.positions[1:]:
            return False
        
        self.positions.insert(0, new_head)
        
        # Добавление хвоста, если нужно
        if self.growth_pending > 0:
            self.growth_pending -= 1
        else:
            self.positions.pop()
        
        return True
        
    def grow(self, amount=1):
        self.growth_pending += amount
        
    def get_head_position(self):
        return self.positions[0]
        
    def draw(self, surface):
        # Рисуем голову
        head_pos = self.positions[0]
        pygame.draw.rect(surface, SNAKE_HEAD_COLOR, 
                         (head_pos[0] * GRID_SIZE, head_pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, (20, 100, 40), 
                         (head_pos[0] * GRID_SIZE, head_pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
        
        # Рисуем тело
        for i, pos in enumerate(self.positions[1:]):
            # Плавный переход цвета от головы к хвосту
            color_factor = 1.0 - (i / len(self.positions))
            body_color = (
                max(30, int(SNAKE_COLOR[0] * color_factor)),
                max(30, int(SNAKE_COLOR[1] * color_factor)),
                max(30, int(SNAKE_COLOR[2] * color_factor))
            )
            pygame.draw.rect(surface, body_color, 
                             (pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, (20, 100, 40), 
                             (pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
            
    def update_effects(self):
        # Обновление таймеров эффектов
        if self.speed_boost_timer > 0:
            self.speed_boost_timer -= 1
            if self.speed_boost_timer == 0:
                self.speed = 8  # Возвращаем нормальную скорость

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = FOOD_COLOR
        self.eaten_animation = 0
        self.is_bonus = False
        self.bonus_type = None
        self.randomize_position()
        
    def randomize_position(self, snake_positions=None):
        if snake_positions is None:
            snake_positions = []
            
        while True:
            self.position = (random.randint(0, GRID_WIDTH - 1), 
                           (random.randint(0, GRID_HEIGHT - 1)))
            if self.position not in snake_positions:
                break
                
        # Случайно определяем, будет ли это обычная еда или бонус (20% шанс)
        self.is_bonus = random.random() < 0.2
        if self.is_bonus:
            self.bonus_type = random.choice(BONUS_EFFECTS)
            self.color = random.choice(BONUS_COLORS)
        else:
            self.color = FOOD_COLOR
            self.bonus_type = None
            
    def draw(self, surface):
        x, y = self.position
        rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        
        # Анимация поедания
        if self.eaten_animation > 0:
            radius = int(GRID_SIZE * 0.7 * (self.eaten_animation / 10))
            pygame.draw.circle(surface, (255, 255, 200), rect.center, radius)
            self.eaten_animation -= 1
        else:
            # Рисуем еду с эффектом свечения
            pygame.draw.rect(surface, self.color, rect)
            pygame.draw.rect(surface, (255, 255, 255, 100), rect, 1)
            
            # Для бонусов добавляем эффект
            if self.is_bonus:
                pygame.draw.circle(surface, (255, 255, 255, 150), rect.center, GRID_SIZE // 2, 1)
                
    def start_eaten_animation(self):
        self.eaten_animation = 10

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.food.randomize_position(self.snake.positions)
        self.game_state = "MENU"  # MENU, PLAYING, GAME_OVER
        self.difficulty = "NORMAL"  # EASY, NORMAL, HARD
        self.game_speed = 8
        self.move_counter = 0
        self.special_effect = None
        self.special_effect_timer = 0
        
    def start_game(self):
        self.snake.reset()
        self.food.randomize_position(self.snake.positions)
        
        # Настройка сложности
        if self.difficulty == "EASY":
            self.game_speed = 6
        elif self.difficulty == "NORMAL":
            self.game_speed = 8
        elif self.difficulty == "HARD":
            self.game_speed = 12
            
        self.game_state = "PLAYING"
        self.special_effect = None
        self.special_effect_timer = 0
        
    def handle_input(self, event):
        if self.game_state == "PLAYING":
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    self.snake.update_direction(UP)
                elif event.key == K_DOWN:
                    self.snake.update_direction(DOWN)
                elif event.key == K_LEFT:
                    self.snake.update_direction(LEFT)
                elif event.key == K_RIGHT:
                    self.snake.update_direction(RIGHT)
                elif event.key == K_ESCAPE:
                    self.game_state = "MENU"
        elif self.game_state == "GAME_OVER":
            if event.type == KEYDOWN and event.key == K_SPACE:
                self.game_state = "MENU"
                
    def update(self):
        if self.game_state == "PLAYING":
            # Обновление эффектов
            self.snake.update_effects()
            
            if self.special_effect == "slow_time":
                self.special_effect_timer -= 1
                if self.special_effect_timer <= 0:
                    self.special_effect = None
                    self.snake.slow_time_factor = 1.0
                    
            # Движение змеи
            self.move_counter += 1
            move_interval = max(1, int(self.game_speed * self.snake.slow_time_factor))
            
            if self.move_counter >= move_interval:
                if not self.snake.move():
                    self.game_state = "GAME_OVER"
                self.move_counter = 0
                
                # Проверка поедания еды
                head = self.snake.get_head_position()
                if head == self.food.position:
                    # Анимация поедания
                    self.food.start_eaten_animation()
                    
                    # Обычная еда
                    if not self.food.is_bonus:
                        self.snake.grow()
                        self.snake.score += 10
                    # Бонус-еда
                    else:
                        self.apply_bonus_effect(self.food.bonus_type)
                        self.snake.score += 30
                    
                    # Создаем новую еду
                    self.food.randomize_position(self.snake.positions)
                    
    def apply_bonus_effect(self, effect_type):
        if effect_type == "slow_time":
            self.special_effect = "slow_time"
            self.special_effect_timer = 150  # ~5 секунд при 30 FPS
            self.snake.slow_time_factor = 0.5  # Замедление времени в 2 раза
        elif effect_type == "speed_boost":
            self.snake.speed = 15  # Ускорение
            self.snake.speed_boost_timer = 300  # ~10 секунд
        elif effect_type == "teleport":
            # Телепортируем змейку в случайное место
            head_x, head_y = self.snake.positions[0]
            new_x = random.randint(0, GRID_WIDTH - 1)
            new_y = random.randint(0, GRID_HEIGHT - 1)
            
            # Перемещаем всю змейку
            delta_x = new_x - head_x
            delta_y = new_y - head_y
            new_positions = []
            for x, y in self.snake.positions:
                new_x = (x + delta_x) % GRID_WIDTH
                new_y = (y + delta_y) % GRID_HEIGHT
                new_positions.append((new_x, new_y))
            self.snake.positions = new_positions
    
    def draw_grid(self, surface):
        # Заполнение фона
        surface.fill(BACKGROUND)
        
        # Рисование сетки
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(surface, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))
            
    def draw_ui(self, surface):
        # Панель счета
        score_surface = pygame.Surface((SCREEN_WIDTH, 40), pygame.SRCALPHA)
        score_surface.fill(UI_BG)
        pygame.draw.rect(score_surface, UI_BORDER, (0, 0, SCREEN_WIDTH, 40), 2)
        
        score_text = font_small.render(f"Очки: {self.snake.score}", True, TEXT_COLOR)
        score_surface.blit(score_text, (20, 10))
        
        # Индикатор эффекта
        if self.special_effect:
            effect_text = font_small.render(f"Эффект: {self.get_effect_name()}", True, TEXT_COLOR)
            score_surface.blit(effect_text, (SCREEN_WIDTH - 200, 10))
            
        surface.blit(score_surface, (0, 0))
        
    def get_effect_name(self):
        if self.special_effect == "slow_time":
            return "Замедление времени"
        elif self.snake.speed_boost_timer > 0:
            return "Ускорение змейки"
        return ""
        
    def draw(self, surface):
        # Рисуем сетку
        self.draw_grid(surface)
        
        # Рисуем змейку
        self.snake.draw(surface)
        
        # Рисуем еду
        self.food.draw(surface)
        
        # Рисуем UI
        self.draw_ui(surface)
        
        # Сообщения для разных состояний игры
        if self.game_state == "MENU":
            self.draw_menu(surface)
        elif self.game_state == "GAME_OVER":
            self.draw_game_over(surface)
            
    def draw_menu(self, surface):
        # Затемнение фона
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))
        
        # Заголовок
        title = font_large.render("ЗМЕЙКА С БОНУСАМИ", True, TEXT_COLOR)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        surface.blit(title, title_rect)
        
        # Кнопки сложности
        difficulties = ["EASY", "NORMAL", "HARD"]
        button_height = 50
        button_width = 200
        button_spacing = 20
        
        for i, diff in enumerate(difficulties):
            button_color = (70, 130, 70) if diff == self.difficulty else (50, 100, 50)
            button_rect = pygame.Rect(
                SCREEN_WIDTH // 2 - button_width // 2,
                SCREEN_HEIGHT // 2 + i * (button_height + button_spacing),
                button_width,
                button_height
            )
            
            pygame.draw.rect(surface, button_color, button_rect)
            pygame.draw.rect(surface, (100, 170, 100), button_rect, 3)
            
            diff_text = font_medium.render(diff, True, TEXT_COLOR)
            diff_rect = diff_text.get_rect(center=button_rect.center)
            surface.blit(diff_text, diff_rect)
            
            # Обработка кликов
            mouse_pos = pygame.mouse.get_pos()
            if button_rect.collidepoint(mouse_pos):
                pygame.draw.rect(surface, (90, 190, 90), button_rect, 4)
                for event in pygame.event.get():
                    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                        self.difficulty = diff
                        self.start_game()
        
        # Инструкция
        instruction = font_small.render("Нажмите на уровень сложности, чтобы начать", True, TEXT_COLOR)
        instruction_rect = instruction.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4))
        surface.blit(instruction, instruction_rect)
        
    def draw_game_over(self, surface):
        # Затемнение фона
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))
        
        # Заголовок
        title = font_large.render("ИГРА ОКОНЧЕНА", True, (231, 76, 60))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        surface.blit(title, title_rect)
        
        # Счет
        score_text = font_medium.render(f"Ваш счет: {self.snake.score}", True, TEXT_COLOR)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        surface.blit(score_text, score_rect)
        
        # Инструкция
        instruction = font_small.render("Нажмите ПРОБЕЛ для возврата в меню", True, TEXT_COLOR)
        instruction_rect = instruction.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4))
        surface.blit(instruction, instruction_rect)

# Основная функция игры
def main():
    game = Game()
    
    while True:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            game.handle_input(event)
            
        # Обновление игры
        game.update()
        
        # Отрисовка
        game.draw(screen)
        pygame.display.flip()
        
        # Управление FPS
        clock.tick(FPS)

if __name__ == "__main__":
    main()
```

## Особенности реализации:

1. **Сетка игрового поля**: Четкая сетка на фоне создает визуальную структуру
2. **Приятная цветовая гамма**: Зеленая палитра с акцентами для змейки и еды
3. **Многоуровневое меню**: Выбор сложности (легкий, нормальный, сложный)
4. **Анимация поедания еды**: Эффект вспышки при съедании еды
5. **Изюминка - специальные бонусы**:
   - Замедление времени: делает игру медленнее на 5 секунд
   - Ускорение змейки: повышает скорость передвижения
   - Телепорт: перемещает змейку в случайную точку поля

## Как играть:
- В меню выберите уровень сложности
- Управляйте змейкой стрелками
- Собирайте обычную еду (красные квадраты) и бонусы (цветные квадраты)
- Избегайте столкновений с самой собой
- Для перезапуска после проигрыша нажмите ПРОБЕЛ

Для запуска игры установите библиотеку Pygame:
```
pip install pygame
```

Запустите файл с игрой и наслаждайтесь!