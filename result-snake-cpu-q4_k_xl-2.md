```text
Prompt
- Tokens: 59
- Time: 3168.597 ms
- Speed: 18.6 t/s
Generation
- Tokens: 8609
- Time: 2999169.067 ms
- Speed: 2.9 t/s
```

<think>
Мы создадим игру "Змейка" с использованием библиотеки Pygame.
 У нас будет:
   - Сетка игрового поля.
   - Приятная цветовая гамма.
   - Меню (начальное меню с кнопками "Старт" и "Выход").
   - Анимация поедания еды (например, увеличение змейки с эффектом).
   - Изюминка: добавим два типа еды:
        * Обычная еда (зеленое яблоко) - добавляет 1 сегмент.
        * Золотое яблоко (появляется реже) - добавляет 3 сегмента, но также ускоряет змейку немного.

 План:
   1. Инициализация Pygame, настройка размеров окна, цветов.
   2. Классы: Змейка, Еда (Food, GoldenFood).
   3. Основной игровой цикл и меню.
   4. Обработка ввода (движение змейки, пауза, выход).
   5. Отображение счета.
   6. Коллизии: со стенами, с собой.
   7. Меню: с кнопками "Start" и "Quit".

 Для анимации поедания: можно сделать эффект вспышки или увеличение головы.

 Реализуем:
   - Игровое поле с сеткой.
   - Змейка как список сегментов (координат).
   - Управление: стрелки.

 Дополнительно:
   - Счетчик очков.
   - При поедании еды: змейка растет, новая еда появляется в случайном месте.
   - Золотое яблоко исчезает через некоторое время, если не съедено.

 Шаги:

   a) Настройки:
        WIDTH, HEIGHT: размер окна (например, 800x600)
        GRID_SIZE: размер клетки (20 пикселей)

   b) Класс Snake:
        body: список координат [ (x0,y0), (x1,y1), ... ]
        direction: текущее направление (UP, DOWN, LEFT, RIGHT)
        move(): перемещение змейки (добавляем новую голову в направлении direction, удаляем хвост если не съели еду)
        grow(): увеличение змейки (не удаляем хвост в move)

   c) Класс Food (и GoldenFood):
        position: (x, y)
        draw(): отрисовка

   d) Функция меню:
        Отображаем заголовок, две кнопки: "Start" и "Quit".
        Обработка кликов мыши.

   e) Основной цикл игры:
        while running:
            обработка событий
            обновление состояний (движение змейки, проверка коллизий)
            отрисовка

   f) Эффект поедания еды:
        При съедании обычной еды: змейка растет на 1, эффект можно показать, сделав мигание еды перед исчезновением (или анимацию появления нового сегмента).
        Для золотой еды: рост на 3, и увеличение скорости (уменьшение задержки между кадрами).

   g) Изюминка: золотая еда, которая дает больше очков и ускоряет игру.

   h) Также добавим звуки? (по желанию, но в условии не было, поэтому без звуков)

   i) Сетка: рисуем горизонтальные и вертикальные линии с шагом GRID_SIZE.

   j) Цвета:
        Змейка: темно-зеленый (#2E8B57) и для головы немного темнее (#1F5E3B)
        Обычная еда: красный (#FF0000) или зеленое яблоко? Пусть будет зеленое (#00FF00) для обычной, и золотое (#FFD700) для золотой.
        Фон: светло-серый (#F0F0F0) или бежевый (#F5F5DC)
        Сетка: светло-серая (#D3D3D3)

   k) Меню: фон, кнопки с подсветкой при наведении.

   l) Также нужно отображать счет.

   m) Скорость игры: 
        Обычная скорость: FPS = 10, но будем использовать clock.tick(10)
        При съедании золотого яблока: увеличим скорость (FPS = 15) на некоторое время? Или навсегда? 
        Пусть ускорение будет временным (например, на 5 секунд). Или можно просто увеличить скорость на 5% за каждое золотое яблоко, но с ограничением.

   n) Золотая еда должна появляться реже. Мы будем генерировать случайно: 
        Обычная еда появляется всегда, когда съедена.
        Золотая еда появляется с вероятностью 1/10.

   o) Золотая еда должна исчезать, если ее не съели через 5 секунд? Тогда нам нужно хранить время появления.

   p) Реализуем временное ускорение от золотой еды: после съедания золотой еды, скорость увеличивается (например, FPS=15) на 10 секунд, затем возвращается обратно.

   q) Также для анимации поедания: при съедании еды, нарисуем на месте еды кружок, который увеличивается (эффект взрыва) и исчезает.

   Но для простоты анимации мы можем сделать:
        При съедании еды, нарисовать несколько кадров: круги разного размера с изменяющейся прозрачностью.

   Однако, чтобы не усложнять, сделаем просто мигание (изменение цвета) головы змейки при съедании.

   r) Создадим класс Game, который будет управлять состоянием игры.

   s) Состояния игры: меню, игра, конец игры.

   t) При конце игры: выводим сообщение "Game Over", счет и кнопку "Play Again" и "Menu".

   u) Реализуем паузу: по нажатию пробела.

   v) Изюминка: два типа еды и временное ускорение.

   w) Для меню используем простой цикл с рисованием кнопок.

   x) Для удобства, создадим класс Button.

   y) Для анимации поедания: будем хранить список эффектов (кортежи: позиция, время начала анимации, тип анимации). 
        В нашем случае, при съедании еды, создадим эффект (кружок) на месте еды, который будет расширяться и исчезать.
        Для этого будем обновлять и рисовать эффекты в основном цикле.

   z) Эффект: 
        class ParticleEffect:
            def __init__(self, pos, effect_type):
                self.pos = pos
                self.start_time = текущее время
                self.duration = 0.5  # секунды
                self.radius = 0
                self.max_radius = GRID_SIZE * 1.5

            def update(self, current_time):
                # увеличиваем радиус со временем
                elapsed = current_time - self.start_time
                if elapsed > self.duration:
                    return False  # эффект закончился
                progress = elapsed / self.duration
                self.radius = progress * self.max_radius
                return True

            def draw(self, screen):
                # рисуем круг с прозрачностью
                alpha = 255 * (1 - (self.radius / self.max_radius))
                color = (255, 215, 0, int(alpha)) if self.effect_type == 'gold' else (0, 255, 0, int(alpha))
                # ... рисуем круг с радиусом self.radius в позиции self.pos

   Но в Pygame рисуем без прозрачности для простоты? Или используем Surface с альфа-каналом.

   Однако для простоты, мы не будем делать прозрачность, а просто изменим цвет и будем рисовать круги с увеличением радиуса.

   Но это требует дополнительной работы. Возможно, на данном этапе мы ограничимся миганием головы змейки.

   При съедании еды мы можем на несколько кадров изменить цвет головы змейки (например, на желтый) и вернуть обратно.

   Решим сделать простое изменение цвета головы при съедании еды (на 5 кадров).

   Другой вариант: при съедании еды, рисуем на месте еды кружок, который быстро растет и исчезает. Это будет проще, потому что не привязано к змейке.

   Давайте сделаем так:
        При съедании еды, создадим объект анимации (пусть это будет кружок), который увеличивается и исчезает. 
        Мы можем хранить список активных анимаций.

   Создадим класс EatingAnimation:
        def __init__(self, position, color, current_time):
            self.position = position
            self.start_time = current_time
            self.duration = 0.3  # секунды
            self.radius = 0
            self.max_radius = GRID_SIZE * 1.5
            self.color = color

        def update(self, current_time):
            elapsed = current_time - self.start_time
            if elapsed > self.duration:
                return False
            progress = elapsed / self.duration
            self.radius = progress * self.max_radius
            return True

        def draw(self, screen):
            # Рисуем кружок с цветом и радиусом self.radius
            center = (self.position[0] + GRID_SIZE//2, self.position[1] + GRID_SIZE//2)
            pygame.draw.circle(screen, self.color, center, int(self.radius))

   В основном цикле, в части отрисовки, будем рисовать все активные анимации.

   Для этого в игровом состоянии будем хранить список активных анимаций и обновлять их каждую итерацию.

   При съедании еды создадим анимацию с цветом еды.

   Так как у нас два типа еды, то цвет для обычной еды - зеленый, для золотой - золотой.

   Таким образом, мы реализуем анимацию поедания.

   С учетом времени, мы будем использовать pygame.time.get_ticks() для получения текущего времени в миллисекундах.

   Также для управления игровым состоянием (меню, игра, гейм овер) будем использовать переменную game_state.

   Разобьем код на функции и классы.

   Из-за ограниченности времени, сделаем без ООП в глобальном масштабе, но с некоторыми классами.

   Полный код:

   Шаг за шагом:

   Импортируем pygame и sys, random.
</think>
# Игра "Змейка" с улучшенной графикой и уникальными особенностями

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

# Цветовая палитра
BACKGROUND = (15, 20, 25)
GRID_COLOR = (30, 35, 40)
SNAKE_HEAD_COLOR = (46, 204, 113)
SNAKE_BODY_COLOR = (39, 174, 96)
FOOD_COLOR = (231, 76, 60)
GOLDEN_FOOD_COLOR = (241, 196, 15)
TEXT_COLOR = (236, 240, 241)
BUTTON_COLOR = (52, 152, 219)
BUTTON_HOVER_COLOR = (41, 128, 185)
WALL_COLOR = (52, 73, 94)

# Настройка экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка с изюминкой")
clock = pygame.time.Clock()

# Шрифты
title_font = pygame.font.SysFont("Arial", 50, bold=True)
font = pygame.font.SysFont("Arial", 30)
small_font = pygame.font.SysFont("Arial", 24)

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.is_hovered = False
        
    def draw(self, surface):
        color = BUTTON_HOVER_COLOR if self.is_hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, TEXT_COLOR, self.rect, 2, border_radius=10)
        
        text_surf = font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(3, 8)
        self.speed_x = random.uniform(-2, 2)
        self.speed_y = random.uniform(-2, 2)
        self.life = 30
        
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.life -= 1
        self.size = max(0, self.size - 0.1)
        
    def draw(self, surface):
        alpha = min(255, self.life * 8)
        color = (*self.color, alpha)
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), int(self.size))
        
    def is_dead(self):
        return self.life <= 0

