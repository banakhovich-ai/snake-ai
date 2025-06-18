```text
Prompt
- Tokens: 64
- Time: 4101.395 ms
- Speed: 15.6 t/s
Generation
- Tokens: 4954
- Time: 1559753.296 ms
- Speed: 3.2 t/s
```

<think>
Мы создадим игру "Змейка" с использованием библиотеки Pygame.
 Требования:
 1. Игровое поле с сеткой.
 2. Приятная цветовая гамма.
 3. Меню.
 4. Анимация поедания еды.
 5. Интересная изюминка.

 Изюминка: добавим два типа еды:
   - Зеленая (обычная) - увеличивает длину змейки и добавляет 10 очков.
   - Золотая (редкая) - появляется реже, дает 50 очков, и при съедании временно увеличивает скорость змейки (на 5 секунд).

 Также добавим препятствия, которые появляются после набора определенного количества очков.

 План:
 1. Инициализация Pygame, настройка окна, цветов.
 2. Создание классов: Змейка, Еда, Препятствие.
 3. Реализация игрового цикла с меню.
 4. Реализация анимации (при съедании еды - небольшой эффект).
 5. Реализация изюминки: два типа еды, временный эффект скорости, препятствия.

 Шаги кода:
 1. Импорт библиотек.
 2. Определение констант (размеры, цвета, скорость и т.д.).
 3. Класс Snake.
 4. Класс Food (с разными типами).
 5. Класс Obstacle (препятствия).
 6. Функция отрисовки сетки.
 7. Функция отрисовки змейки, еды, препятствий.
 8. Функция отрисовки меню.
 9. Функция отрисовки счета.
10. Анимация при съедании еды (например, увеличение размера еды перед исчезновением или частицы).
11. Основной игровой цикл с меню.

 Для анимации съедания еды: при съедании еды, на ее месте появится анимация (например, круги, расходящиеся от центра).

 Для упрощения, анимация будет длиться несколько кадров. Создадим класс анимации, но можно и без него, просто список частиц.

 Реализуем простую систему частиц для анимации съедания:
   - При съедании создадим несколько частиц (кругов), которые будут расширяться и исчезать.

 Рассмотрим структуру:
   - Частица: имеет позицию, радиус, цвет, время жизни.

 Для меню: кнопки "Старт", "Выход".

 Препятствия: появятся, когда счет игрока достигнет, например, 100. Будем добавлять каждые 50 очков новое препятствие.

 Реализуем два типа еды:
   - Обычная (зеленая) - появляется всегда.
   - Золотая (желтая) - появляется с вероятностью 10% при появлении новой еды, но только если золотой еды в данный момент нет.

 Золотая еда исчезает через 5 секунд, если ее не съели.

 Эффект от золотой еды: ускорение змейки в 1.5 раза на 5 секунд.

 Давайте начнем писать код.
</think>
# Змейка на Python с PyGame

