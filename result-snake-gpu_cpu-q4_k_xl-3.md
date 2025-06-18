```text
Prompt
- Tokens: 59
- Time: 29152.87 ms
- Speed: 2.0 t/s
Generation
- Tokens: 6414
- Time: 1094009.594 ms
- Speed: 5.9 t/s
```

<think>
Мы создадим игру "Змейка" с использованием библиотеки Pygame.
 Требования:
   - Сетка на игровом поле.
   - Приятная цветовая гамма.
   - Меню (начало игры, пауза, завершение).
   - Анимация поедания еды (например, эффект при съедании).
   - Интересная изюминка: добавим возможность ускорения змейки при нажатии пробела (или другой ключ) за счет уменьшения длины (жертвуем частью хвоста для ускорения).

 План:
   1. Инициализация Pygame, настройка окна.
   2. Определение цветов.
   3. Создание классов: Змейка, Еда.
   4. Сетка: нарисовать сетку на поле.
   5. Реализация движения змейки.
   6. Столкновения: со стенами, с собой.
   7. Меню: начальное меню, пауза, игра окончена.
   8. Анимация при поедании еды: например, увеличение счетчика с анимацией.
   9. Изюминка: при нажатии пробела змейка ускоряется, но теряет 3 сегмента хвоста (если есть). Если нет хвоста, то ускорение не работает.

 Дополнительно:
   - Счет.
   - Уровни? (можно сделать, но для простоты пока без уровней, но можно увеличивать скорость по мере роста)

 Реализация:

 Шаги кода:

   Импортируем необходимые модули.
   Определяем константы: размер окна, размер блока, скорость и т.д.

   Класс Snake:
        __init__: начальные координаты, направление, тело (список сегментов).
        move: перемещение змейки, добавление головы и удаление хвоста (если не съели еду).
        grow: увеличение длины (добавляем сегмент при съедании еды).
        draw: отрисовка змейки.

   Класс Food:
        __init__: случайные координаты на сетке.
        draw: отрисовка еды.

   Функция draw_grid: рисует сетку.

   Функции меню:
        main_menu: кнопки "Начать игру", "Выход".
        pause_menu: во время паузы.
        game_over_menu: при завершении.

   Основной игровой цикл:
        - Обработка событий (выход, движение змейки, меню).
        - Движение змейки.
        - Проверка столкновений.
        - Проверка съедания еды: если съели, генерируем новую еду, увеличиваем змейку и счет.
        - Отрисовка: сетка, змейка, еда, счет.
        - Реализация изюминки: при нажатии пробела ускоряем змейку (увеличиваем скорость), но удаляем 3 последних сегмента (если длина позволяет). Если длина меньше 4, то ускорение не срабатывает.

   Для анимации поедания: можно сделать, чтобы при съедании еды показывалось какое-то визуальное эффекты (например, круги вокруг еды) или изменение цвета змейки на короткое время.

   Мы сделаем простую анимацию: при съедании еды вокруг головы змейки (или на месте еды) появляется несколько кругов, которые постепенно исчезают.

   Для этого создадим класс анимации (или список активных анимационных эффектов). Каждый эффект будет иметь координаты, размер, и время жизни.

   Реализуем список `effects`. При съедании еды добавляем новый эффект (например, кольца) в список. В цикле отрисовки будем рисовать эти эффекты (с увеличением размера и уменьшением прозрачности) и удалять, когда время истечет.

   Упрощенный вариант: один эффект (круг, который расширяется и исчезает) в месте съеденной еды.

   Создадим класс Effect:
        __init__(self, x, y): 
            self.x = x
            self.y = y
            self.radius = 0
            self.max_radius = 30
            self.growth_speed = 5
            self.active = True

        update(self):
            self.radius += self.growth_speed
            if self.radius > self.max_radius:
                self.active = False

        draw(self, screen):
            alpha = 255 * (1 - self.radius / self.max_radius)
            color = (255, 0, 0, int(alpha)) # красный, но можно изменить
            pygame.draw.circle(screen, color, (self.x, self.y), self.radius, 2)

   Но в Pygame прозрачность рисуется по-другому, поэтому можно создать поверхность с альфа-каналом.

   Однако, чтобы не усложнять, можно сделать просто белый круг с уменьшающейся толщиной и увеличивающимся радиусом.

   Альтернатива: использовать частицы.

   Для простоты мы сделаем эффект из нескольких кругов, которые расходятся и исчезают. Но будем использовать отдельную поверхность для альфа-смешивания.

   Мы создадим список эффектов. При съедании еды добавим один эффект (или несколько?).

   В данном случае, сделаем один эффект "ExpandingCircle".

   Цвета:
        Фон: темно-серый (40, 40, 40)
        Сетка: светло-серый (100, 100, 100)
        Змейка: зеленая (0, 200, 0)
        Голова змейки: ярко-зеленая (0, 255, 0)
        Еда: красная (255, 0, 0)

   Скорость: изначально 10 кадров в секунду (для змейки). Ускорение может увеличивать скорость до 20.

   Структура:
        Инициализация Pygame.
        Определение констант.
        Классы: Snake, Food, ExpandingCircle (для анимации).
        Функции: draw_grid, show_score, меню.

   Основной игровой цикл будет состоять из:
        - Главного меню (начало)
        - Игрового цикла (с паузой)
        - Меню после смерти

   Для управления состояниями (меню, игра, пауза, конец игры) используем переменную `game_state`.

   game_state может быть:
        "menu" - главное меню
        "playing" - игра
        "paused" - пауза
        "game_over" - конец

   Код:

   Примечание: Мы будем использовать фиксированный размер окна и размер блока.

   Размер блока: 20 пикселей.
   Ширина поля в блоках: 30, высота: 20. Тогда размер окна: (600, 400).

   Но чтобы поместить меню и т.д., сделаем окно немного больше? Нет, игровое поле 600x400, а меню будет на весь экран.

   Мы сделаем так: в игровом режиме окно 600x400, а меню тоже в этом окне.

   Реализуем!

   Начнем писать код.
