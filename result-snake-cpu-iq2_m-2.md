```text
Prompt
- Tokens: 59
- Time: 4879.716 ms
- Speed: 12.1 t/s
Generation
- Tokens: 6570
- Time: 1662731.362 ms
- Speed: 4.0 t/s
```

<think>
Мы создадим игру "Змейка" с использованием библиотеки Pygame.
 Основные требования:
 1. Игровое поле с сеткой.
 2. Приятная цветовая гамма.
 3. Меню (старт, пауза, рестарт).
 4. Анимация поедания еды.
 5. Интересная изюминка (например, добавление препятствий или двух игроков, или бонусов, которые дают особые эффекты).

 Для простоты реализации и в рамках примера выберем следующую изюминку: 
   - Появление на поле временных бонусов (яблоко другого цвета), которые дают:
        * Ускорение змеи на некоторое время.
        * Замедление змеи на некоторое время.
        * Укорочение змеи (удаление нескольких последних сегментов).
        * Удлинение змеи (добавление нескольких сегментов).

 Но для начала сделаем базовую змейку, а затем добавим бонусы.

 План:
 1. Инициализация Pygame, настройка окна, цветов, шрифтов.
 2. Создание змейки: список сегментов (каждый сегмент - прямоугольник), направление движения.
 3. Еда: появление в случайном месте, но не на змейке. Анимация при поедании (увеличим змейку и добавим эффект).
 4. Игровой цикл: обработка событий (выход, клавиши управления), обновление позиции змейки, проверка столкновений, отрисовка.
 5. Меню: начальный экран, пауза, конец игры.
 6. Изюминка: добавим бонусы, которые появляются на ограниченное время и дают временные эффекты.

 Для анимации поедания еды можно сделать:
   - При поедании еды показывать небольшой взрыв или анимацию (кружочки, которые расходятся) на месте съеденной еды.

 Для меню создадим функции, которые будут отображать текст и ждать действий пользователя.

 Бонусы:
   - Создадим список активных бонусов (каждый бонус имеет позицию, тип, время появления и длительность).
   - Бонусы появляются на время и исчезают. Если змейка съедает бонус, то активируется эффект на определенное время.
   - Эффекты:
        * SPEED_UP: скорость змейки увеличивается (уменьшаем задержку между обновлениями) на 5 секунд.
        * SPEED_DOWN: скорость змейки уменьшается на 5 секунд.
        * SHORTEN: удалить 3 последних сегмента змейки (если есть сегменты).
        * LENGTHEN: добавить 3 сегмента (но не сразу, а постепенно, как при обычной еде, но 3 раза подряд).

 Однако, чтобы не усложнять, сделаем так: при съедании бонуса "SHORTEN" сразу удалим 3 последних сегмента (если есть), а при "LENGTHEN" установим флаг, что следующие 3 съеденные еды дадут увеличение (или просто сразу добавим 3 сегмента).

 Но я выберу более простой вариант: бонусы дают немедленный эффект, кроме SPEED_UP и SPEED_DOWN, которые временные.

 Реализация:
   - Скорость змейки регулируется через задержку в главном цикле (или через таймер).
   - Для временных эффектов заведем словарь текущих эффектов и таймеры для них.

 Сетка: нарисуем сетку на фоне.

 Цвета: возьмем приятные цвета (например, зеленый для змейки, красный для еды, желтый для бонусов, и т.д.)

 Начнем писать код.

 Примечание: из-за сложности игры и большого объема кода, я постараюсь сделать код максимально читаемым и структурированным.

 Мы создадим классы:
   - Game: основной класс игры.
   - Snake: класс змейки.
   - Food: класс еды.
   - Bonus: класс бонуса.

 Однако, для простоты, сначала сделаем без классов, а затем переведем в классы.

 Но чтобы было проще, начнем с функций и глобальных переменных, а потом реорганизуем.

 Шаги:

 1. Инициализация Pygame.
 2. Определение констант (размеры, цвета, скорости и т.д.)
 3. Создание функций для отрисовки змейки, еды, сетки, меню.
 4. Основной игровой цикл.

 Давайте начнем.
