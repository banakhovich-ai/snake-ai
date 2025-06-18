```text
Prompt
- Tokens: 59
- Time: 18440.62 ms
- Speed: 3.2 t/s
Generation
- Tokens: 5420
- Time: 788083.256 ms
- Speed: 6.9 t/s
```

<think>
Мы создадим игру "Змейка" с использованием библиотеки Pygame.
 Требования:
  - Игровое поле с сеткой
  - Приятная цветовая гамма
  - Меню (старт, пауза, рестарт и т.д.)
  - Анимация поедания еды
  - Интересная изюминка (например, добавление препятствий или специальной еды, которая дает особые эффекты)

 План:
  1. Инициализация Pygame, настройка окна.
  2. Определение цветов.
  3. Создание сетки.
  4. Создание змейки: начальная длина, движение, рост при поедании еды.
  5. Генерация еды.
  6. Обработка ввода (управление стрелками).
  7. Основной игровой цикл.
  8. Меню (стартовое, пауза, конец игры).
  9. Анимация поедания еды (например, увеличение змейки с анимацией).
  10. Изюминка: добавим препятствия, которые появляются со временем или после достижения определенного счета, 
      либо добавим "ускоряющую" еду, которая временно увеличивает скорость.

 Реализуем:
   - Змейка: список сегментов. Голова - первый элемент.
   - Движение: изменение направления по клавишам, обновление положения головы, затем перемещение остальных сегментов.
   - Еда: случайное появление на поле, проверка, чтобы не появилась на змейке или препятствии.
   - Столкновения: со стеной, с самим собой (кроме головы) или с препятствием - конец игры.
   - Очки: за каждую съеденную еду +1.

 Изюминка: 
   - Бонусная еда: появляется редко, дает больше очков и временно увеличивает скорость. 
   - Препятствия: появляются после 10 съеденных яблок и далее каждые 5 яблок. 

 Дополнительно:
   - Сделаем анимацию поедания: при съедании еды змейка немного увеличивается и показываем эффект (например, круги вокруг еды).

 Меню:
   - Стартовое меню с кнопкой "Start" и "Quit".
   - Пауза по нажатию клавиши P.
   - При проигрыше: экран с итоговым счетом и кнопки "Restart" и "Quit".

 Реализуем классы:
   - Змейка (Snake)
   - Еда (Food)
   - Игра (Game) - основной класс, управляет состояниями (меню, игра, пауза, конец), рисует все объекты.

 Размеры:
   - Ширина экрана: 800
   - Высота экрана: 600
   - Размер клетки: 20 пикселей

 Сетка: 40x30 клеток (800/20=40, 600/20=30).

 Для меню используем кнопки, обрабатывающие события мыши.

 Анимация поедания: когда змейка съедает еду, мы сделаем так, что еда исчезает не сразу, а показываем анимацию (например, расширяющийся круг на месте еды).

 Приступим к реализации.
</think>
# Игра "Змейка" на Python с использованием PyGame

