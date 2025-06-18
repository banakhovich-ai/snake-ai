import pygame
import sys
import random
import math
from pygame.locals import *

# Инициализация Pygame
pygame.init()
pygame.font.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
FPS = 10

# Цвета
BACKGROUND = (20, 20, 30)
GRID_COLOR = (40, 40, 60)
SNAKE_COLOR = (0, 200, 100)
SNAKE_HEAD_COLOR = (0, 230, 120)
FOOD_COLOR = (255, 50, 50)
SPECIAL_FOOD_COLOR = (255, 200, 0)
TEXT_COLOR = (230, 230, 250)
BUTTON_COLOR = (70, 70, 100)
BUTTON_HOVER_COLOR = (90, 90, 130)
BUTTON_TEXT_COLOR = (230, 230, 250)

# Направления
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.hovered = False
        
    def draw(self, surface):
        color = BUTTON_HOVER_COLOR if self.hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        pygame.draw.rect(surface, (120, 120, 160), self.rect, 2, border_radius=5)
        
        font = pygame.font.SysFont(None, 32)
        text_surf = font.render(self.text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def handle_event(self, event):
        if event.type == MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == MOUSEBUTTONDOWN:
            if self.hovered and self.action:
                self.action()
                return True
        return False

class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        for i in range(1, self.length):
            self.positions.append((self.positions[0][0] - i, self.positions[0][1]))
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.score = 0
        self.growth_pending = 0
        self.special_mode = False
        self.special_timer = 0
        
    def get_head_position(self):
        return self.positions[0]
        
    def update_direction(self):
        self.direction = self.next_direction
        
    def move(self):
        head = self.get_head_position()
        x, y = self.direction
        
        # Изюминка: прохождение сквозь стены
        new_x = (head[0] + x) % GRID_WIDTH
        new_y = (head[1] + y) % GRID_HEIGHT
        new_position = (new_x, new_y)
        
        # Проверка столкновения с собой
        if new_position in self.positions[1:]:
            return False
            
        self.positions.insert(0, new_position)
        
        if self.growth_pending > 0:
            self.growth_pending -= 1
        else:
            self.positions.pop()
            
        return True
        
    def grow(self, amount=1):
        self.growth_pending += amount
        
    def draw(self, surface):
        for i, pos in enumerate(self.positions):
            color = SNAKE_HEAD_COLOR if i == 0 else SNAKE_COLOR
            rect = pygame.Rect((pos[0] * GRID_SIZE, pos[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, (0, 150, 70), rect, 1)
            
            # Рисуем глаза на голове
            if i == 0:
                eye_size = GRID_SIZE // 5
                eye_offset = GRID_SIZE // 4
                
                # Определяем направление для размещения глаз
                if self.direction == UP or self.direction == DOWN:
                    left_eye = (pos[0] * GRID_SIZE + eye_offset, pos[1] * GRID_SIZE + eye_offset)
                    right_eye = (pos[0] * GRID_SIZE + GRID_SIZE - eye_offset, pos[1] * GRID_SIZE + eye_offset)
                else:
                    left_eye = (pos[0] * GRID_SIZE + eye_offset, pos[1] * GRID_SIZE + eye_offset)
                    right_eye = (pos[0] * GRID_SIZE + eye_offset, pos[1] * GRID_SIZE + GRID_SIZE - eye_offset)
                
                pygame.draw.circle(surface, (0, 0, 0), left_eye, eye_size)
                pygame.draw.circle(surface, (0, 0, 0), right_eye, eye_size)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = FOOD_COLOR
        self.special = False
        self.spawn()
        
    def spawn(self, snake_positions=None):
        while True:
            self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if snake_positions is None or self.position not in snake_positions:
                break
                
        # 20% шанс появления особой еды
        self.special = random.random() < 0.2
        self.color = SPECIAL_FOOD_COLOR if self.special else FOOD_COLOR
        self.spawn_time = pygame.time.get_ticks()
        
    def draw(self, surface):
        rect = pygame.Rect((self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.color, rect)
        
        # Рисуем дополнительную деталь для особой еды
        if self.special:
            inner_rect = pygame.Rect(
                (self.position[0] * GRID_SIZE + GRID_SIZE//4, 
                 self.position[1] * GRID_SIZE + GRID_SIZE//4), 
                (GRID_SIZE//2, GRID_SIZE//2)
            )
            pygame.draw.rect(surface, (255, 255, 200), inner_rect)
            
            # Пульсация для особой еды
            elapsed = pygame.time.get_ticks() - self.spawn_time
            pulse = (math.sin(elapsed / 200) + 1) * 0.2 + 0.6
            pulse_size = int(GRID_SIZE * pulse)
            pulse_rect = pygame.Rect(
                (self.position[0] * GRID_SIZE + (GRID_SIZE - pulse_size) // 2, 
                 self.position[1] * GRID_SIZE + (GRID_SIZE - pulse_size) // 2),
                (pulse_size, pulse_size)
            )
            pygame.draw.rect(surface, (255, 255, 200, 150), pulse_rect, 2)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Змейка с изюминкой")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 24)
        
        self.snake = Snake()
        self.food = Food()
        self.food.spawn(self.snake.positions)
        
        self.game_state = "menu"  # menu, playing, game_over
        self.animation_particles = []
        
        # Создаем кнопки для меню
        self.menu_buttons = [
            Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 30, 200, 50, "Начать игру", self.start_game),
            Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 40, 200, 50, "Выход", self.quit_game)
        ]
        
        # Создаем кнопки для экрана завершения игры
        self.game_over_buttons = [
            Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 40, 200, 50, "Играть снова", self.restart_game),
            Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 100, 200, 50, "В меню", self.return_to_menu)
        ]
        
    def start_game(self):
        self.game_state = "playing"
        self.snake.reset()
        self.food.spawn(self.snake.positions)
        
    def restart_game(self):
        self.snake.reset()
        self.food.spawn(self.snake.positions)
        self.game_state = "playing"
        
    def return_to_menu(self):
        self.game_state = "menu"
        
    def quit_game(self):
        pygame.quit()
        sys.exit()
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            if self.game_state == "menu":
                for button in self.menu_buttons:
                    button.handle_event(event)
                    
            elif self.game_state == "playing":
                if event.type == KEYDOWN:
                    if event.key == K_UP and self.snake.direction != DOWN:
                        self.snake.next_direction = UP
                    elif event.key == K_DOWN and self.snake.direction != UP:
                        self.snake.next_direction = DOWN
                    elif event.key == K_LEFT and self.snake.direction != RIGHT:
                        self.snake.next_direction = LEFT
                    elif event.key == K_RIGHT and self.snake.direction != LEFT:
                        self.snake.next_direction = RIGHT
                    elif event.key == K_ESCAPE:
                        self.game_state = "menu"
                        
            elif self.game_state == "game_over":
                for button in self.game_over_buttons:
                    button.handle_event(event)
                    
    def update(self):
        if self.game_state == "playing":
            self.snake.update_direction()
            if not self.snake.move():
                self.game_state = "game_over"
                
            # Проверка съедения еды
            head = self.snake.get_head_position()
            if head == self.food.position:
                # Анимация поедания
                self.create_eating_animation(head)
                
                # Обычная еда
                if not self.food.special:
                    self.snake.grow()
                    self.snake.score += 1
                # Особенная еда
                else:
                    self.snake.grow(3)
                    self.snake.score += 3
                    self.snake.special_mode = True
                    self.snake.special_timer = 50  # 50 кадров особого режима
                    
                self.food.spawn(self.snake.positions)
                
            # Обновление особого режима
            if self.snake.special_mode:
                self.snake.special_timer -= 1
                if self.snake.special_timer <= 0:
                    self.snake.special_mode = False
                    
            # Обновление анимации частиц
            for particle in self.animation_particles[:]:
                particle[2] -= 1  # Уменьшаем размер
                particle[3] -= 1  # Уменьшаем время жизни
                if particle[3] <= 0:
                    self.animation_particles.remove(particle)
                    
    def create_eating_animation(self, position):
        # Создаем несколько частиц для анимации
        for _ in range(10):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 3)
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            size = random.randint(3, 8)
            lifetime = random.randint(20, 40)
            color = (random.randint(200, 255), random.randint(100, 200), random.randint(50, 150))
            self.animation_particles.append([
                position[0] * GRID_SIZE + GRID_SIZE//2,  # x
                position[1] * GRID_SIZE + GRID_SIZE//2,  # y
                size,  # начальный размер
                lifetime,  # время жизни
                dx,  # скорость по x
                dy,  # скорость по y
                color  # цвет
            ])
        
    def draw_grid(self):
        # Задний фон
        self.screen.fill(BACKGROUND)
        
        # Рисуем сетку
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y), 1)
            
    def draw_score(self):
        score_text = self.font.render(f"Очки: {self.snake.score}", True, TEXT_COLOR)
        self.screen.blit(score_text, (10, 10))
        
        # Если в особом режиме, показываем индикатор
        if self.snake.special_mode:
            mode_text = self.font.render("СУПЕР РЕЖИМ!", True, (255, 255, 0))
            self.screen.blit(mode_text, (SCREEN_WIDTH - mode_text.get_width() - 10, 10))
            
    def draw_menu(self):
        title_font = pygame.font.SysFont(None, 64)
        title_text = title_font.render("ЗМЕЙКА", True, (0, 200, 150))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4))
        self.screen.blit(title_text, title_rect)
        
        subtitle = self.font.render("Особая версия: проходи сквозь стены!", True, TEXT_COLOR)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4 + 60))
        self.screen.blit(subtitle, subtitle_rect)
        
        for button in self.menu_buttons:
            button.draw(self.screen)
            
    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        game_over_font = pygame.font.SysFont(None, 72)
        game_over_text = game_over_font.render("ИГРА ОКОНЧЕНА", True, (200, 50, 50))
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
        self.screen.blit(game_over_text, game_over_rect)
        
        score_text = self.font.render(f"Ваш счет: {self.snake.score}", True, TEXT_COLOR)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        self.screen.blit(score_text, score_rect)
        
        for button in self.game_over_buttons:
            button.draw(self.screen)
            
    def draw_particles(self):
        for particle in self.animation_particles:
            x, y, size, _, dx, dy, color = particle
            # Обновляем позицию частицы
            particle[0] += dx
            particle[1] += dy
            # Рисуем частицу
            pygame.draw.circle(self.screen, color, (int(particle[0]), int(particle[1])), int(size))
        
    def draw(self):
        self.draw_grid()
        
        if self.game_state == "playing":
            self.food.draw(self.screen)
            self.snake.draw(self.screen)
            self.draw_score()
            self.draw_particles()
            
        elif self.game_state == "menu":
            self.draw_menu()
            
        elif self.game_state == "game_over":
            self.food.draw(self.screen)
            self.snake.draw(self.screen)
            self.draw_score()
            self.draw_game_over()
            self.draw_particles()
            
    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            
            pygame.display.update()
            self.clock.tick(FPS)

# Запуск игры
if __name__ == "__main__":
    game = Game()
    game.run()