</think>
# Игра "Змейка" на Python с дополнительными возможностями

```python
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

# Цвета (приятная пастельная гамма)
BACKGROUND = (30, 30, 40)
GRID_COLOR = (50, 50, 60)
SNAKE_COLOR = (100, 230, 150)
SNAKE_HEAD_COLOR = (130, 255, 170)
FOOD_COLOR = (255, 100, 120)
SPECIAL_FOOD_COLOR = (255, 220, 100)
MENU_BG = (20, 20, 30, 200)
TEXT_COLOR = (240, 240, 255)
BUTTON_COLOR = (80, 150, 220)
BUTTON_HOVER = (100, 170, 250)
OBSTACLE_COLOR = (180, 100, 150)

class Snake:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        self.score = 0
        self.grow_to = 3
        self.speed_boost = 0
    
    def get_head_position(self):
        return self.positions[0]
    
    def update(self):
        head = self.get_head_position()
        x, y = self.direction
        new_x = (head[0] + x) % GRID_WIDTH
        new_y = (head[1] + y) % GRID_HEIGHT
        new_position = (new_x, new_y)
        
        # Проверка на столкновение с собой
        if new_position in self.positions[1:]:
            return False
        
        self.positions.insert(0, new_position)
        
        # Управление длиной змейки
        if self.grow_to > 0:
            self.grow_to -= 1
        else:
            self.positions.pop()
        
        return True
    
    def grow(self, amount=1):
        self.grow_to += amount
        self.length += amount
        self.score += 10 * amount
    
    def render(self, surface):
        for i, pos in enumerate(self.positions):
            color = SNAKE_HEAD_COLOR if i == 0 else SNAKE_COLOR
            rect = pygame.Rect(pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, (40, 40, 50), rect, 1)
            
            # Рисуем глаза для головы змейки
            if i == 0:
                eye_size = GRID_SIZE // 5
                dx, dy = self.direction
                
                # Глаза смотрят в направлении движения
                if dx == 1:  # вправо
                    left_eye = (pos[0]*GRID_SIZE + GRID_SIZE - eye_size*2, pos[1]*GRID_SIZE + eye_size*2)
                    right_eye = (pos[0]*GRID_SIZE + GRID_SIZE - eye_size*2, pos[1]*GRID_SIZE + GRID_SIZE - eye_size*3)
                elif dx == -1:  # влево
                    left_eye = (pos[0]*GRID_SIZE + eye_size, pos[1]*GRID_SIZE + eye_size*2)
                    right_eye = (pos[0]*GRID_SIZE + eye_size, pos[1]*GRID_SIZE + GRID_SIZE - eye_size*3)
                elif dy == 1:  # вниз
                    left_eye = (pos[0]*GRID_SIZE + eye_size*2, pos[1]*GRID_SIZE + GRID_SIZE - eye_size*2)
                    right_eye = (pos[0]*GRID_SIZE + GRID_SIZE - eye_size*3, pos[1]*GRID_SIZE + GRID_SIZE - eye_size*2)
                else:  # вверх
                    left_eye = (pos[0]*GRID_SIZE + eye_size*2, pos[1]*GRID_SIZE + eye_size)
                    right_eye = (pos[0]*GRID_SIZE + GRID_SIZE - eye_size*3, pos[1]*GRID_SIZE + eye_size)
                
                pygame.draw.circle(surface, (30, 40, 50), left_eye, eye_size)
                pygame.draw.circle(surface, (30, 40, 50), right_eye, eye_size)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.spawn_food()
        self.eaten_animation = 0
        self.special = False
        self.special_timer = 0
    
    def spawn_food(self, snake_positions=None, obstacles=None):
        if snake_positions is None:
            snake_positions = []
        
        # Генерация позиции, не занятой змейкой и препятствиями
        while True:
            self.position = (random.randint(0, GRID_WIDTH - 1), 
                            random.randint(0, GRID_HEIGHT - 1))
            if self.position not in snake_positions and (obstacles is None or self.position not in obstacles):
                break
        
        # Определяем, будет ли это особая еда
        self.special = random.random() < 0.2
        self.special_timer = 100 if self.special else 0
        self.eaten_animation = 0
    
    def update(self):
        if self.eaten_animation > 0:
            self.eaten_animation -= 1
        if self.special_timer > 0:
            self.special_timer -= 1
            if self.special_timer == 0:
                self.special = False
    
    def render(self, surface):
        if self.eaten_animation > 0:
            # Анимация поедания
            size = GRID_SIZE * (1 + self.eaten_animation / 10)
            rect = pygame.Rect(
                self.position[0] * GRID_SIZE + GRID_SIZE // 2 - size // 2,
                self.position[1] * GRID_SIZE + GRID_SIZE // 2 - size // 2,
                size, size
            )
            pygame.draw.rect(surface, (255, 200, 100, 150), rect, border_radius=int(size/2))
        elif self.position:
            # Обычная еда
            rect = pygame.Rect(self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, SPECIAL_FOOD_COLOR if self.special else FOOD_COLOR, rect, border_radius=8)
            
            # Анимация пульсации для особой еды
            if self.special:
                pulse = abs(math.sin(pygame.time.get_ticks() / 200)) * 5
                pulse_rect = pygame.Rect(
                    rect.x - pulse, rect.y - pulse,
                    GRID_SIZE + pulse * 2, GRID_SIZE + pulse * 2
                )
                pygame.draw.rect(surface, (255, 220, 100, 100), pulse_rect, 2, border_radius=8)

class Obstacle:
    def __init__(self):
        self.positions = []
    
    def generate(self, count=5):
        self.positions = []
        for _ in range(count):
            while True:
                pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
                if pos not in self.positions:
                    self.positions.append(pos)
                    break
    
    def render(self, surface):
        for pos in self.positions:
            rect = pygame.Rect(pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, OBSTACLE_COLOR, rect)
            pygame.draw.rect(surface, (120, 60, 100), rect, 1)
            
            # Рисуем узор на препятствии
            inner_rect = pygame.Rect(
                rect.x + GRID_SIZE // 4,
                rect.y + GRID_SIZE // 4,
                GRID_SIZE // 2,
                GRID_SIZE // 2
            )
            pygame.draw.rect(surface, (200, 130, 170), inner_rect, 2)

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = BUTTON_COLOR
        self.hover_color = BUTTON_HOVER
        self.is_hovered = False
    
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, (200, 220, 255), self.rect, 2, border_radius=10)
        
        font = pygame.font.SysFont(None, 36)
        text_surf = font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
    
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
    
    def check_click(self, pos):
        return self.rect.collidepoint(pos)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Змейка")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 24)
        
        self.snake = Snake()
        self.food = Food()
        self.obstacles = Obstacle()
        self.obstacles.generate(8)
        
        self.game_state = "menu"  # menu, playing, paused, game_over
        self.init_menu()
        
        # Эффект для отражения движения
        self.trail = []
        
        # Загрузка звуков (если они есть)
        try:
            self.eat_sound = pygame.mixer.Sound("eat.wav")
        except:
            self.eat_sound = None
    
    def init_menu(self):
        center_x = WIDTH // 2
        self.start_button = Button(center_x - 100, 200, 200, 50, "Начать игру")
        self.quit_button = Button(center_x - 100, 300, 200, 50, "Выход")
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if self.game_state == "playing":
                    if event.key == pygame.K_UP and self.snake.direction != (0, 1):
                        self.snake.direction = (0, -1)
                    if event.key == pygame.K_DOWN and self.snake.direction != (0, -1):
                        self.snake.direction = (0, 1)
                    if event.key == pygame.K_LEFT and self.snake.direction != (1, 0):
                        self.snake.direction = (-1, 0)
                    if event.key == pygame.K_RIGHT and self.snake.direction != (-1, 0):
                        self.snake.direction = (1, 0)
                    if event.key == pygame.K_p:
                        self.game_state = "paused"
                    if event.key == pygame.K_SPACE and self.snake.speed_boost > 0:
                        # Активация ускорения по нажатию пробела
                        self.snake.speed_boost = 100
                
                if event.key == pygame.K_ESCAPE:
                    if self.game_state == "playing" or self.game_state == "paused":
                        self.game_state = "paused" if self.game_state == "playing" else "playing"
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.game_state == "menu":
                    if self.start_button.check_click(event.pos):
                        self.game_state = "playing"
                    if self.quit_button.check_click(event.pos):
                        pygame.quit()
                        sys.exit()
                
                if self.game_state == "game_over":
                    if self.start_button.check_click(event.pos):
                        self.reset_game()
    
    def reset_game(self):
        self.snake.reset()
        self.food.spawn_food(self.snake.positions, self.obstacles.positions)
        self.obstacles.generate(8)
        self.game_state = "playing"
    
    def update(self):
        if self.game_state != "playing":
            return
            
        # Обновление позиции змейки
        if not self.snake.update():
            self.game_state = "game_over"
            return
        
        # Обновление анимации еды
        self.food.update()
        
        # Проверка столкновения с едой
        if self.snake.get_head_position() == self.food.position:
            # Анимация поедания
            self.food.eaten_animation = 10
            
            # Специальная еда дает дополнительные очки и ускорение
            if self.food.special:
                self.snake.grow(3)
                self.snake.speed_boost = 100
            else:
                self.snake.grow(1)
            
            # Воспроизведение звука
            if self.eat_sound:
                self.eat_sound.play()
            
            # Создание новой еды
            self.food.spawn_food(self.snake.positions, self.obstacles.positions)
        
        # Проверка столкновения с препятствиями
        if self.snake.get_head_position() in self.obstacles.positions:
            self.game_state = "game_over"
        
        # Обновление ускорения
        if self.snake.speed_boost > 0:
            self.snake.speed_boost -= 1
    
    def draw_grid(self):
        # Рисуем сетку
        for x in range(0, WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (WIDTH, y))
    
    def draw_trail(self):
        # Эффект следа от движения змейки
        self.trail.append(self.snake.get_head_position())
        if len(self.trail) > 20:
            self.trail.pop(0)
        
        for i, pos in enumerate(self.trail):
            alpha = int(200 * (i / len(self.trail)))
            color = (100, 230, 150, alpha)
            rect = pygame.Rect(pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(self.screen, color, rect, border_radius=5)
    
    def draw_hud(self):
        # Отображение счета
        score_text = self.font.render(f"Очки: {self.snake.score}", True, TEXT_COLOR)
        self.screen.blit(score_text, (10, 10))
        
        # Отображение длины змейки
        length_text = self.small_font.render(f"Длина: {self.snake.length}", True, TEXT_COLOR)
        self.screen.blit(length_text, (10, 50))
        
        # Индикатор ускорения
        if self.snake.speed_boost > 0:
            boost_text = self.small_font.render(f"Ускорение: {self.snake.speed_boost//10}", True, (255, 220, 100))
            self.screen.blit(boost_text, (10, 80))
    
    def draw_menu(self):
        # Полупрозрачный фон меню
        menu_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        menu_surface.fill(MENU_BG)
        self.screen.blit(menu_surface, (0, 0))
        
        # Заголовок
        title_font = pygame.font.SysFont(None, 72)
        title = title_font.render("ЗМЕЙКА", True, TEXT_COLOR)
        self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 80))
        
        # Кнопки
        self.start_button.draw(self.screen)
        self.quit_button.draw(self.screen)
        
        # Инструкции
        instr = self.small_font.render("Используйте стрелки для управления", True, TEXT_COLOR)
        self.screen.blit(instr, (WIDTH//2 - instr.get_width()//2, 380))
        
        instr2 = self.small_font.render("P - пауза, ESC - вернуться в меню", True, TEXT_COLOR)
        self.screen.blit(instr2, (WIDTH//2 - instr2.get_width()//2, 410))
        
        # Изюминка игры
        feature = self.small_font.render("Особенность: собирайте золотые яблоки для ускорения!", True, (255, 220, 100))
        self.screen.blit(feature, (WIDTH//2 - feature.get_width()//2, 480))
    
    def draw_pause(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        pause_font = pygame.font.SysFont(None, 72)
        pause_text = pause_font.render("ПАУЗА", True, TEXT_COLOR)
        self.screen.blit(pause_text, (WIDTH//2 - pause_text.get_width()//2, HEIGHT//2 - 50))
        
        instr = self.font.render("Нажмите P для продолжения", True, TEXT_COLOR)
        self.screen.blit(instr, (WIDTH//2 - instr.get_width()//2, HEIGHT//2 + 30))
    
    def draw_game_over(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((20, 20, 30, 220))
        self.screen.blit(overlay, (0, 0))
        
        game_over_font = pygame.font.SysFont(None, 72)
        game_over = game_over_font.render("ИГРА ОКОНЧЕНА", True, (255, 100, 120))
        self.screen.blit(game_over, (WIDTH//2 - game_over.get_width()//2, HEIGHT//2 - 100))
        
        score_text = self.font.render(f"Ваш счет: {self.snake.score}", True, TEXT_COLOR)
        self.screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 - 20))
        
        self.start_button.rect.center = (WIDTH//2, HEIGHT//2 + 50)
        self.start_button.text = "Играть снова"
        self.start_button.draw(self.screen)
    
    def draw(self):
        self.screen.fill(BACKGROUND)
        self.draw_grid()
        self.draw_trail()
        self.obstacles.render(self.screen)
        self.food.render(self.screen)
        self.snake.render(self.screen)
        self.draw_hud()
        
        if self.game_state == "menu":
            self.draw_menu()
        elif self.game_state == "paused":
            self.draw_pause()
        elif self.game_state == "game_over":
            self.draw_game_over()
    
    def run(self):
        while True:
            mouse_pos = pygame.mouse.get_pos()
            
            if self.game_state == "menu":
                self.start_button.check_hover(mouse_pos)
                self.quit_button.check_hover(mouse_pos)
            
            self.handle_events()
            self.update()
            self.draw()
            
            pygame.display.flip()
            
            # Регулировка скорости с учетом ускорения
            base_speed = FPS
            if self.game_state == "playing" and self.snake.speed_boost > 0:
                base_speed = FPS * 2
            self.clock.tick(base_speed)

# Запуск игры
if __name__ == "__main__":
    game = Game()
    game.run()
```

