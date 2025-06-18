```text
Prompt
- Tokens: 59
- Time: 3279.928 ms
- Speed: 18.0 t/s
Generation
- Tokens: 6457
- Time: 2097096.35 ms
- Speed: 3.1 t/s
```

<think>
Мы создадим игру "Змейка" с использованием библиотеки Pygame.
 Требования:
  - Игровое поле с сеткой.
  - Приятная цветовая гамма.
  - Меню (начало игры, пауза, конец игры).
  - Анимация поедания еды (например, эффект при съедании).
  - Интересная изюминка: добавим два типа еды: обычная (увеличивает длину на 1) и специальная (увеличивает на 3, но появляется редко и ненадолго).

 План:
  1. Инициализация Pygame, настройка окна.
  2. Определение цветов.
  3. Создание сетки.
  4. Класс Змейки: перемещение, рост, проверка столкновений.
  5. Класс Еды: обычная и специальная (золотая). Специальная еда появляется случайно на короткое время.
  6. Основной игровой цикл с меню (начало, пауза, игра, конец игры).
  7. Анимация при съедании еды: когда змея ест еду, создадим эффект (например, круги или частицы).
  8. Дополнительно: подсчет очков, уровни сложности (скорость змейки увеличивается).

 Реализация:

 Шаг 1: Инициализация и константы
 Шаг 2: Класс Snake
 Шаг 3: Класс Food (обычная и специальная)
 Шаг 4: Класс Game, который управляет состоянием игры (меню, игра, конец) и отрисовкой.

 Анимацию при съедании еды реализуем с помощью создания частиц в месте съеденной еды.

 Для простоты меню будет содержать:
   - Начальный экран: кнопка "Начать игру", "Выход"
   - Пауза: по нажатию клавиши P
   - Конец игры: экран с очками и кнопками "Играть снова", "Выход"

 Изюминка: специальная еда (золотая) появляется на 5 секунд, затем исчезает. Если змея успевает ее съесть, то змейка растет на 3 сегмента.

 Реализуем систему очков:
   - Обычная еда: 10 очков.
   - Золотая еда: 50 очков.

 Дополнительно: если змея съедает золотую еду, то в течение 3 секунд она становится "ускоренной" (двигается быстрее) или наоборот, замедленной? 
 Но в классической змейке скорость постоянна. Мы не будем менять скорость, чтобы не усложнять, но добавим бонус в виде роста на 3.

 Структура:

 1. Импорты и настройки.
 2. Класс Particle (для анимации съеденной еды)
 3. Класс Snake
 4. Класс Food (с типом: normal или special)
 5. Класс Game

 Сетка: нарисуем тонкие линии на поле.

 Приятная цветовая гамма:
   - Фон: #0f1f3a (темно-синий)
   - Сетка: #1a3b5a (голубовато-серый)
   - Змейка: #4caf50 (зеленый) и голова: #2e7d32 (темно-зеленый)
   - Обычная еда: #ff5252 (красный)
   - Специальная еда: #ffd740 (золотой)

 Меню: фон, кнопки.
</think>
# Змейка на Python с PyGame

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
FPS = 10

# Цвета (приятная пастельная гамма)
BACKGROUND = (41, 47, 54)
GRID_COLOR = (60, 70, 77)
SNAKE_HEAD = (76, 175, 80)
SNAKE_BODY = (102, 187, 106)
FOOD_COLOR = (255, 152, 0)
SPECIAL_FOOD_COLOR = (255, 193, 7)
TEXT_COLOR = (224, 224, 224)
BUTTON_COLOR = (92, 107, 192)
BUTTON_HOVER = (118, 132, 205)
MENU_BG = (30, 35, 42)