class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        self.score = 0
        self.grow_pending = 2  # Начинаем с длины 3
        self.speed_boost = 0
        self.invincible = 0
        self.particles = []
        
    def get_head_position(self):
        return self.positions[0]
    
    def update(self):
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_x = (head_x + dir_x) % GRID_WIDTH
        new_y = (head_y + dir_y) % GRID_HEIGHT
        
        # Проверка столкновения с собой (если не бессмертен)
        if not self.invincible and (new_x, new_y) in self.positions[1:]:
            return False  # Игра окончена
            
        # Добавление новой головы
        self.positions.insert(0, (new_x, new_y))
        
        # Уменьшение буфера роста
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.positions.pop()
            
        # Обновление частиц
        for particle in self.particles[:]:
            particle.update()
            if particle.is_dead():
                self.particles.remove(particle)
                
        # Обновление спецэффектов
        if self.speed_boost > 0:
            self.speed_boost -= 1
        if self.invincible > 0:
            self.invincible -= 1
            
        return True
    
    def draw(self, surface):
        for i, (x, y) in enumerate(self.positions):
            # Рисуем голову другим цветом
            if i == 0:
                color = (52, 152, 219) if self.invincible > 0 else SNAKE_HEAD_COLOR
            else:
                # Плавный переход цвета для тела
                ratio = i / len(self.positions)
                r = int(SNAKE_BODY_COLOR[0] * (1 - ratio) + 39 * ratio)
                g = int(SNAKE_BODY_COLOR[1] * (1 - ratio) + 174 * ratio)
                b = int(SNAKE_BODY_COLOR[2] * (1 - ratio) + 96 * ratio)
                color = (r, g, b)
                
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, color, rect, border_radius=8)
            
            if i == 0:
                # Глаза змейки
                eye_size = GRID_SIZE // 5
                # Направление взгляда
                dx, dy = self.direction
                offset_x = 0 if dx == 0 else GRID_SIZE//3 * (1 if dx > 0 else -1)
                offset_y = 0 if dy == 0 else GRID_SIZE//3 * (1 if dy > 0 else -1)
                
                left_eye = (x * GRID_SIZE + GRID_SIZE//3 + offset_x, y * GRID_SIZE + GRID_SIZE//3 + offset_y)
                right_eye = (x * GRID_SIZE + 2*GRID_SIZE//3 + offset_x, y * GRID_SIZE + GRID_SIZE//3 + offset_y)
                pygame.draw.circle(surface, (0, 0, 0), left_eye, eye_size)
                pygame.draw.circle(surface, (0, 0, 0), right_eye, eye_size)
                
        # Рисуем частицы
        for particle in self.particles:
            particle.draw(surface)
    
    def change_direction(self, direction):
        # Предотвращение разворота на 180 градусов
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction
    
    def grow(self, amount=1):
        self.grow_pending += amount
        self.score += amount
        
    def create_particles(self, x, y, color, count=15):
        for _ in range(count):
            self.particles.append(Particle(x, y, color))
    
    def add_speed_boost(self):
        self.speed_boost = 100  # 100 кадров ускорения
        
    def activate_invincibility(self):
        self.invincible = 150  # 150 кадров бессмертия

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.is_golden = False
        self.timer = 0
        self.spawn()
        
    def spawn(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        self.is_golden = random.random() < 0.2  # 20% шанс золотой еды
        self.timer = 0
        
    def update(self):
        self.timer += 1
        
    def draw(self, surface):
        x, y = self.position
        rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        
        if self.is_golden:
            # Анимация золотой еды (мерцание)
            alpha = 128 + 127 * math.sin(self.timer * 0.1)
            color = (241, 196, 15, int(alpha))
            
            # Создаем поверхность с альфа-каналом
            s = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
            pygame.draw.circle(s, color, (GRID_SIZE//2, GRID_SIZE//2), GRID_SIZE//2 - 2)
            pygame.draw.circle(s, (255, 223, 0), (GRID_SIZE//2, GRID_SIZE//2), GRID_SIZE//2 - 4)
            
            # Рисуем корону
            crown_points = [
                (GRID_SIZE//2, GRID_SIZE//4),
                (GRID_SIZE//3, GRID_SIZE//2),
                (GRID_SIZE//2, GRID_SIZE//3),
                (2*GRID_SIZE//3, GRID_SIZE//2)
            ]
            pygame.draw.polygon(s, (255, 215, 0), crown_points)
            
            surface.blit(s, rect)
        else:
            color = FOOD_COLOR
            pygame.draw.circle(surface, color, rect.center, GRID_SIZE//2 - 2)
            pygame.draw.circle(surface, (192, 57, 43), rect.center, GRID_SIZE//4)

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.state = "MENU"  # MENU, PLAYING, GAME_OVER
        self.buttons = [
            Button(WIDTH//2 - 100, HEIGHT//2, 200, 50, "Играть"),
            Button(WIDTH//2 - 100, HEIGHT//2 + 70, 200, 50, "Выход")
        ]
        self.walls = self.generate_walls()
        self.game_over_timer = 0
        
    def generate_walls(self):
        walls = []
        # Генерируем случайные стены
        for _ in range(10):
            wall_length = random.randint(3, 8)
            start_x = random.randint(1, GRID_WIDTH - wall_length - 1)
            start_y = random.randint(1, GRID_HEIGHT - 1)
            
            # Вертикально или горизонтально
            if random.choice([True, False]):
                # Горизонтальная стена
                for i in range(wall_length):
                    walls.append((start_x + i, start_y))
            else:
                # Вертикальная стена
                for i in range(wall_length):
                    walls.append((start_x, start_y + i))
        return walls
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if self.state == "MENU":
                mouse_pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    button.check_hover(mouse_pos)
                    if button.is_clicked(mouse_pos, event):
                        if button.text == "Играть":
                            self.state = "PLAYING"
                        elif button.text == "Выход":
                            pygame.quit()
                            sys.exit()
                            
            elif self.state == "PLAYING":
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
                        self.snake.activate_invincibility()
                    elif event.key == pygame.K_p:
                        self.state = "PAUSE"
                        
            elif self.state == "GAME_OVER":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                        
                mouse_pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    button.check_hover(mouse_pos)
                    if button.is_clicked(mouse_pos, event):
                        if button.text == "Играть":
                            self.reset_game()
                        elif button.text == "Выход":
                            pygame.quit()
                            sys.exit()
            
            elif self.state == "PAUSE":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.state = "PLAYING"
    
    def update(self):
        if self.state == "PLAYING":
            # Обновляем змейку
            if not self.snake.update():
                self.state = "GAME_OVER"
                self.game_over_timer = 0
                
            # Проверка столкновения со стенами
            head = self.snake.get_head_position()
            if head in self.walls and not self.snake.invincible:
                self.state = "GAME_OVER"
                self.game_over_timer = 0
                
            # Проверка поедания еды
            if head == self.food.position:
                # Создаем частицы для анимации поедания
                screen_x = head[0] * GRID_SIZE + GRID_SIZE // 2
                screen_y = head[1] * GRID_SIZE + GRID_SIZE // 2
                color = GOLDEN_FOOD_COLOR if self.food.is_golden else FOOD_COLOR
                self.snake.create_particles(screen_x, screen_y, color, 30)
                
                # Золотая еда дает больше очков и бонусы
                if self.food.is_golden:
                    self.snake.grow(3)
                    self.snake.add_speed_boost()
                else:
                    self.snake.grow(1)
                    
                self.food.spawn()
                # Проверяем, чтобы еда не появилась на змейке или стене
                while (self.food.position in self.snake.positions or 
                       self.food.position in self.walls):
                    self.food.spawn()
                    
            # Обновляем еду
            self.food.update()
            
            # Обновляем скорость игры
            global FPS
            base_fps = 10
            if self.snake.speed_boost > 0:
                FPS = base_fps + 5
            else:
                FPS = base_fps
                
        elif self.state == "GAME_OVER":
            self.game_over_timer += 1
    
    def draw_grid(self):
        for x in range(0, WIDTH, GRID_SIZE):
            pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT), 1)
        for y in range(0, HEIGHT, GRID_SIZE):
            pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y), 1)
            
    def draw_walls(self):
        for wall in self.walls:
            x, y = wall
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, WALL_COLOR, rect, border_radius=5)
            pygame.draw.rect(screen, (44, 62, 80), rect, 2, border_radius=5)
    
    def draw_menu(self):
        # Фоновый градиент
        for y in range(HEIGHT):
            color = (15 + y//20, 20 + y//15, 25 + y//10)
            pygame.draw.line(screen, color, (0, y), (WIDTH, y))
            
        # Заголовок с эффектом
        title_text = title_font.render("ИГРА ЗМЕЙКА", True, TEXT_COLOR)
        title_shadow = title_font.render("ИГРА ЗМЕЙКА", True, (46, 204, 113))
        screen.blit(title_shadow, (WIDTH//2 - title_text.get_width()//2 + 3, HEIGHT//4 + 3))
        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//4))
        
        # Подзаголовок
        subtitle = font.render("С изюминкой!", True, (241, 196, 15))
        screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, HEIGHT//4 + 60))
        
        # Рисуем кнопки
        for button in self.buttons:
            button.draw(screen)
            
        # Анимация змейки в меню
        snake_head_x = WIDTH // 2 - 200
        snake_head_y = HEIGHT // 2 + 150
        pygame.draw.circle(screen, SNAKE_HEAD_COLOR, (snake_head_x, snake_head_y), 20)
        
        # Тело змейки (волна)
        for i in range(1, 15):
            offset = math.sin(pygame.time.get_ticks() / 500 + i * 0.5) * 10
            pygame.draw.circle(screen, SNAKE_BODY_COLOR, 
                              (snake_head_x + i * 15, snake_head_y + offset), 
                              15 - i * 0.5)
        
        # Рисуем еду
        pygame.draw.circle(screen, FOOD_COLOR, (WIDTH//2 + 200, HEIGHT//2 + 150), 15)
        pygame.draw.circle(screen, (192, 57, 43), (WIDTH//2 + 200, HEIGHT//2 + 150), 8)
        
        # Золотая еда
        pygame.draw.circle(screen, GOLDEN_FOOD_COLOR, (WIDTH//2 + 250, HEIGHT//2 + 150), 15)
        pygame.draw.circle(screen, (255, 223, 0), (WIDTH//2 + 250, HEIGHT//2 + 150), 8)
        
        # Ключи управления
        controls = [
            "Управление: Стрелки",
            "Пробел: Включить бессмертие (10 сек)",
            "P: Пауза"
        ]
        for i, text in enumerate(controls):
            text_surf = small_font.render(text, True, (200, 200, 200))
            screen.blit(text_surf, (WIDTH//2 - text_surf.get_width()//2, HEIGHT//2 + 200 + i * 30))
    
    def draw_game(self):
        # Рисуем сетку
        self.draw_grid()
        
        # Рисуем стены
        self.draw_walls()
        
        # Рисуем змейку
        self.snake.draw(screen)
        
        # Рисуем еду
        self.food.draw(screen)
        
        # Отображение счета
        score_text = font.render(f"Счет: {self.snake.score}", True, TEXT_COLOR)
        screen.blit(score_text, (10, 10))
        
        # Отображение бонусов
        if self.snake.speed_boost > 0:
            speed_text = font.render("Ускорение!", True, (52, 152, 219))
            screen.blit(speed_text, (WIDTH - speed_text.get_width() - 10, 10))
            
        if self.snake.invincible > 0:
            inv_text = font.render("Бессмертие!", True, (155, 89, 182))
            screen.blit(inv_text, (WIDTH - inv_text.get_width() - 10, 50))
    
    def draw_game_over(self):
        # Затемнение экрана
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        # Анимация "Game Over"
        scale = 1.0 + 0.1 * math.sin(self.game_over_timer * 0.1)
        title = title_font.render("GAME OVER", True, (231, 76, 60))
        title_x = WIDTH//2 - title.get_width()//2
        title_y = HEIGHT//3
        
        # Эффект пульсации
        scaled_title = pygame.transform.scale(title, 
            (int(title.get_width() * scale), int(title.get_height() * scale)))
        screen.blit(scaled_title, 
                   (title_x - (scaled_title.get_width() - title.get_width())//2, 
                    title_y - (scaled_title.get_height() - title.get_height())//2))
        
        # Счет
        score_text = font.render(f"Ваш счет: {self.snake.score}", True, TEXT_COLOR)
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
        
        # Кнопки
        for button in self.buttons:
            button.draw(screen)
        
        # Подсказка
        hint = small_font.render("Нажмите ПРОБЕЛ для новой игры", True, (200, 200, 200))
        screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT - 100))
        
        # Анимация частиц
        if self.game_over_timer % 5 == 0:
            x = random.randint(0, WIDTH)
            self.snake.particles.append(Particle(x, 0, (231, 76, 60)))
    
    def draw_pause(self):
        # Полупрозрачный оверлей
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        
        # Текст паузы
        pause_text = title_font.render("ПАУЗА", True, TEXT_COLOR)
        screen.blit(pause_text, (WIDTH//2 - pause_text.get_width()//2, HEIGHT//3))
        
        # Инструкция
        continue_text = font.render("Нажмите P для продолжения", True, (200, 200, 200))
        screen.blit(continue_text, (WIDTH//2 - continue_text.get_width()//2, HEIGHT//2))
    
    def draw(self):
        screen.fill(BACKGROUND)
        
        if self.state == "MENU":
            self.draw_menu()
        elif self.state == "PLAYING":
            self.draw_game()
        elif self.state == "GAME_OVER":
            self.draw_game()
            self.draw_game_over()
        elif self.state == "PAUSE":
            self.draw_game()
            self.draw_pause()
        
        pygame.display.flip()
    
    def reset_game(self):
        self.snake.reset()
        self.food.spawn()
        self.walls = self.generate_walls()
        # Убеждаемся, что еда не появилась на стене или змейке
        while (self.food.position in self.snake.positions or 
               self.food.position in self.walls):
            self.food.spawn()
    
    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(FPS)

# Запуск игры
if __name__ == "__main__":
    game = Game()
    game.run()
```

## Особенности игры

1. **Приятная цветовая гамма**:
   - Тёмно-синий фон с сеткой
   - Ярко-зелёная змейка с градиентом
   - Контрастные элементы (красная и золотая еда)

2. **Анимация поедания еды**:
   - При поедании появляются частицы цвета съеденной еды
   - Золотая еда мерцает и имеет корону

3. **Меню**:
   - Красивый заголовок с тенями
   - Интерактивные кнопки с эффектом наведения
   - Анимированная змейка и еда в меню

4. **Уникальные особенности (изюминка)**:
   - **Два типа еды**: обычная (красная) и золотая
   - **Бонусы от золотой еды**: 
     - +3 к длине змейки
     - Временное ускорение
   - **Специальная способность**: пробел для активации бессмертия (10 сек)
   - **Стены на игровом поле** - добавляют сложность
   - **Бессмертие при активации**: голова змейки синеет
   - **Сетка и плавная анимация**

5. **Дополнительные функции**:
   - Пауза (клавиша P)
   - Подробная статистика (счёт, активные бонусы)
   - Эффектный экран завершения игры

## Управление
- Стрелки: управление направлением змейки
- Пробел: активировать бессмертие (10 секунд)
- P: пауза/продолжить игру

## Запуск игры
Для запуска игры необходимо установить библиотеку Pygame:
```
pip install pygame
```

Затем запустите скрипт с игрой.