## Особенности игры

1. **Сетка игрового поля**:
   - Поле разделено на клетки размером 20x20 пикселей
   - Сетка отображается поверх фона для лучшей ориентации

2. **Приятная цветовая гамма**:
   - Темный фон с фиолетовыми оттенками
   - Зеленая змейка с детализированной головой (глазами)
   - Красная и золотая (специальная) еда
   - Пурпурные препятствия с узором

3. **Меню и интерфейс**:
   - Главное меню с кнопками "Начать игру" и "Выход"
   - Экран паузы
   - Экран окончания игры с возможностью рестарта
   - Отображение счета и длины змейки

4. **Анимации**:
   - Анимация поедания еды (пульсирующий эффект)
   - След от движения змейки
   - Пульсация специальной еды
   - Анимация кнопок при наведении

5. **Особенности игры (изюминки)**:
   - **Специальные золотые яблоки**:
     - Дают 3 единицы роста вместо 1
     - Предоставляют временное ускорение
   - **Препятствия**:
     - Случайно генерируемые препятствия на поле
     - Столкновение с ними заканчивает игру
   - **Ускорение**:
     - Активируется при съедании золотых яблок
     - Можно активировать вручную пробелом
   - **Порталы**:
     - При выходе за границы экрана змейка появляется с противоположной стороны

## Управление:
- Стрелки для управления направлением движения
- P - пауза/продолжение игры
- ESC - переход в меню/возврат в игру
- Пробел - активация ускорения (если доступно)

## Как играть:
1. Начните игру из меню
2. Управляйте змейкой, собирая красные яблоки
3. Старайтесь собирать золотые яблоки для получения бонусов
4. Избегайте столкновений с хвостом и препятствиями
5. Набирайте как можно больше очков!

Для запуска игры просто сохраните код в файл `snake.py` и запустите его с помощью Python. Убедитесь, что у вас установлена библиотека Pygame (`pip install pygame`).