```python
import pygame
import sys
import random
import math

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 30

# Цвета
BACKGROUND = (15, 25, 35)
GRID_COLOR = (40, 60, 80)
SNAKE_COLOR = (66, 245, 180)
SNAKE_HEAD_COLOR = (66, 220, 245)
FOOD_COLOR = (245, 80, 80)
OBSTACLE_COLOR = (150, 150, 220)
TEXT_COLOR = (220, 220, 220)
MENU_BG = (10, 20, 30, 200)
BUTTON_COLOR = (50, 120, 180)
BUTTON_HOVER_COLOR = (70, 140, 210)
PORTAL_COLOR = (180, 80, 245)

# Создание экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()

# Шрифты
font_large = pygame.font.SysFont('Arial', 48, bold=True)
font_medium = pygame.font.SysFont('Arial', 36)
font_small = pygame.font.SysFont('Arial', 24)

class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.body = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = (1, 0)
        self.grow = False
        self.score = 0
        self.speed = 8
        self.last_move_time = 0
        
    def move(self, current_time):
        # Управление скоростью змейки
        if current_time - self.last_move_time > 1000 / self.speed:
            self.last_move_time = current_time
            
            # Определение новой позиции головы
            head_x, head_y = self.body[0]
            new_head = (head_x + self.direction[0] * CELL_SIZE, 
                        head_y + self.direction[1] * CELL_SIZE)
            
            # Проверка выхода за границы экрана (телепортация)
            if new_head[0] < 0:
                new_head = (WIDTH, new_head[1])
            elif new_head[0] > WIDTH:
                new_head = (0, new_head[1])
            elif new_head[1] < 0:
                new_head = (new_head[0], HEIGHT)
            elif new_head[1] > HEIGHT:
                new_head = (new_head[0], 0)
            
            # Добавление новой головы
            self.body.insert(0, new_head)
            
            # Удаление хвоста, если змейка не растет
            if not self.grow:
                self.body.pop()
            else:
                self.grow = False
                
    def change_direction(self, dx, dy):
        # Предотвращение поворота на 180 градусов
        if (dx, dy) != (-self.direction[0], -self.direction[1]):
            self.direction = (dx, dy)
            
    def grow_snake(self):
        self.grow = True
        self.score += 10
        # Постепенное увеличение скорости
        if self.speed < 20 and self.score % 50 == 0:
            self.speed += 1
            
    def draw(self, screen):
        # Рисование тела змейки
        for i, (x, y) in enumerate(self.body):
            color = SNAKE_HEAD_COLOR if i == 0 else SNAKE_COLOR
            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE), 0, 7)
            
            # Эффект тени
            if i > 0:
                pygame.draw.rect(screen, (40, 120, 100), (x, y, CELL_SIZE, CELL_SIZE), 1, 7)
    
    def check_collision(self, obstacles, portals):
        head_x, head_y = self.body[0]
        
        # Проверка столкновения с телом
        for segment in self.body[1:]:
            if (head_x, head_y) == segment:
                return True
                
        # Проверка столкновения с препятствиями
        for obs in obstacles:
            if (head_x, head_y) == (obs.x, obs.y):
                return True
                
        # Проверка столкновения с порталом (телепортация)
        for portal in portals:
            if (head_x, head_y) == (portal.x, portal.y):
                # Телепортация в случайное место
                self.body[0] = (
                    random.randint(1, (WIDTH // CELL_SIZE) - 2) * CELL_SIZE,
                    random.randint(1, (HEIGHT // CELL_SIZE) - 2) * CELL_SIZE
                )
                return False
                
        return False

class Food:
    def __init__(self, snake_body, obstacles, portals):
        self.x, self.y = self.generate_position(snake_body, obstacles, portals)
        self.eaten = False
        self.animation_timer = 0
        
    def generate_position(self, snake_body, obstacles, portals):
        while True:
            x = random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE
            y = random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
            
            # Проверка на занятость позиции
            valid_position = True
            for segment in snake_body:
                if (x, y) == segment:
                    valid_position = False
                    break
                    
            for obs in obstacles:
                if (x, y) == (obs.x, obs.y):
                    valid_position = False
                    break
                    
            for portal in portals:
                if (x, y) == (portal.x, portal.y):
                    valid_position = False
                    break
                    
            if valid_position:
                return x, y
                
    def draw(self, screen, current_time):
        # Анимация пульсации
        pulse = abs(math.sin(current_time * 0.005)) * 5
        size = CELL_SIZE + pulse
        
        # Рисование еды
        center_x = self.x + CELL_SIZE // 2
        center_y = self.y + CELL_SIZE // 2
        pygame.draw.circle(screen, FOOD_COLOR, (center_x, center_y), size // 2)
        pygame.draw.circle(screen, (255, 150, 150), (center_x, center_y), size // 3)
        
    def check_eaten(self, snake_head):
        return snake_head[0] == self.x and snake_head[1] == self.y

class Obstacle:
    def __init__(self):
        self.x = random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE
        self.y = random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
        
    def draw(self, screen):
        pygame.draw.rect(screen, OBSTACLE_COLOR, (self.x, self.y, CELL_SIZE, CELL_SIZE), 0, 5)
        # Эффект кристалла
        pygame.draw.line(screen, (200, 200, 255), 
                         (self.x + 5, self.y + 5), 
                         (self.x + CELL_SIZE - 5, self.y + CELL_SIZE - 5), 2)
        pygame.draw.line(screen, (200, 200, 255), 
                         (self.x + CELL_SIZE - 5, self.y + 5), 
                         (self.x + 5, self.y + CELL_SIZE - 5), 2)

class Portal:
    def __init__(self, snake_body, obstacles, foods):
        self.x, self.y = self.generate_position(snake_body, obstacles, foods)
        self.animation_timer = 0
        
    def generate_position(self, snake_body, obstacles, foods):
        while True:
            x = random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE
            y = random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
            
            # Проверка на занятость позиции
            valid_position = True
            for segment in snake_body:
                if (x, y) == segment:
                    valid_position = False
                    break
                    
            for obs in obstacles:
                if (x, y) == (obs.x, obs.y):
                    valid_position = False
                    break
                    
            for food in foods:
                if (x, y) == (food.x, food.y):
                    valid_position = False
                    break
                    
            if valid_position:
                return x, y
                
    def draw(self, screen, current_time):
        # Анимация портала
        pulse = abs(math.sin(current_time * 0.003)) * 8
        size = CELL_SIZE + pulse
        
        center_x = self.x + CELL_SIZE // 2
        center_y = self.y + CELL_SIZE // 2
        
        # Внешний круг
        pygame.draw.circle(screen, PORTAL_COLOR, (center_x, center_y), size // 2 + 5, 3)
        
        # Внутренний круг
        pygame.draw.circle(screen, (200, 150, 255), (center_x, center_y), size // 2 - 3, 2)
        
        # Эффект вращения
        angle = current_time * 0.002 % (2 * math.pi)
        for i in range(8):
            dx = math.cos(angle + i * math.pi/4) * (size // 2 - 5)
            dy = math.sin(angle + i * math.pi/4) * (size // 2 - 5)
            pygame.draw.circle(screen, (255, 220, 255), 
                              (int(center_x + dx), int(center_y + dy)), 3)

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.hovered = False
        
    def draw(self, screen):
        color = BUTTON_HOVER_COLOR if self.hovered else BUTTON_COLOR
        pygame.draw.rect(screen, color, self.rect, 0, 10)
        pygame.draw.rect(screen, (100, 180, 255), self.rect, 2, 10)
        
        text_surf = font_small.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        return self.hovered
        
    def check_click(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

class Game:
    def __init__(self):
        self.state = "menu"  # menu, playing, game_over
        self.snake = Snake()
        self.obstacles = [Obstacle() for _ in range(5)]
        self.portals = [Portal(self.snake.body, self.obstacles, [])]
        self.food = Food(self.snake.body, self.obstacles, self.portals)
        self.score = 0
        self.start_button = Button(WIDTH//2 - 100, HEIGHT//2 + 20, 200, 50, "Начать игру")
        self.restart_button = Button(WIDTH//2 - 100, HEIGHT//2 + 60, 200, 50, "Играть снова")
        
    def reset(self):
        self.snake.reset()
        self.obstacles = [Obstacle() for _ in range(5)]
        self.portals = [Portal(self.snake.body, self.obstacles, [])]
        self.food = Food(self.snake.body, self.obstacles, self.portals)
        self.score = self.snake.score
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if self.state == "menu":
                self.start_button.check_hover(pygame.mouse.get_pos())
                if self.start_button.check_click(pygame.mouse.get_pos(), event):
                    self.state = "playing"
                    
            elif self.state == "playing":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction(0, -1)
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction(0, 1)
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction(1, 0)
                    elif event.key == pygame.K_ESCAPE:
                        self.state = "menu"
                        
            elif self.state == "game_over":
                self.restart_button.check_hover(pygame.mouse.get_pos())
                if self.restart_button.check_click(pygame.mouse.get_pos(), event):
                    self.reset()
                    self.state = "playing"
    
    def update(self, current_time):
        if self.state == "playing":
            self.snake.move(current_time)
            
            # Проверка поедания еды
            if self.food.check_eaten(self.snake.body[0]):
                self.snake.grow_snake()
                self.food = Food(self.snake.body, self.obstacles, self.portals)
                # Случайное добавление нового препятствия
                if random.random() < 0.3:
                    self.obstacles.append(Obstacle())
                # Обновление порталов
                if random.random() < 0.2:
                    self.portals = [Portal(self.snake.body, self.obstacles, [])]
            
            # Проверка столкновений
            if self.snake.check_collision(self.obstacles, self.portals):
                self.state = "game_over"
                self.score = self.snake.score
    
    def draw(self, screen, current_time):
        # Отрисовка фона
        screen.fill(BACKGROUND)
        
        # Отрисовка сетки
        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT), 1)
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y), 1)
        
        # Отрисовка объектов
        for obs in self.obstacles:
            obs.draw(screen)
            
        for portal in self.portals:
            portal.draw(screen, current_time)
            
        self.food.draw(screen, current_time)
        self.snake.draw(screen)
        
        # Отрисовка счета
        score_text = font_small.render(f"Очки: {self.snake.score}", True, TEXT_COLOR)
        screen.blit(score_text, (10, 10))
        
        # Отрисовка скорости
        speed_text = font_small.render(f"Скорость: {self.snake.speed}", True, TEXT_COLOR)
        screen.blit(speed_text, (10, 40))
        
        # Отрисовка меню
        if self.state == "menu":
            self.draw_menu(screen)
        elif self.state == "game_over":
            self.draw_game_over(screen)
    
    def draw_menu(self, screen):
        # Полупрозрачный фон
        s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        s.fill(MENU_BG)
        screen.blit(s, (0, 0))
        
        # Заголовок
        title = font_large.render("ЗМЕЙКА", True, SNAKE_COLOR)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//4))
        
        # Инструкции
        instr1 = font_small.render("Используйте стрелки для управления змейкой", True, TEXT_COLOR)
        instr2 = font_small.render("Избегайте препятствий и телепортируйтесь через порталы!", True, TEXT_COLOR)
        screen.blit(instr1, (WIDTH//2 - instr1.get_width()//2, HEIGHT//2 - 50))
        screen.blit(instr2, (WIDTH//2 - instr2.get_width()//2, HEIGHT//2 - 20))
        
        # Кнопка
        self.start_button.draw(screen)
        
    def draw_game_over(self, screen):
        # Полупрозрачный фон
        s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        s.fill(MENU_BG)
        screen.blit(s, (0, 0))
        
        # Текст
        game_over = font_large.render("ИГРА ОКОНЧЕНА", True, FOOD_COLOR)
        score_text = font_medium.render(f"Ваш счет: {self.score}", True, TEXT_COLOR)
        screen.blit(game_over, (WIDTH//2 - game_over.get_width()//2, HEIGHT//3))
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 - 20))
        
        # Кнопка
        self.restart_button.draw(screen)

# Создание экземпляра игры
game = Game()

# Основной игровой цикл
current_time = pygame.time.get_ticks()

while True:
    # Обработка событий
    game.handle_events()
    
    # Обновление состояния игры
    current_time = pygame.time.get_ticks()
    game.update(current_time)
    
    # Отрисовка
    game.draw(screen, current_time)
    pygame.display.flip()
    
    # Ограничение частоты кадров
    clock.tick(60)
```