# Направления
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
        self.special_effect = 0
    
    def get_head_position(self):
        return self.positions[0]
    
    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point
    
    def move(self):
        head = self.get_head_position()
        x, y = self.direction
        new_position = ((head[0] + x) % GRID_WIDTH, (head[1] + y) % GRID_HEIGHT)
        
        if new_position in self.positions[1:]:
            return False  # Столкновение с собой
        
        self.positions.insert(0, new_position)
        
        if len(self.positions) > self.grow_to:
            self.positions.pop()
            
        return True  # Движение успешно
    
    def grow(self, amount=1):
        self.grow_to += amount
        self.score += 10 * amount
    
    def draw(self, surface):
        for i, p in enumerate(self.positions):
            color = SNAKE_HEAD if i == 0 else SNAKE_BODY
            
            # Эффект после поедания специальной еды
            if self.special_effect > 0:
                if i == 0:
                    color = (255, 255, 100)  # Голова светится
                elif random.random() < 0.3:
                    color = (150, 255, 150)  # Случайные сегменты светятся
            
            rect = pygame.Rect((p[0] * GRID_SIZE, p[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, (30, 30, 30), rect, 1)
            
            # Рисуем глаза у головы
            if i == 0:
                eye_size = GRID_SIZE // 5
                # Определяем направление взгляда
                dx, dy = self.direction
                eye_offset_x = dx * (GRID_SIZE // 3)
                eye_offset_y = dy * (GRID_SIZE // 3)
                
                # Левый глаз
                left_eye = pygame.Rect(
                    (p[0] * GRID_SIZE + GRID_SIZE//3 - eye_size//2 + eye_offset_x//3, 
                     p[1] * GRID_SIZE + GRID_SIZE//3 - eye_size//2 + eye_offset_y//3),
                    (eye_size, eye_size)
                )
                # Правый глаз
                right_eye = pygame.Rect(
                    (p[0] * GRID_SIZE + 2*GRID_SIZE//3 - eye_size//2 + eye_offset_x//3, 
                     p[1] * GRID_SIZE + GRID_SIZE//3 - eye_size//2 + eye_offset_y//3),
                    (eye_size, eye_size)
                )
                
                pygame.draw.rect(surface, (30, 30, 30), left_eye)
                pygame.draw.rect(surface, (30, 30, 30), right_eye)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = FOOD_COLOR
        self.randomize_position()
        self.special = False
        self.special_timer = 0
    
    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), 
                      random.randint(0, GRID_HEIGHT - 1))
        # С вероятностью 15% создаем специальную еду
        self.special = random.random() < 0.15
        self.special_timer = 30 if self.special else 0
    
    def draw(self, surface):
        rect = pygame.Rect((self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE), 
                          (GRID_SIZE, GRID_SIZE))
        
        if self.special:
            # Рисуем "звездочку" для специальной еды
            pygame.draw.rect(surface, SPECIAL_FOOD_COLOR, rect)
            pygame.draw.rect(surface, (180, 160, 0), rect, 1)
            
            # Анимация звезды
            if pygame.time.get_ticks() % 500 < 250:
                center_x = self.position[0] * GRID_SIZE + GRID_SIZE // 2
                center_y = self.position[1] * GRID_SIZE + GRID_SIZE // 2
                radius = GRID_SIZE // 3
                pygame.draw.circle(surface, (255, 255, 200), (center_x, center_y), radius)
        else:
            # Обычная еда с "яблочным" дизайном
            pygame.draw.rect(surface, self.color, rect)
            pygame.draw.rect(surface, (180, 80, 0), rect, 1)
            
            # Рисуем черенок
            pygame.draw.rect(surface, (120, 70, 20), 
                            (rect.x + GRID_SIZE // 2 - 2, rect.y - 3, 4, 5))
            
            # Рисуем листик
            leaf_points = [
                (rect.x + GRID_SIZE // 2 + 4, rect.y - 1),
                (rect.x + GRID_SIZE // 2 + 8, rect.y - 5),
                (rect.x + GRID_SIZE // 2 + 4, rect.y - 3)
            ]
            pygame.draw.polygon(surface, (102, 187, 106), leaf_points)

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 5)
        self.speed_x = random.uniform(-2, 2)
        self.speed_y = random.uniform(-2, 2)
        self.life = random.randint(20, 40)
    
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.life -= 1
        self.size = max(0, self.size - 0.1)
        return self.life > 0
    
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size))

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = BUTTON_COLOR
        self.hover_color = BUTTON_HOVER
        self.is_hovered = False
    
    def draw(self, surface, font):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, (100, 110, 190), self.rect, 2, border_radius=8)
        
        text_surf = font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
    
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
    
    def check_click(self, pos, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Змейка')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 24)
        self.title_font = pygame.font.SysFont('Arial', 48, bold=True)
        
        self.snake = Snake()
        self.food = Food()
        self.particles = []
        
        self.state = "MENU"  # MENU, PLAYING, GAME_OVER
        self.init_menu()
        
        # Изюминка: телепортационные порталы
        self.portals = []
        self.portal_cooldown = 0
        
    def init_menu(self):
        center_x = SCREEN_WIDTH // 2
        self.play_button = Button(center_x - 100, 250, 200, 50, "Играть")
        self.quit_button = Button(center_x - 100, 320, 200, 50, "Выход")
    
    def spawn_portals(self):
        self.portals = []
        
        # Генерируем две пары порталов
        for _ in range(2):
            portal1 = (random.randint(2, GRID_WIDTH - 3), random.randint(2, GRID_HEIGHT - 3))
            portal2 = (random.randint(2, GRID_WIDTH - 3), random.randint(2, GRID_HEIGHT - 3))
            
            # Убедимся, что порталы не накладываются друг на друга и не на змею/еду
            while portal1 == portal2 or portal1 in [p[0] for p in self.portals] or portal2 in [p[0] for p in self.portals]:
                portal1 = (random.randint(2, GRID_WIDTH - 3), random.randint(2, GRID_HEIGHT - 3))
                portal2 = (random.randint(2, GRID_WIDTH - 3), random.randint(2, GRID_HEIGHT - 3))
            
            self.portals.append((portal1, portal2))
        
        self.portal_cooldown = 300  # Порталы существуют 300 кадров
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            if self.state == "MENU":
                self.play_button.check_hover(pygame.mouse.get_pos())
                if self.play_button.check_click(pygame.mouse.get_pos(), event):
                    self.state = "PLAYING"
                    self.snake.reset()
                    self.food.randomize_position()
                elif self.quit_button.check_click(pygame.mouse.get_pos(), event):
                    pygame.quit()
                    sys.exit()
            
            elif self.state == "PLAYING":
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.snake.turn(UP)
                    elif event.key == K_DOWN:
                        self.snake.turn(DOWN)
                    elif event.key == K_LEFT:
                        self.snake.turn(LEFT)
                    elif event.key == K_RIGHT:
                        self.snake.turn(RIGHT)
                    elif event.key == K_ESCAPE:
                        self.state = "MENU"
            
            elif self.state == "GAME_OVER":
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.state = "PLAYING"
                        self.snake.reset()
                        self.food.randomize_position()
                        self.portals = []
                        self.portal_cooldown = 0
    
    def update(self):
        if self.state == "PLAYING":
            # Движение змеи
            if not self.snake.move():
                self.state = "GAME_OVER"
                return
            
            # Проверка съедания еды
            if self.snake.get_head_position() == self.food.position:
                # Анимация поедания
                self.create_eating_particles()
                
                # Специальная еда дает больше очков и временный эффект
                if self.food.special:
                    self.snake.grow(3)
                    self.snake.special_effect = 30  # Эффект длится 30 кадров
                else:
                    self.snake.grow(1)
                
                self.food.randomize_position()
                
                # Проверяем, чтобы еда не появилась на змее
                while self.food.position in self.snake.positions:
                    self.food.randomize_position()
            
            # Обновление частиц
            self.particles = [p for p in self.particles if p.update()]
            
            # Обновление специального эффекта змеи
            if self.snake.special_effect > 0:
                self.snake.special_effect -= 1
            
            # Порталная система (изюминка)
            if len(self.portals) == 0 and random.random() < 0.01:
                self.spawn_portals()
            
            if self.portal_cooldown > 0:
                self.portal_cooldown -= 1
                
                # Телепортация змеи при входе в портал
                head_pos = self.snake.get_head_position()
                for (portal1, portal2) in self.portals:
                    if head_pos == portal1:
                        # Находим направление выхода из портала
                        dx = portal2[0] - portal1[0]
                        dy = portal2[1] - portal1[1]
                        
                        # Перемещаем змею
                        self.snake.positions[0] = portal2
                        
                        # Создаем частицы для эффекта телепортации
                        self.create_portal_particles(portal1)
                        self.create_portal_particles(portal2)
                        
                        # Очищаем порталы после использования
                        self.portals = []
                        self.portal_cooldown = 0
                        break
                    
                    elif head_pos == portal2:
                        dx = portal1[0] - portal2[0]
                        dy = portal1[1] - portal2[1]
                        
                        self.snake.positions[0] = portal1
                        self.create_portal_particles(portal1)
                        self.create_portal_particles(portal2)
                        self.portals = []
                        self.portal_cooldown = 0
                        break
            
            # Удаление порталов по истечении времени
            if self.portal_cooldown == 0:
                self.portals = []
    
    def create_eating_particles(self):
        food_pos = self.food.position
        center_x = food_pos[0] * GRID_SIZE + GRID_SIZE // 2
        center_y = food_pos[1] * GRID_SIZE + GRID_SIZE // 2
        
        for _ in range(20):
            color = SPECIAL_FOOD_COLOR if self.food.special else FOOD_COLOR
            self.particles.append(Particle(center_x, center_y, color))
    
    def create_portal_particles(self, portal_pos):
        center_x = portal_pos[0] * GRID_SIZE + GRID_SIZE // 2
        center_y = portal_pos[1] * GRID_SIZE + GRID_SIZE // 2
        
        for _ in range(30):
            self.particles.append(Particle(center_x, center_y, (128, 0, 128)))
    
    def draw_grid(self):
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y), 1)
    
    def draw_portals(self):
        for (portal1, portal2) in self.portals:
            # Рисуем первый портал
            rect1 = pygame.Rect(
                (portal1[0] * GRID_SIZE, portal1[1] * GRID_SIZE),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(self.screen, (138, 43, 226), rect1, border_radius=8)
            pygame.draw.rect(self.screen, (75, 0, 130), rect1, 2, border_radius=8)
            
            # Анимация портала
            if pygame.time.get_ticks() % 500 < 250:
                center_x = portal1[0] * GRID_SIZE + GRID_SIZE // 2
                center_y = portal1[1] * GRID_SIZE + GRID_SIZE // 2
                radius = GRID_SIZE // 2
                pygame.draw.circle(self.screen, (200, 100, 255), (center_x, center_y), radius)
            
            # Рисуем второй портал
            rect2 = pygame.Rect(
                (portal2[0] * GRID_SIZE, portal2[1] * GRID_SIZE),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(self.screen, (138, 43, 226), rect2, border_radius=8)
            pygame.draw.rect(self.screen, (75, 0, 130), rect2, 2, border_radius=8)
            
            if pygame.time.get_ticks() % 500 < 250:
                center_x = portal2[0] * GRID_SIZE + GRID_SIZE // 2
                center_y = portal2[1] * GRID_SIZE + GRID_SIZE // 2
                radius = GRID_SIZE // 2
                pygame.draw.circle(self.screen, (200, 100, 255), (center_x, center_y), radius)
    
    def draw(self):
        self.screen.fill(BACKGROUND)
        self.draw_grid()
        
        # Рисуем порталы (если есть)
        if self.state == "PLAYING" and self.portals:
            self.draw_portals()
        
        # Рисуем еду
        self.food.draw(self.screen)
        
        # Рисуем змею
        self.snake.draw(self.screen)
        
        # Рисуем частицы
        for particle in self.particles:
            particle.draw(self.screen)
        
        # Рисуем счет
        score_text = self.font.render(f'Очки: {self.snake.score}', True, TEXT_COLOR)
        self.screen.blit(score_text, (10, 10))
        
        # Рисуем специальный индикатор
        if self.snake.special_effect > 0:
            effect_text = self.font.render('БОНУС!', True, (255, 255, 0))
            self.screen.blit(effect_text, (SCREEN_WIDTH - 120, 10))
        
        # Отрисовка меню
        if self.state == "MENU":
            # Затемнение игрового поля
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
            # Заголовок
            title = self.title_font.render('ЗМЕЙКА', True, TEXT_COLOR)
            title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 150))
            self.screen.blit(title, title_rect)
            
            # Кнопки
            self.play_button.draw(self.screen, self.font)
            self.quit_button.draw(self.screen, self.font)
            
            # Подсказка
            hint = self.font.render('Управление: Стрелки, ESC - меню', True, (180, 180, 180))
            hint_rect = hint.get_rect(center=(SCREEN_WIDTH//2, 500))
            self.screen.blit(hint, hint_rect)
        
        # Отрисовка экрана завершения игры
        elif self.state == "GAME_OVER":
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
            game_over = self.title_font.render('ИГРА ОКОНЧЕНА', True, (255, 100, 100))
            game_over_rect = game_over.get_rect(center=(SCREEN_WIDTH//2, 200))
            self.screen.blit(game_over, game_over_rect)
            
            score_text = self.font.render(f'Ваш счет: {self.snake.score}', True, TEXT_COLOR)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, 280))
            self.screen.blit(score_text, score_rect)
            
            restart = self.font.render('Нажмите SPACE для новой игры', True, (180, 180, 180))
            restart_rect = restart.get_rect(center=(SCREEN_WIDTH//2, 350))
            self.screen.blit(restart, restart_rect)
    
    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)

# Запуск игры
if __name__ == "__main__":
    game = Game()
    game.run()
```

## Особенности игры "Змейка"

### Основные характеристики:
1. **Сетка игрового поля** - фон разделен на клетки для лучшей ориентации
2. **Приятная цветовая гамма** - темные тона с акцентами на змейке и еде
3. **Меню** - начальный экран с кнопками "Играть" и "Выход"
4. **Анимация поедания еды** - частицы при съедании яблока
5. **Изюминка** - телепортационные порталы

### Уникальные особенности:
- **Специальная еда**:
  - Появляется с вероятностью 15%
  - Дает +3 к длине змейки
  - Временный бонусный эффект (золотой цвет)
  
- **Телепортационные порталы**:
  - Случайно появляются на поле
  - Позволяют мгновенно перемещаться между точками
  - Исчезают после использования или через время
  
- **Визуальные эффекты**:
  - Анимированные глаза у змейки
  - Частицы при съедании еды
  - Эффекты свечения при бонусах
  - Анимированные порталы

- **Интерфейс**:
  - Подсчет очков
  - Экраны меню и окончания игры
  - Инструкции по управлению
  - Индикаторы специальных эффектов

### Управление:
- Стрелки - управление направлением движения
- ESC - переход в меню во время игры
- SPACE - перезапуск после проигрыша
- Мышь - выбор кнопок в меню

Игра сочетает классическую механику змейки с современной графикой и оригинальными игровыми элементами для создания увлекательного игрового процесса.