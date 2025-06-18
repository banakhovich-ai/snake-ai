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
