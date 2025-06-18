import pygame
import sys
import random
import math
from enum import Enum

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
BACKGROUND = (15, 15, 30)
GRID_COLOR = (30, 30, 50)
SNAKE_COLOR = (50, 205, 50)
SNAKE_HEAD_COLOR = (0, 255, 127)
FOOD_COLOR = (220, 20, 60)
BONUS_COLOR = (255, 215, 0)
OBSTACLE_COLOR = (139, 0, 139)
TEXT_COLOR = (200, 200, 255)
MENU_BG = (25, 25, 50, 200)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER = (100, 160, 210)
BUTTON_TEXT = (230, 230, 255)

# Направления
class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = Direction.RIGHT
        self.grow = False
        self.score = 0
        self.bonus_active = False
        self.bonus_timer = 0
        
    def move(self):
        head_x, head_y = self.body[0]
        
        if self.direction == Direction.UP:
            new_head = (head_x, head_y - 1)
        elif self.direction == Direction.DOWN:
            new_head = (head_x, head_y + 1)
        elif self.direction == Direction.LEFT:
            new_head = (head_x - 1, head_y)
        elif self.direction == Direction.RIGHT:
            new_head = (head_x + 1, head_y)
            
        self.body.insert(0, new_head)
        
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
    
    def change_direction(self, new_direction):
        # Предотвращение поворота на 180 градусов
        if (new_direction == Direction.UP and self.direction != Direction.DOWN) or \
           (new_direction == Direction.DOWN and self.direction != Direction.UP) or \
           (new_direction == Direction.LEFT and self.direction != Direction.RIGHT) or \
           (new_direction == Direction.RIGHT and self.direction != Direction.LEFT):
            self.direction = new_direction
    
    def grow_snake(self):
        self.grow = True
        self.score += 1
        
    def activate_bonus(self, duration):
        self.bonus_active = True
        self.bonus_timer = duration
        
    def update_bonus(self):
        if self.bonus_active:
            self.bonus_timer -= 1
            if self.bonus_timer <= 0:
                self.bonus_active = False
    
    def check_collision(self):
        head = self.body[0]
        
        # Проверка границ
        if head[0] < 0 or head[0] >= GRID_WIDTH or head[1] < 0 or head[1] >= GRID_HEIGHT:
            return True
            
        # Проверка столкновения с телом
        if head in self.body[1:]:
            return True
            
        return False

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 24)
        self.title_font = pygame.font.SysFont('Arial', 48, bold=True)
        self.snake = Snake()
        self.food = self.generate_food()
        self.obstacles = []
        self.bonus_food = None
        self.bonus_spawn_timer = 0
        self.game_state = "MENU"  # MENU, PLAYING, GAME_OVER
        self.animation_particles = []
        self.spawn_obstacles()
        
    def generate_food(self):
        while True:
            food_pos = (random.randint(0, GRID_WIDTH - 1), (random.randint(0, GRID_HEIGHT - 1))
            if food_pos not in self.snake.body and food_pos not in self.obstacles:
                return food_pos
                
    def spawn_bonus_food(self):
        if self.bonus_spawn_timer <= 0 and not self.bonus_food:
            while True:
                bonus_pos = (random.randint(0, GRID_WIDTH - 1), (random.randint(0, GRID_HEIGHT - 1))
                if bonus_pos not in self.snake.body and bonus_pos not in self.obstacles and bonus_pos != self.food:
                    self.bonus_food = bonus_pos
                    self.bonus_spawn_timer = 100  # Время до следующего появления бонуса
                    break
    
    def spawn_obstacles(self):
        self.obstacles = []
        num_obstacles = min(10, self.snake.score // 2)  # Увеличиваем количество препятствий с ростом счета
        
        for _ in range(num_obstacles):
            while True:
                obstacle_pos = (random.randint(0, GRID_WIDTH - 1), (random.randint(0, GRID_HEIGHT - 1))
                if (obstacle_pos not in self.snake.body and 
                    obstacle_pos != self.food and 
                    (not self.bonus_food or obstacle_pos != self.bonus_food) and
                    obstacle_pos != (GRID_WIDTH // 2, GRID_HEIGHT // 2)):  # Не спавнить в начальной позиции
                    self.obstacles.append(obstacle_pos)
                    break
    
    def check_food_collision(self):
        if self.snake.body[0] == self.food:
            self.snake.grow_snake()
            self.food = self.generate_food()
            self.spawn_obstacles()
            
            # Добавляем анимацию
            for _ in range(10):
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(1, 3)
                particle = {
                    'pos': (self.food[0] * GRID_SIZE + GRID_SIZE // 2, self.food[1] * GRID_SIZE + GRID_SIZE // 2),
                    'vel': (math.cos(angle) * speed, math.sin(angle) * speed),
                    'size': random.randint(2, 5),
                    'life': 20
                }
                self.animation_particles.append(particle)
            
        if self.bonus_food and self.snake.body[0] == self.bonus_food:
            self.snake.grow_snake()
            self.snake.grow_snake()  # Двойной рост за бонус
            self.snake.activate_bonus(30)  # Активируем бонус на 30 кадров
            self.bonus_food = None
            
    def update(self):
        if self.game_state == "PLAYING":
            self.snake.move()
            self.snake.update_bonus()
            
            if self.snake.check_collision() or self.snake.body[0] in self.obstacles:
                self.game_state = "GAME_OVER"
            
            self.check_food_collision()
            
            # Обновление бонусной еды
            if self.bonus_food:
                self.bonus_spawn_timer -= 1
                if self.bonus_spawn_timer <= 0:
                    self.bonus_food = None
            
            # Спавн новой бонусной еды
            if not self.bonus_food:
                self.bonus_spawn_timer -= 1
                if self.bonus_spawn_timer <= 0:
                    self.spawn_bonus_food()
            
            # Обновление анимации частиц
            for particle in self.animation_particles[:]:
                particle['pos'] = (particle['pos'][0] + particle['vel'][0], 
                                  particle['pos'][1] + particle['vel'][1])
                particle['life'] -= 1
                if particle['life'] <= 0:
                    self.animation_particles.remove(particle)
    
    def draw(self):
        self.screen.fill(BACKGROUND)
        
        # Рисуем сетку
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))
        
        # Рисуем препятствия
        for obstacle in self.obstacles:
            pygame.draw.rect(self.screen, OBSTACLE_COLOR, 
                           (obstacle[0] * GRID_SIZE, obstacle[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            # Рисуем узор на препятствии
            pygame.draw.line(self.screen, (180, 50, 200), 
                           (obstacle[0] * GRID_SIZE, obstacle[1] * GRID_SIZE),
                           (obstacle[0] * GRID_SIZE + GRID_SIZE, obstacle[1] * GRID_SIZE + GRID_SIZE), 2)
            pygame.draw.line(self.screen, (180, 50, 200), 
                           (obstacle[0] * GRID_SIZE + GRID_SIZE, obstacle[1] * GRID_SIZE),
                           (obstacle[0] * GRID_SIZE, obstacle[1] * GRID_SIZE + GRID_SIZE), 2)
        
        # Рисуем змею
        for i, segment in enumerate(self.snake.body):
            color = SNAKE_HEAD_COLOR if i == 0 else SNAKE_COLOR
            pygame.draw.rect(self.screen, color, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            # Рисуем глаза у головы
            if i == 0:
                eye_size = GRID_SIZE // 4
                if self.snake.direction == Direction.RIGHT:
                    pygame.draw.circle(self.screen, (0, 0, 0), (segment[0] * GRID_SIZE + GRID_SIZE - eye_size, segment[1] * GRID_SIZE + eye_size * 2), eye_size)
                    pygame.draw.circle(self.screen, (0, 0, 0), (segment[0] * GRID_SIZE + GRID_SIZE - eye_size, segment[1] * GRID_SIZE + GRID_SIZE - eye_size * 2), eye_size)
                elif self.snake.direction == Direction.LEFT:
                    pygame.draw.circle(self.screen, (0, 0, 0), (segment[0] * GRID_SIZE + eye_size, segment[1] * GRID_SIZE + eye_size * 2), eye_size)
                    pygame.draw.circle(self.screen, (0, 0, 0), (segment[0] * GRID_SIZE + eye_size, segment[1] * GRID_SIZE + GRID_SIZE - eye_size * 2), eye_size)
                elif self.snake.direction == Direction.UP:
                    pygame.draw.circle(self.screen, (0, 0, 0), (segment[0] * GRID_SIZE + eye_size * 2, segment[1] * GRID_SIZE + eye_size), eye_size)
                    pygame.draw.circle(self.screen, (0, 0, 0), (segment[0] * GRID_SIZE + GRID_SIZE - eye_size * 2, segment[1] * GRID_SIZE + eye_size), eye_size)
                elif self.snake.direction == Direction.DOWN:
                    pygame.draw.circle(self.screen, (0, 0, 0), (segment[0] * GRID_SIZE + eye_size * 2, segment[1] * GRID_SIZE + GRID_SIZE - eye_size), eye_size)
                    pygame.draw.circle(self.screen, (0, 0, 0), (segment[0] * GRID_SIZE + GRID_SIZE - eye_size * 2, segment[1] * GRID_SIZE + GRID_SIZE - eye_size), eye_size)
        
        # Рисуем еду
        pygame.draw.rect(self.screen, FOOD_COLOR, (self.food[0] * GRID_SIZE, self.food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        # Рисуем блик на еде
        pygame.draw.circle(self.screen, (255, 150, 150), 
                          (self.food[0] * GRID_SIZE + GRID_SIZE // 4, self.food[1] * GRID_SIZE + GRID_SIZE // 4), 
                          GRID_SIZE // 6)
        
        # Рисуем бонусную еду (если есть)
        if self.bonus_food:
            pygame.draw.rect(self.screen, BONUS_COLOR, 
                           (self.bonus_food[0] * GRID_SIZE, self.bonus_food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            # Рисуем звезду
            center_x = self.bonus_food[0] * GRID_SIZE + GRID_SIZE // 2
            center_y = self.bonus_food[1] * GRID_SIZE + GRID_SIZE // 2
            pygame.draw.circle(self.screen, (255, 255, 200), (center_x, center_y), GRID_SIZE // 3)
            pygame.draw.circle(self.screen, BONUS_COLOR, (center_x, center_y), GRID_SIZE // 5)
        
        # Рисуем анимационные частицы
        for particle in self.animation_particles:
            alpha = min(255, particle['life'] * 12)
            color = (255, 200, 100, alpha)
            pygame.draw.circle(self.screen, color, (int(particle['pos'][0]), int(particle['pos'][1])), particle['size'])
        
        # Рисуем счет
        score_text = self.font.render(f'Score: {self.snake.score}', True, TEXT_COLOR)
        self.screen.blit(score_text, (10, 10))
        
        # Рисуем индикатор бонуса
        if self.snake.bonus_active:
            bonus_text = self.font.render('SPEED BOOST!', True, BONUS_COLOR)
            self.screen.blit(bonus_text, (SCREEN_WIDTH - 150, 10))
        
        # Рисуем меню или экран завершения игры
        if self.game_state == "MENU":
            self.draw_menu()
        elif self.game_state == "GAME_OVER":
            self.draw_game_over()
    
    def draw_menu(self):
        # Полупрозрачный фон
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        s.fill(MENU_BG)
        self.screen.blit(s, (0, 0))
        
        # Заголовок
        title = self.title_font.render('SNAKE GAME', True, SNAKE_HEAD_COLOR)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 4))
        
        # Кнопка старта
        start_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
        mouse_pos = pygame.mouse.get_pos()
        hover = start_rect.collidePoint(mouse_pos) if mouse_pos else False
        
        pygame.draw.rect(self.screen, BUTTON_HOVER if hover else BUTTON_COLOR, start_rect, border_radius=10)
        pygame.draw.rect(self.screen, TEXT_COLOR, start_rect, 3, border_radius=10)
        
        start_text = self.font.render('START GAME', True, BUTTON_TEXT)
        self.screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 + 15))
        
        # Инструкции
        inst = [
            "Используйте стрелки для управления",
            "Съедайте красную еду - растете",
            "Золотая еда дает двойной рост и скорость",
            "Избегайте фиолетовых препятствий!",
            "Нажмите ESC для выхода"
        ]
        
        for i, text in enumerate(inst):
            inst_text = self.font.render(text, True, TEXT_COLOR)
            self.screen.blit(inst_text, (SCREEN_WIDTH // 2 - inst_text.get_width() // 2, SCREEN_HEIGHT // 1.8 + i * 30))
        
        return start_rect
    
    def draw_game_over(self):
        # Полупрозрачный фон
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        s.fill((50, 0, 0, 180))
        self.screen.blit(s, (0, 0))
        
        # Текст Game Over
        game_over = self.title_font.render('GAME OVER', True, FOOD_COLOR)
        self.screen.blit(game_over, (SCREEN_WIDTH // 2 - game_over.get_width() // 2, SCREEN_HEIGHT // 3))
        
        # Счет
        score_text = self.font.render(f'Final Score: {self.snake.score}', True, TEXT_COLOR)
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
        
        # Кнопка рестарта
        restart_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 1.7, 200, 50)
        mouse_pos = pygame.mouse.get_pos()
        hover = restart_rect.collidePoint(mouse_pos) if mouse_pos else False
        
        pygame.draw.rect(self.screen, BUTTON_HOVER if hover else BUTTON_COLOR, restart_rect, border_radius=10)
        pygame.draw.rect(self.screen, TEXT_COLOR, restart_rect, 3, border_radius=10)
        
        restart_text = self.font.render('PLAY AGAIN', True, BUTTON_TEXT)
        self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 1.7 + 15))
        
        return restart_rect
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if self.game_state == "PLAYING":
                    if event.key == pygame.K_UP:
                        self.snake.change_direction(Direction.UP)
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction(Direction.DOWN)
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction(Direction.LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction(Direction.RIGHT)
                    elif event.key == pygame.K_ESCAPE:
                        self.game_state = "MENU"
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if self.game_state == "MENU":
                    start_rect = self.draw_menu()
                    if start_rect.collidepoint(mouse_pos):
                        self.snake.reset()
                        self.food = self.generate_food()
                        self.obstacles = []
                        self.bonus_food = None
                        self.game_state = "PLAYING"
                        self.spawn_obstacles()
                        
                elif self.game_state == "GAME_OVER":
                    restart_rect = self.draw_game_over()
                    if restart_rect.collidepoint(mouse_pos):
                        self.snake.reset()
                        self.food = self.generate_food()
                        self.obstacles = []
                        self.bonus_food = None
                        self.game_state = "PLAYING"
                        self.spawn_obstacles()
    
    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS + (5 if self.snake.bonus_active else 0))  # Увеличиваем скорость при бонусе

if __name__ == "__main__":
    game = Game()
    game.run()