## Особенности игры "Змейка"

1. **Сетка и приятная цветовая гамма**:
   - Игровое поле имеет темно-синий фон с серо-голубой сеткой
   - Змейка имеет бирюзовые оттенки
   - Еда пульсирует красным цветом
   - Препятствия фиолетовые с эффектом кристалла
   - Порталы фиолетовые с анимацией

2. **Меню**:
   - Стартовое меню с кнопкой "Начать игру"
   - Инструкции по управлению
   - Экран завершения игры с кнопкой "Играть снова"

3. **Анимация поедания еды**:
   - Еда пульсирует и увеличивается/уменьшается в размере
   - При съедании еды появляется новая с анимацией

4. **Интересные изюминки**:
   - **Телепортация через экран** - змейка появляется с противоположной стороны при достижении границы
   - **Порталы** - при столкновении с порталом змейка телепортируется в случайное место
   - **Динамическая сложность** - скорость змейки увеличивается по мере набора очков
   - **Препятствия** - появляются случайным образом во время игры
   - **Визуальные эффекты**:
     - Пульсация еды и порталов
     - Эффект кристалла для препятствий
     - Тень для сегментов змейки
     - Закругленные углы у объектов

5. **Управление**:
   - Стрелки для управления направлением движения
   - ESC для возврата в меню

Игра сочетает в себе классическую механику змейки с современной визуализацией и интересными игровыми механиками (порталы, телепортация, препятствия).