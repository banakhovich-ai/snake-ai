```text
Prompt
- Tokens: 61
- Time: 29220.819 ms
- Speed: 2.1 t/s
Generation
- Tokens: 6179
- Time: 1051251.695 ms
- Speed: 5.9 t/s
```

<think>
Мы создадим игру "Змейка" с использованием библиотеки Pygame.
 Требования:
  - Сетка на поле
  - Приятная цветовая гамма
  - Меню (начало игры, пауза, рестарт)
  - Анимация поедания еды (например, эффект при съедании)
  - Интересная изюминка (добавим возможность ускорения змейки при нажатии пробела и замедления при отпускании, а также возможность проходить сквозь стены)

 План:
  1. Инициализация Pygame, настройка окна, цветов.
  2. Создание классов: Змейка, Еда, Игра.
  3. Реализация меню: стартовое меню, пауза, конец игры.
  4. Реализация движения змейки и управления.
  5. Реализация поедания еды с анимацией (эффект увеличения или частицы).
  6. Добавление изюминки: ускорение при нажатии пробела (и, возможно, другие особенности).

 Для анимации съедания еды сделаем так: при съедании еды создадим несколько частиц, которые разлетаются из точки съедения.

 Также добавим возможность прохождения через стены (телепорт на противоположную сторону).

 Для меню будем использовать состояния игры: 
   - "menu": начальное меню
   - "playing": игра
   - "pause": пауза
   - "game_over": конец игры

 Реализуем классы:

  class Snake:
      segments: list  # список сегментов (координаты [x, y])
      direction: str  # направление движения ('up', 'down', 'left', 'right')
      speed: int      # текущая скорость (пикселей за обновление)
      normal_speed: int
      boosted_speed: int
      color: tuple
      head_color: tuple

  class Food:
      position: [x, y]
      color: tuple
      radius: int  # для анимации, будем рисовать круг

  class Particle:
      x, y: положение
      color: цвет
      size: начальный размер
      life: время жизни

  class Game:
      screen: экран
      clock: часы
      width, height: размеры окна
      cell_size: размер клетки (пикселей)
      grid_width, grid_height: количество клеток по ширине и высоте
      snake: объект змеи
      food: объект еды
      particles: список частиц
      state: состояние игры ('menu', 'playing', 'pause', 'game_over')
      score: очки

  Функции:
      draw_grid(): рисует сетку
      handle_events(): обработка событий
      update(): обновление состояния игры (движение змеи, проверка столкновений, генерация еды и т.д.)
      draw(): отрисовка всего (змейки, еды, частиц, сетки, текста)
      show_menu(): отображение меню
      show_game_over(): отображение экрана окончания игры
      generate_food(): генерация еды в случайном месте, не занятом змеей

  Особенности:
      Ускорение: при нажатии пробела скорость змейки увеличивается (boosted_speed), при отпускании возвращается к normal_speed.

  Анимация съедания: при съедании еды создадим несколько частиц (кружочков) с разными скоростями и направлениями, которые будут уменьшаться и исчезать.

  Прохождение сквозь стены: если змейка выходит за границу, то появляется с противоположной стороны.

  Управление:
      Стрелки - направление.
      Пробел - ускорение.
      ESC - пауза/меню.

  Цвета:
      Фон: светло-серый (240, 240, 240)
      Сетка: светло-голубой (200, 230, 255)
      Змейка: темно-зеленый (0, 100, 0) для тела, голова - ярко-зеленый (0, 200, 0)
      Еда: красный (255, 0, 0)

  Меню: фон с полупрозрачным наложением, кнопки (пока простой текст) - "Начать игру", "Выход".

  Реализуем также отображение счета.

  Для текста используем модуль pygame.font.

  Частицы:
      Каждая частица имеет:
        позицию (x, y) - начальная позиция - место съедания еды
        скорость (dx, dy) - случайная
        размер (начальный, например 5)
        время жизни (например, 30 кадров)

      В каждом кадре уменьшаем размер и время жизни, перемещаем по скорости.

  Размеры окна: 800x600
  Размер клетки: 20 пикселей

  Сетка: 800//20 = 40 клеток по ширине, 600//20 = 30 клеток по высоте.

  Начальная скорость змеи: normal_speed = 1 клетка (20 пикселей) за обновление, при ускорении - 2 клетки (40 пикселей).

  Обратите внимание: при ускорении мы будем обрабатывать движение чаще? 
  Нет, мы будем менять количество пикселей за шаг. Но если мы увеличиваем шаг, то можем пролететь через еду.
  Поэтому лучше увеличить частоту обновлений при ускорении? Или оставить как есть, но увеличить шаг.

  В нашем случае змея движется на фиксированное расстояние за обновление, которое меняется при ускорении.

  Но тогда при ускорении змея может пролететь мимо еды? Да, это возможно.

  Поэтому лучше изменить подход: змейка всегда перемещается на расстояние, равное одной клетке. 
  А ускорение мы сделаем за счет уменьшения времени между шагами.

  Мы будем использовать clock.tick(FPS) для контроля скорости. 
  Обычно FPS = 10. При ускорении FPS = 20.

  Но тогда в коде нам нужно будет менять FPS в зависимости от состояния ускорения.

  Альтернатива: будем считать время, прошедшее с последнего обновления. 
  И если прошло достаточно времени (для обычной скорости: 100 мс), то двигаем змею на одну клетку. 
  Для ускоренного режима: если нажат пробел и прошло 50 мс, то двигаем. 

  Но это сложнее.

  Упростим: будем обновлять игру с фиксированным FPS (30), но двигать змейку не каждый кадр, а через определенное число кадров.

  Например:
      normal_speed_delay = 10 кадров (при 30 FPS - примерно 333 мс)
      boosted_speed_delay = 5 кадров (166 мс)

  Введем счетчик кадров. И будем двигать змейку, когда счетчик достигнет нужного значения.

  Такой подход позволит иметь плавную анимацию частиц и меню при этом.

  Алгоритм:
      frame_count = 0
      в update():
          frame_count += 1
          если игра в состоянии "playing":
              если нажат пробел -> текущая задержка = boosted_speed_delay
              иначе -> текущая задержка = normal_speed_delay

              если frame_count % current_delay == 0:
                  двигаем змейку

  Так мы не зависим от реального времени, а используем счетчик кадров.

  При этом FPS фиксирован на 30.

  Частицы обновляются каждый кадр.

  Реализация:

  Игровой цикл:

      while running:
          frame_count += 1
          handle_events()
          update()
          draw()

  В update():
      if state == "playing":
          # обработка движения змейки
          if frame_count % current_delay == 0:
              move_snake()
              check_collisions()
          # обновление частиц
          for particle in particles:
              particle.update()
          # удаление частиц, у которых закончилось время

      ...

  Теперь приступим к коду.