</think>
# Игра "Змейка" на Python

```python
import pygame
import sys
import random
import math

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")

# Цветовая гамма
BACKGROUND = (15, 20, 25)
GRID_COLOR = (30, 35, 45)
SNAKE_HEAD_COLOR = (50, 200, 100)
SNAKE_BODY_COLOR = (40, 180, 90)
FOOD_COLOR = (220, 70, 60)
SPECIAL_FOOD_COLOR = (200, 180, 60)
TEXT_COLOR = (220, 220, 220)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER_COLOR = (90, 150, 200)
UI_BACKGROUND = (25, 30, 40, 200)  # Полупрозрачный

# Настройки игры
FPS = 10
SPEED_BOOST_DURATION = 20  # Длительность ускорения в кадрах

class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([(0, -1), (0, 1), (1, 0), (-1, 0)])
        self.score = 0
        self.speed_boost = 0
        self.grow_to = 3
        
    def get_head_position(self):
        return self.positions[0]
    
    def move(self):
        head = self.get_head_position()
        x, y = self.direction
        new_x = (head[0] + x) % GRID_WIDTH
        new_y = (head[1] + y) % GRID_HEIGHT
        new_position = (new_x, new_y)
        
        # Проверка столкновения с собой
        if new_position in self.positions[1:]:
            return False
        
        self.positions.insert(0, new_position)
        
        if len(self.positions) > self.grow_to:
            self.positions.pop()
            
        if self.speed_boost > 0:
            self.speed_boost -= 1
            
        return True
    
    def grow(self):
        self.grow_to += 1
        self.score += 1
    
    def activate_speed_boost(self):
        self.speed_boost = SPEED_BOOST_DURATION
    
    def draw(self, surface):
        for i, pos in enumerate(self.positions):
            rect = pygame.Rect(pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            
            # Голова змейки
            if i == 0:
                pygame.draw.rect(surface, SNAKE_HEAD_COLOR, rect)
                
                # Глаза змейки
                eye_size = GRID_SIZE // 5
                direction = self.direction
                
                # Левый глаз
                if direction == (1, 0):  # Движение вправо
                    pygame.draw.circle(surface, (255, 255, 255), 
                                     (rect.centerx - GRID_SIZE//4, rect.centery - GRID_SIZE//4), eye_size)
                elif direction == (-1, 0):  # Движение влево
                    pygame.draw.circle(surface, (255, 255, 255), 
                                     (rect.centerx + GRID_SIZE//4, rect.centery - GRID_SIZE//4), eye_size)
                elif direction == (0, 1):  # Движение вниз
                    pygame.draw.circle(surface, (255, 255, 255), 
                                     (rect.centerx - GRID_SIZE//4, rect.centery - GRID_SIZE//4), eye_size)
                else:  # Движение вверх
                    pygame.draw.circle(surface, (255, 255, 255), 
                                     (rect.centerx - GRID_SIZE//4, rect.centery + GRID_SIZE//4), eye_size)
                
                # Правый глаз (противоположный)
                if direction == (1, 0):  # Движение вправо
                    pygame.draw.circle(surface, (255, 255, 255), 
                                     (rect.centerx - GRID_SIZE//4, rect.centery + GRID_SIZE//4), eye_size)
                elif direction == (-1, 0):  # Движение влево
                    pygame.draw.circle(surface, (255, 255, 255), 
                                     (rect.centerx + GRID_SIZE//4, rect.centery + GRID_SIZE//4), eye_size)
                elif direction == (0, 1):  # Движение вниз
                    pygame.draw.circle(surface, (255, 255, 255), 
                                     (rect.centerx + GRID_SIZE//4, rect.centery - GRID_SIZE//4), eye_size)
                else:  # Движение вверх
                    pygame.draw.circle(surface, (255, 255, 255), 
                                     (rect.centerx + GRID_SIZE//4, rect.centery + GRID_SIZE//4), eye_size)
            # Тело змейки
            else:
                pygame.draw.rect(surface, SNAKE_BODY_COLOR, rect)
                # Чешуя на теле
                scale_size = GRID_SIZE // 3
                pygame.draw.rect(surface, (30, 150, 70), 
                                 (pos[0]*GRID_SIZE + scale_size, pos[1]*GRID_SIZE + scale_size, 
                                  scale_size, scale_size))

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = FOOD_COLOR
        self.is_special = False
        self.spawn_time = 0
        self.reset()
    
    def reset(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        # С вероятностью 15% создаем специальную еду
        self.is_special = random.random() < 0.15
        self.color = SPECIAL_FOOD_COLOR if self.is_special else FOOD_COLOR
        self.spawn_time = pygame.time.get_ticks()
        
    def draw(self, surface):
        rect = pygame.Rect(self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, self.color, rect)
        
        # Анимация пульсации
        time = pygame.time.get_ticks() - self.spawn_time
        pulse = abs(math.sin(time * 0.005)) * 0.3 + 0.7
        
        inner_rect = pygame.Rect(
            self.position[0] * GRID_SIZE + GRID_SIZE*(1-pulse)/2,
            self.position[1] * GRID_SIZE + GRID_SIZE*(1-pulse)/2,
            GRID_SIZE * pulse,
            GRID_SIZE * pulse
        )
        
        pygame.draw.rect(surface, (255, 255, 255), inner_rect, 1)

class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.hovered = False
        
    def draw(self, surface):
        color = BUTTON_HOVER_COLOR if self.hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, (150, 200, 255), self.rect, 2, border_radius=10)
        
        font = pygame.font.SysFont(None, 36)
        text_surf = font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.hovered:
            if self.action:
                self.action()
            return True
        return False

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 5)
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(0.5, 2.5)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.lifetime = random.randint(20, 40)
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        self.size = max(0, self.size - 0.1)
        return self.lifetime > 0
        
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size))

def draw_grid(surface):
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (0, y), (WIDTH, y))

def draw_text(surface, text, size, x, y, color=TEXT_COLOR, center=False):
    font = pygame.font.SysFont(None, size)
    text_surf = font.render(text, True, color)
    if center:
        text_rect = text_surf.get_rect(center=(x, y))
    else:
        text_rect = text_surf.get_rect(topleft=(x, y))
    surface.blit(text_surf, text_rect)

def draw_ui_panel(surface, title):
    # Полупрозрачная панель
    s = pygame.Surface((400, 300), pygame.SRCALPHA)
    s.fill((25, 30, 40, 200))
    pygame.draw.rect(s, (50, 60, 90), s.get_rect(), 2)
    surface.blit(s, (WIDTH//2 - 200, HEIGHT//2 - 150))
    
    # Заголовок
    draw_text(surface, title, 60, WIDTH//2, HEIGHT//2 - 100, (220, 200, 100), center=True)

def main_menu():
    start_button = Button(WIDTH//2 - 100, HEIGHT//2 - 20, 200, 50, "Начать игру", lambda: None)
    quit_button = Button(WIDTH//2 - 100, HEIGHT//2 + 50, 200, 50, "Выход", lambda: None)
    
    while True:
        SCREEN.fill(BACKGROUND)
        
        # Анимированный фон
        for _ in range(5):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            pygame.draw.circle(SCREEN, (30, 40, 60), (x, y), 3)
        
        draw_text(SCREEN, "ЗМЕЙКА", 80, WIDTH//2, 100, (100, 200, 150), center=True)
        draw_text(SCREEN, "Изюминка игры:", 30, WIDTH//2, 180, (180, 180, 100), center=True)
        draw_text(SCREEN, "Специальная еда дает ускорение!", 25, WIDTH//2, 220, (150, 200, 255), center=True)
        
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            # Обработка кнопок
            if start_button.handle_event(event):
                return
            if quit_button.handle_event(event):
                pygame.quit()
                sys.exit()
                
        start_button.check_hover(mouse_pos)
        quit_button.check_hover(mouse_pos)
        
        start_button.draw(SCREEN)
        quit_button.draw(SCREEN)
        
        pygame.display.flip()

def game_over_menu(score):
    restart_button = Button(WIDTH//2 - 100, HEIGHT//2 + 20, 200, 50, "Играть снова", lambda: None)
    menu_button = Button(WIDTH//2 - 100, HEIGHT//2 + 90, 200, 50, "Главное меню", lambda: None)
    
    while True:
        SCREEN.fill(BACKGROUND)
        
        # Анимация частиц
        for _ in range(3):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            pygame.draw.circle(SCREEN, (150, 50, 50), (x, y), 2)
        
        draw_ui_panel(SCREEN, "ИГРА ОКОНЧЕНА")
        draw_text(SCREEN, f"Счет: {score}", 40, WIDTH//2, HEIGHT//2 - 30, (220, 180, 80), center=True)
        
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if restart_button.handle_event(event):
                return True
            if menu_button.handle_event(event):
                return False
                
        restart_button.check_hover(mouse_pos)
        menu_button.check_hover(mouse_pos)
        
        restart_button.draw(SCREEN)
        menu_button.draw(SCREEN)
        
        pygame.display.flip()

def main():
    snake = Snake()
    food = Food()
    particles = []
    clock = pygame.time.Clock()
    game_state = "PLAYING"
    
    # Музыка и звуки
    try:
        pygame.mixer.music.load("background.mp3")  # Заменить на реальный файл
        pygame.mixer.music.play(-1)  # Бесконечный цикл
        eat_sound = pygame.mixer.Sound("eat.wav")  # Заменить на реальный файл
    except:
        # Если звуки недоступны
        eat_sound = None
    
    while True:
        SCREEN.fill(BACKGROUND)
        draw_grid(SCREEN)
        
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if game_state == "PLAYING":
                    if event.key == pygame.K_UP and snake.direction != (0, 1):
                        snake.direction = (0, -1)
                    elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                        snake.direction = (0, 1)
                    elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                        snake.direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                        snake.direction = (1, 0)
                    elif event.key == pygame.K_ESCAPE:
                        game_state = "PAUSED"
                        
                elif game_state == "PAUSED":
                    if event.key == pygame.K_ESCAPE:
                        game_state = "PLAYING"
                        
            # Обработка кнопок паузы
            if game_state == "PAUSED":
                pass
                
        if game_state == "PLAYING":
            # Движение змейки
            if not snake.move():
                game_state = "GAME_OVER"
                
            # Проверка съедания еды
            if snake.get_head_position() == food.position:
                # Создание частиц для эффекта поедания
                for _ in range(20):
                    particles.append(Particle(
                        food.position[0] * GRID_SIZE + GRID_SIZE//2,
                        food.position[1] * GRID_SIZE + GRID_SIZE//2,
                        (255, 200, 100) if food.is_special else (255, 100, 100)
                ))
                
                snake.grow()
                if food.is_special:
                    snake.activate_speed_boost()
                    if eat_sound:
                        eat_sound.play()
                food.reset()
                
                # Проверка, что еда не появилась на змейке
                while food.position in snake.positions:
                    food.reset()
            
            # Обновление частиц
            particles = [p for p in particles if p.update()]
            
            # Рисование змейки
            snake.draw(SCREEN)
            
            # Рисование еды
            food.draw(SCREEN)
            
            # Рисование частиц
            for particle in particles:
                particle.draw(SCREEN)
            
            # Рисование UI
            draw_text(SCREEN, f"Счет: {snake.score}", 36, 10, 10)
            
            if snake.speed_boost > 0:
                draw_text(SCREEN, "УСКОРЕНИЕ!", 36, WIDTH - 150, 10, (255, 200, 50))
                
            # Изменение скорости на основе ускорения
            current_fps = FPS + 5 if snake.speed_boost > 0 else FPS
            
        elif game_state == "PAUSED":
            draw_ui_panel(SCREEN, "ПАУЗА")
            draw_text(SCREEN, "Нажмите ESC для продолжения", 30, WIDTH//2, HEIGHT//2 + 40, center=True)
            
        elif game_state == "GAME_OVER":
            # Сначала показываем экран окончания игры
            if game_over_menu(snake.score):
                # Перезапуск игры
                snake.reset()
                food.reset()
                particles = []
                game_state = "PLAYING"
            else:
                return  # Возврат в главное меню
            
        pygame.display.flip()
        clock.tick(current_fps if game_state == "PLAYING" else FPS)

if __name__ == "__main__":
    main_menu()
    while True:
        main()
```