```python
import pygame
import sys
import random
import math

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = (SCREEN_HEIGHT - 100) // GRID_SIZE
GAME_AREA_HEIGHT = GRID_HEIGHT * GRID_SIZE
FPS = 10

# Цвета
BACKGROUND = (15, 20, 25)
GRID_COLOR = (30, 40, 50)
SNAKE_HEAD_COLOR = (0, 200, 150)
SNAKE_BODY_COLOR = (0, 180, 130)
FOOD_COLOR = (220, 70, 70)
SPECIAL_FOOD_COLOR = (255, 215, 0)
TEXT_COLOR = (220, 220, 220)
UI_BG_COLOR = (25, 35, 45)
UI_HIGHLIGHT = (40, 150, 120)
BUTTON_COLOR = (35, 45, 55)
BUTTON_HOVER = (50, 60, 70)

# Создание экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Змейка с изюминкой")
clock = pygame.time.Clock()

# Шрифты
font_large = pygame.font.SysFont('Arial', 48, bold=True)
font_medium = pygame.font.SysFont('Arial', 32)
font_small = pygame.font.SysFont('Arial', 24)

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
        self.invincible = 0
        
    def get_head_position(self):
        return self.positions[0]
    
    def update(self):
        head = self.get_head_position()
        x, y = self.direction
        new_x = (head[0] + x) % GRID_WIDTH
        new_y = (head[1] + y) % GRID_HEIGHT
        new_position = (new_x, new_y)
        
        # Проверка на столкновение с собой
        if new_position in self.positions[1:] and self.invincible <= 0:
            return False
        
        self.positions.insert(0, new_position)
        
        if self.grow_to > 0:
            self.grow_to -= 1
        else:
            self.positions.pop()
        
        # Обновление таймеров эффектов
        if self.speed_boost > 0:
            self.speed_boost -= 1
        if self.invincible > 0:
            self.invincible -= 1
        
        return True
    
    def grow(self, amount=1):
        self.grow_to += amount
    
    def render(self, surface):
        for i, pos in enumerate(self.positions):
            color = SNAKE_HEAD_COLOR if i == 0 else SNAKE_BODY_COLOR
            
            # Эффект мерцания при неуязвимости
            if i == 0 and self.invincible > 0 and self.invincible % 4 < 2:
                color = (255, 255, 255)
                
            rect = pygame.Rect(pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, (0, 0, 0), rect, 1)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = FOOD_COLOR
        self.randomize_position()
        self.special_timer = 0
        self.special_active = False
        
    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), 
                        random.randint(0, GRID_HEIGHT - 1))
        
    def update(self, snake_positions):
        # Обновляем таймер специальной еды
        if not self.special_active:
            self.special_timer += 1
            if self.special_timer >= 15:  # Специальная еда появляется каждые 15 съеденных обычных
                self.special_active = True
                self.special_timer = 0
        
    def render(self, surface):
        # Обычная еда
        rect = pygame.Rect(self.position[0] * GRID_SIZE, 
                          self.position[1] * GRID_SIZE, 
                          GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, (0, 0, 0), rect, 1)
        
        # Специальная еда (если активна)
        if self.special_active:
            special_pos = (self.position[0] * GRID_SIZE + GRID_SIZE//2, 
                           self.position[1] * GRID_SIZE + GRID_SIZE//2)
            pygame.draw.circle(surface, SPECIAL_FOOD_COLOR, special_pos, GRID_SIZE//2)
            pygame.draw.circle(surface, (150, 100, 0), special_pos, GRID_SIZE//2, 1)

class Particle:
    def __init__(self, position, color):
        self.x, self.y = position
        self.color = color
        self.size = random.randint(3, 8)
        self.speed_x = random.uniform(-2, 2)
        self.speed_y = random.uniform(-2, 2)
        self.lifetime = random.randint(20, 40)
        
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.lifetime -= 1
        return self.lifetime > 0
        
    def render(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)

class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.hovered = False
        
    def render(self, surface):
        color = BUTTON_HOVER if self.hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, UI_HIGHLIGHT, self.rect, 3, border_radius=10)
        
        text_surf = font_medium.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered:
                return self.action
        return None

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.particles = []
        self.state = "menu"  # "menu", "game", "game_over"
        self.score = 0
        self.high_score = 0
        self.special_eaten = False
        
        # Создание кнопок
        button_width, button_height = 200, 60
        center_x = SCREEN_WIDTH // 2 - button_width // 2
        self.play_button = Button(center_x, 250, button_width, button_height, "Играть", self.start_game)
        self.quit_button = Button(center_x, 350, button_width, button_height, "Выход", self.quit_game)
        
    def start_game(self):
        self.state = "game"
        self.snake.reset()
        self.food.randomize_position()
        self.food.special_timer = 0
        self.food.special_active = False
        self.score = 0
        self.special_eaten = False
        
    def quit_game(self):
        pygame.quit()
        sys.exit()
        
    def spawn_particles(self, position, count=20):
        for _ in range(count):
            self.particles.append(Particle(
                (position[0] * GRID_SIZE + GRID_SIZE//2, 
                 position[1] * GRID_SIZE + GRID_SIZE//2),
                SPECIAL_FOOD_COLOR if self.special_eaten else FOOD_COLOR
            ))
    
    def update(self):
        if self.state == "game":
            # Обновление змейки
            if not self.snake.update():
                self.state = "game_over"
                if self.score > self.high_score:
                    self.high_score = self.score
            
            # Обновление еды
            self.food.update(self.snake.positions)
            
            # Проверка съедания еды
            if self.snake.get_head_position() == self.food.position:
                self.score += 1
                self.snake.grow(1)
                self.spawn_particles(self.food.position)
                self.food.randomize_position()
                self.special_eaten = False
                
                # Проверка на специальную еду
                if self.food.special_active:
                    self.score += 5
                    self.snake.grow(3)
                    self.snake.speed_boost = 20
                    self.snake.invincible = 30
                    self.food.special_active = False
                    self.special_eaten = True
            
            # Обновление частиц
            self.particles = [p for p in self.particles if p.update()]
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            # Обработка кнопок
            if self.state == "menu" or self.state == "game_over":
                result = self.play_button.handle_event(event)
                if result == self.start_game:
                    self.start_game()
                
                result = self.quit_button.handle_event(event)
                if result == self.quit_game:
                    self.quit_game()
            
            # Управление змейкой
            if self.state == "game":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.snake.direction != (0, 1):
                        self.snake.direction = (0, -1)
                    elif event.key == pygame.K_DOWN and self.snake.direction != (0, -1):
                        self.snake.direction = (0, 1)
                    elif event.key == pygame.K_LEFT and self.snake.direction != (1, 0):
                        self.snake.direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and self.snake.direction != (-1, 0):
                        self.snake.direction = (1, 0)
                    elif event.key == pygame.K_SPACE:
                        self.snake.grow(1)
            
            # Перезапуск игры
            if self.state == "game_over" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.start_game()
    
    def render(self):
        # Отрисовка фона
        screen.fill(BACKGROUND)
        
        # Отрисовка игрового поля
        game_surface = pygame.Surface((SCREEN_WIDTH, GAME_AREA_HEIGHT))
        game_surface.fill(BACKGROUND)
        
        # Отрисовка сетки
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(game_surface, GRID_COLOR, (x, 0), (x, GAME_AREA_HEIGHT))
        for y in range(0, GAME_AREA_HEIGHT, GRID_SIZE):
            pygame.draw.line(game_surface, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))
        
        # Отрисовка игровых объектов
        if self.state != "menu":
            self.food.render(game_surface)
            self.snake.render(game_surface)
            
            # Отрисовка частиц
            for particle in self.particles:
                particle.render(game_surface)
        
        screen.blit(game_surface, (0, 0))
        
        # Отрисовка UI
        ui_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT - GAME_AREA_HEIGHT))
        ui_surface.fill(UI_BG_COLOR)
        
        # Отрисовка меню
        if self.state == "menu":
            title = font_large.render("ЗМЕЙКА", True, UI_HIGHLIGHT)
            screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))
            
            self.play_button.render(screen)
            self.quit_button.render(screen)
            
            # Отрисовка подсказки
            hint = font_small.render("Собирайте красную еду, избегайте столкновений с собой", True, TEXT_COLOR)
            screen.blit(hint, (SCREEN_WIDTH//2 - hint.get_width()//2, 450))
            
        # Отрисовка игры
        elif self.state == "game" or self.state == "game_over":
            # Отрисовка счета
            score_text = font_medium.render(f"Очки: {self.score}", True, TEXT_COLOR)
            screen.blit(score_text, (20, GAME_AREA_HEIGHT + 20))
            
            high_score_text = font_medium.render(f"Рекорд: {self.high_score}", True, TEXT_COLOR)
            screen.blit(high_score_text, (SCREEN_WIDTH - high_score_text.get_width() - 20, GAME_AREA_HEIGHT + 20))
            
            # Отрисовка эффектов
            if self.snake.speed_boost > 0:
                boost_text = font_small.render(f"Ускорение: {self.snake.speed_boost//10 + 1}", True, (255, 215, 0))
                screen.blit(boost_text, (SCREEN_WIDTH//2 - boost_text.get_width()//2, GAME_AREA_HEIGHT + 30))
            
            if self.snake.invincible > 0:
                inv_text = font_small.render(f"Неуязвимость: {self.snake.invincible//10 + 1}", True, (0, 200, 255))
                screen.blit(inv_text, (SCREEN_WIDTH//2 - inv_text.get_width()//2, GAME_AREA_HEIGHT + 60))
        
        # Отрисовка экрана завершения игры
        if self.state == "game_over":
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            
            game_over_text = font_large.render("ИГРА ОКОНЧЕНА", True, (220, 70, 70))
            screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, 150))
            
            score_text = font_medium.render(f"Ваш счет: {self.score}", True, TEXT_COLOR)
            screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 250))
            
            restart_text = font_medium.render("Нажмите ENTER для новой игры", True, TEXT_COLOR)
            screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, 350))
    
    def run(self):
        while True:
            mouse_pos = pygame.mouse.get_pos()
            
            # Обновление кнопок
            if self.state == "menu" or self.state == "game_over":
                self.play_button.check_hover(mouse_pos)
                self.quit_button.check_hover(mouse_pos)
            
            self.handle_events()
            self.update()
            self.render()
            
            pygame.display.flip()
            
            # Управление скоростью
            if self.state == "game":
                if self.snake.speed_boost > 0:
                    clock.tick(FPS * 2)  # Ускорение в 2 раза
                else:
                    clock.tick(FPS)
            else:
                clock.tick(FPS)

# Запуск игры
if __name__ == "__main__":
    game = Game()
    game.run()
```

## Особенности игры:

1. **Приятная цветовая гамма** - Тёмно-синий фон с зелёной змейкой и красной едой создают современный вид.

2. **Сетка игрового поля** - Чёткая сетка помогает ориентироваться в пространстве.

3. **Меню с кнопками** - Интуитивно понятное меню с кнопками "Играть" и "Выход".

4. **Анимация поедания еды** - При съедании еды появляются частицы для визуального эффекта.

5. **Изюминки**:
   - **Специальная еда**:
     - Появляется периодически
     - Даёт 5 дополнительных очков
     - Увеличивает длину змейки на 3 сегмента
     - Даёт временное ускорение
     - Даёт временную неуязвимость
   - **Эффекты**:
     - Ускорение отображается в интерфейсе
     - Неуязвимость подсвечивает голову змейки
     - Мерцающий эффект при специальных состояниях
   - **Система частиц** при съедании еды
   - **Таблица рекордов** - сохранение лучшего результата
   - **Подробный интерфейс** с отображением текущих эффектов

Для управления используйте стрелки на клавиатуре. Пробел позволяет временно увеличить длину змейки (для тестирования).