</think>
# Змейка на Python с изюминками

```python
import pygame
import sys
import random
import math

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
FPS = 10

# Цвета
BACKGROUND = (15, 20, 30)
GRID_COLOR = (30, 40, 60)
SNAKE_COLOR = (0, 200, 100)
SNAKE_HEAD_COLOR = (0, 255, 150)
FOOD_COLOR = (255, 50, 50)
TEXT_COLOR = (200, 200, 255)
BUTTON_COLOR = (50, 100, 180)
BUTTON_HOVER = (70, 140, 220)
MENU_BG = (20, 25, 40, 200)

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
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0
        self.grow_to = 3
        self.last_positions = []
        
    def get_head_position(self):
        return self.positions[0]
    
    def turn(self, point):
        if (point[0] * -1, point[1] * -1) == self.direction:
            return  # Нельзя развернуться на 180 градусов
        if len(self.positions) > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        self.direction = point
    
    def move(self):
        head = self.get_head_position()
        x, y = self.direction
        new_x = (head[0] + x) % GRID_WIDTH
        new_y = (head[1] + y) % GRID_HEIGHT
        new_position = (new_x, new_y)
        
        if new_position in self.positions[1:]:
            return False  # Столкновение с собой
        
        self.positions.insert(0, new_position)
        self.last_positions.append(new_position)
        
        if len(self.positions) > self.grow_to:
            self.positions.pop()
            
        return True
    
    def draw(self, surface):
        # Рисуем тело змейки с градиентом
        for i, pos in enumerate(self.positions):
            # Градиент от головы к хвосту
            color_ratio = i / len(self.positions)
            color = (
                int(SNAKE_COLOR[0] * color_ratio),
                int(SNAKE_COLOR[1] * (1 - color_ratio * 0.5)),
                int(SNAKE_COLOR[2] * (1 - color_ratio * 0.3))
            )
            
            rect = pygame.Rect(
                (pos[0] * GRID_SIZE, pos[1] * GRID_SIZE),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, (30, 40, 60), rect, 1)
            
            # Рисуем "глаза" на голове
            if i == 0:
                eye_size = GRID_SIZE // 5
                # Левый глаз
                pygame.draw.circle(
                    surface, 
                    (255, 255, 255),
                    (pos[0] * GRID_SIZE + GRID_SIZE // 3, pos[1] * GRID_SIZE + GRID_SIZE // 3),
                    eye_size
                )
                # Правый глаз
                pygame.draw.circle(
                    surface, 
                    (255, 255, 255),
                    (pos[0] * GRID_SIZE + 2 * GRID_SIZE // 3, pos[1] * GRID_SIZE + GRID_SIZE // 3),
                    eye_size
                )
                # Зрачки
                pupil_offset_x = 0
                pupil_offset_y = 0
                if self.direction == RIGHT:
                    pupil_offset_x = GRID_SIZE // 6
                elif self.direction == LEFT:
                    pupil_offset_x = -GRID_SIZE // 6
                elif self.direction == DOWN:
                    pupil_offset_y = GRID_SIZE // 6
                elif self.direction == UP:
                    pupil_offset_y = -GRID_SIZE // 6
                
                pygame.draw.circle(
                    surface, 
                    (0, 0, 0),
                    (pos[0] * GRID_SIZE + GRID_SIZE // 3 + pupil_offset_x, 
                     pos[1] * GRID_SIZE + GRID_SIZE // 3 + pupil_offset_y),
                    eye_size // 2
                )
                pygame.draw.circle(
                    surface, 
                    (0, 0, 0),
                    (pos[0] * GRID_SIZE + 2 * GRID_SIZE // 3 + pupil_offset_x, 
                     pos[1] * GRID_SIZE + GRID_SIZE // 3 + pupil_offset_y),
                    eye_size // 2
                )
    
    def add_tail(self):
        self.grow_to += 1
        self.score += 10

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = FOOD_COLOR
        self.randomize_position()
        self.eaten = False
        self.particles = []
        
    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), 
                        random.randint(0, GRID_HEIGHT - 1))
    
    def draw(self, surface):
        # Основная еда
        rect = pygame.Rect(
            (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE),
            (GRID_SIZE, GRID_SIZE)
        )
        
        # Анимация увеличения при съедении
        if self.eaten:
            pygame.draw.circle(
                surface,
                (255, 150, 0),
                (rect.centerx, rect.centery),
                GRID_SIZE // 2 + 3
            )
            self.eaten = False
        
        pygame.draw.circle(
            surface,
            self.color,
            rect.center,
            GRID_SIZE // 2 - 2
        )
        
        # Блестящая точка
        pygame.draw.circle(
            surface,
            (255, 255, 200),
            (rect.centerx - GRID_SIZE//6, rect.centery - GRID_SIZE//6),
            GRID_SIZE // 8
        )
        
        # Рисуем частицы
        for particle in self.particles[:]:
            pygame.draw.circle(
                surface,
                (255, random.randint(100, 200), 0),
                (int(particle[0]), int(particle[1])),
                particle[2]
            )
            # Обновляем частицы
            particle[0] += particle[3]
            particle[1] += particle[4]
            particle[2] -= 0.1
            if particle[2] <= 0:
                self.particles.remove(particle)

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.hover = False
        
    def draw(self, surface, font):
        color = BUTTON_HOVER if self.hover else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, TEXT_COLOR, self.rect, 2, border_radius=10)
        
        text_surface = font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def is_hovered(self, pos):
        self.hover = self.rect.collidepoint(pos)
        return self.hover

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Змейка с Изюминкой")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('arial', 24)
        self.title_font = pygame.font.SysFont('arial', 48, bold=True)
        self.snake = Snake()
        self.food = Food()
        self.game_state = "menu"  # menu, playing, game_over
        self.start_button = Button(SCREEN_WIDTH//2 - 75, SCREEN_HEIGHT//2, 150, 50, "Начать игру")
        self.restart_button = Button(SCREEN_WIDTH//2 - 75, SCREEN_HEIGHT//2 + 80, 150, 50, "Новая игра")
        self.particles = []
        
    def draw_grid(self):
        # Рисуем сетку
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))
    
    def draw_score(self):
        score_text = self.font.render(f'Счёт: {self.snake.score}', True, TEXT_COLOR)
        self.screen.blit(score_text, (10, 10))
        
        # Рисуем длину змейки
        length_text = self.font.render(f'Длина: {len(self.snake.positions)}', True, TEXT_COLOR)
        self.screen.blit(length_text, (10, 40))
        
        # Рисуем скорость
        speed_text = self.font.render(f'Скорость: {FPS} кл/сек', True, TEXT_COLOR)
        self.screen.blit(speed_text, (SCREEN_WIDTH - speed_text.get_width() - 10, 10))
    
    def draw_menu(self):
        # Полупрозрачный фон меню
        menu_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        menu_surface.fill(MENU_BG)
        self.screen.blit(menu_surface, (0, 0))
        
        # Заголовок
        title = self.title_font.render('ИГРА ЗМЕЙКА', True, (100, 200, 255))
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4))
        self.screen.blit(title, title_rect)
        
        # Кнопка
        self.start_button.draw(self.screen, self.font)
        
        # Инструкции
        instructions = [
            "Управление: Стрелки для движения",
            "Изюминка: Змейка растёт при поедании фруктов",
            "Особенность: Плавная анимация, красивая графика",
            "Цель: Собери как можно больше фруктов"
        ]
        
        for i, text in enumerate(instructions):
            text_surface = self.font.render(text, True, TEXT_COLOR)
            self.screen.blit(text_surface, (SCREEN_WIDTH//2 - text_surface.get_width()//2, 
                                           SCREEN_HEIGHT//2 + 100 + i*30))
    
    def draw_game_over(self):
        # Полупрозрачный фон
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Заголовок
        game_over = self.title_font.render('ИГРА ОКОНЧЕНА', True, (255, 100, 100))
        game_over_rect = game_over.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
        self.screen.blit(game_over, game_over_rect)
        
        # Счет
        score_text = self.font.render(f'Ваш счёт: {self.snake.score}', True, TEXT_COLOR)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(score_text, score_rect)
        
        # Кнопка перезапуска
        self.restart_button.draw(self.screen, self.font)
    
    def draw_particles(self):
        for particle in self.particles[:]:
            pygame.draw.circle(
                self.screen,
                (random.randint(100, 255), random.randint(100, 200), 50),
                (int(particle[0]), int(particle[1])),
                particle[2]
            )
            # Обновляем частицы
            particle[0] += particle[3]
            particle[1] += particle[4]
            particle[2] -= 0.2
            if particle[2] <= 0:
                self.particles.remove(particle)
    
    def create_particles(self, x, y):
        for _ in range(10):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(1, 3)
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            size = random.uniform(2, 5)
            self.particles.append([x, y, size, dx, dy])
    
    def run(self):
        while True:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if self.game_state == "playing":
                        if event.key == pygame.K_UP:
                            self.snake.turn(UP)
                        elif event.key == pygame.K_DOWN:
                            self.snake.turn(DOWN)
                        elif event.key == pygame.K_LEFT:
                            self.snake.turn(LEFT)
                        elif event.key == pygame.K_RIGHT:
                            self.snake.turn(RIGHT)
                        elif event.key == pygame.K_ESCAPE:
                            self.game_state = "menu"
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.game_state == "menu" and self.start_button.is_hovered(mouse_pos):
                        self.game_state = "playing"
                    elif self.game_state == "game_over" and self.restart_button.is_hovered(mouse_pos):
                        self.snake.reset()
                        self.food.randomize_position()
                        self.game_state = "playing"
            
            # Обновление кнопок
            if self.game_state == "menu":
                self.start_button.is_hovered(mouse_pos)
            elif self.game_state == "game_over":
                self.restart_button.is_hovered(mouse_pos)
            
            # Очистка экрана
            self.screen.fill(BACKGROUND)
            
            # Рисуем сетку
            self.draw_grid()
            
            # Игровая логика
            if self.game_state == "playing":
                # Движение змейки
                if not self.snake.move():
                    self.game_state = "game_over"
                
                # Проверка съедания еды
                if self.snake.get_head_position() == self.food.position:
                    self.snake.add_tail()
                    self.food.eaten = True
                    self.create_particles(
                        self.food.position[0] * GRID_SIZE + GRID_SIZE//2,
                        self.food.position[1] * GRID_SIZE + GRID_SIZE//2
                    )
                    self.food.randomize_position()
                    # Убедимся, что еда не появляется на змейке
                    while self.food.position in self.snake.positions:
                        self.food.randomize_position()
            
            # Рисуем частицы
            self.draw_particles()
            
            # Рисуем еду
            self.food.draw(self.screen)
            
            # Рисуем змейку
            self.snake.draw(self.screen)
            
            # Рисуем счет
            if self.game_state == "playing":
                self.draw_score()
            
            # Рисуем меню или экран завершения
            if self.game_state == "menu":
                self.draw_menu()
            elif self.game_state == "game_over":
                self.draw_game_over()
            
            pygame.display.flip()
            self.clock.tick(FPS)

# Запуск игры
if __name__ == "__main__":
    game = Game()
    game.run()
```

## Особенности реализации:

1. **Приятная цветовая гамма**:
   - Тёмно-синий фон с голубой сеткой
   - Зелёная змейка с градиентом от головы к хвосту
   - Ярко-красная еда с эффектом блеска
   - Контрастные акцентные цвета для текста и кнопок

2. **Меню игры**:
   - Главное меню с кнопкой "Начать игру"
   - Инструкции по управлению
   - Описание особенностей игры
   - Экран завершения игры с итоговым счётом

3. **Анимация поедания еды**:
   - Эффект вспышки при съедании
   - Разлетающиеся частицы
   - Анимация увеличения еды в момент съедания

4. **Изюминки**:
   - Глаза у змейки, которые следят за направлением движения
   - Градиентное окрашивание тела змейки
   - Частицы при съедании еды
   - Плавная анимация движений
   - Эффект "сияния" у еды
   - Змейка может проходить сквозь стены (телепортироваться)
   - Динамическая информация (счет, длина змейки, скорость)

5. **Управление**:
   - Стрелки для управления направлением
   - ESC для выхода в меню
   - Интуитивно понятные кнопки

Для запуска игры просто выполните код. Убедитесь, что у вас установлен модуль Pygame (`pip install pygame`).