## Особенности игры:

1. **Приятная цветовая гамма**:
   - Темная тема с сине-зелеными оттенками
   - Контрастные элементы интерфейса
   - Анимации и эффекты

2. **Меню**:
   - Главное меню с кнопками "Начать игру" и "Выход"
   - Пауза во время игры
   - Экран окончания игры с возможностью рестарта или возврата в меню

3. **Анимации**:
   - Пульсирующая еда
   - Частицы при поедании пищи
   - Анимация глаз змейки (следуют за направлением движения)
   - Эффект "ускорения" при съедании специальной еды

4. **Изюминки**:
   - **Специальная еда** (золотистого цвета) дает временное ускорение
   - Змейка может проходить сквозь стены (появляется с противоположной стороны)
   - Детализированная змейка с глазами и текстурой чешуи
   - Частицы при съедании пищи для усиления визуального эффекта
   - Полупрозрачные панели интерфейса

5. **Управление**:
   - Стрелки для управления направлением змейки
   - ESC для паузы/продолжения игры

Для работы игры необходимо установить библиотеку Pygame:
```
pip install pygame
```

Игра полностью готова к запуску. Для лучшего опыта рекомендуется добавить звуковые файлы (background.mp3 для фоновой музыки и eat.wav для звука поедания), но и без них игра будет работать корректно.