import pygame
import sys
import random
import math

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# Цвета
BACKGROUND = (15, 30, 45)
GRID_COLOR = (30, 50, 70)
SNAKE_COLOR = (0, 200, 150)
SNAKE_HEAD_COLOR = (0, 255, 200)
FOOD_COLOR = (255, 80, 80)
OBSTACLE_COLOR = (180, 180, 220)
TEXT_COLOR = (220, 220, 255)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER_COLOR = (100, 160, 210)
PARTICLE_COLORS = [
    (255, 215, 0),  # Золотой
    (255, 69, 0),   # Оранжево-красный
    (255, 105, 180) # Розовый
]

# Создание экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка с изюминкой")
clock = pygame.time.Clock()

# Шрифты
font_large = pygame.font.SysFont(None, 72)
font_medium = pygame.font.SysFont(None, 48)
font_small = pygame.font.SysFont(None, 32)

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(3, 8)
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(1.5, 4.0)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = random.randint(20, 40)
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
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
        self.hover_color = BUTTON_HOVER_COLOR
        self.current_color = self.color
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.current_color, self.rect, border_radius=10)
        pygame.draw.rect(surface, (200, 200, 255), self.rect, 3, border_radius=10)
        text_surf = font_small.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
    
    def is_hovered(self, pos):
        if self.rect.collidepoint(pos):
            self.current_color = self.hover_color
            return True
        self.current_color = self.color
        return False

class Snake:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.next_direction = self.direction
        self.grow = False
        self.speed = 8  # Скорость змейки (обновлений в секунду)
        self.score = 0
        self.growth_pending = 0
    
    def change_direction(self, dx, dy):
        # Предотвращение поворота на 180 градусов
        if (dx, dy) != (-self.direction[0], -self.direction[1]):
            self.next_direction = (dx, dy)
    
    def move(self):
        self.direction = self.next_direction
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        self.body.insert(0, new_head)
        
        if self.growth_pending > 0:
            self.growth_pending -= 1
        else:
            self.body.pop()
        
        # Проверка на столкновение с собой
        if self.body[0] in self.body[1:]:
            return False
        return True
    
    def grow_snake(self, amount=1):
        self.growth_pending += amount
    
    def check_collision(self, x, y):
        head = self.body[0]
        return head[0] == x and head[1] == y
    
    def draw(self, surface):
        # Рисование тела змейки
        for i, (x, y) in enumerate(self.body):
            color = SNAKE_HEAD_COLOR if i == 0 else SNAKE_COLOR
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, color, rect, border_radius=7)
            
            # Рисуем глаза для головы
            if i == 0:
                eye_size = GRID_SIZE // 5
                # Определяем положение глаз в зависимости от направления
                if self.direction == (1, 0):  # Вправо
                    pygame.draw.circle(surface, (0, 0, 0), 
                                      (x * GRID_SIZE + GRID_SIZE - eye_size*1.5, 
                                       y * GRID_SIZE + eye_size*2), eye_size)
                    pygame.draw.circle(surface, (0, 0, 0), 
                                      (x * GRID_SIZE + GRID_SIZE - eye_size*1.5, 
                                       y * GRID_SIZE + GRID_SIZE - eye_size*2), eye_size)
                elif self.direction == (-1, 0):  # Влево
                    pygame.draw.circle(surface, (0, 0, 0), 
                                      (x * GRID_SIZE + eye_size*1.5, 
                                       y * GRID_SIZE + eye_size*2), eye_size)
                    pygame.draw.circle(surface, (0, 0, 0), 
                                      (x * GRID_SIZE + eye_size*1.5, 
                                       y * GRID_SIZE + GRID_SIZE - eye_size*2), eye_size)
                elif self.direction == (0, -1):  # Вверх
                    pygame.draw.circle(surface, (0, 0, 0), 
                                      (x * GRID_SIZE + eye_size*2, 
                                       y * GRID_SIZE + eye_size*1.5), eye_size)
                    pygame.draw.circle(surface, (0, 0, 0), 
                                      (x * GRID_SIZE + GRID_SIZE - eye_size*2, 
                                       y * GRID_SIZE + eye_size*1.5), eye_size)
                else:  # Вниз
                    pygame.draw.circle(surface, (0, 0, 0), 
                                      (x * GRID_SIZE + eye_size*2, 
                                       y * GRID_SIZE + GRID_SIZE - eye_size*1.5), eye_size)
                    pygame.draw.circle(surface, (0, 0, 0), 
                                      (x * GRID_SIZE + GRID_SIZE - eye_size*2, 
                                       y * GRID_SIZE + GRID_SIZE - eye_size*1.5), eye_size)

class Food:
    def __init__(self, snake):
        self.position = self.generate_position(snake)
        self.particles = []
    
    def generate_position(self, snake):
        while True:
            position = (random.randint(1, GRID_WIDTH - 2), 
                       random.randint(1, GRID_HEIGHT - 2))
            if position not in snake.body:
                return position
    
    def draw(self, surface):
        x, y = self.position
        rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        
        # Рисуем еду с градиентом
        center = (rect.centerx, rect.centery)
        radius = GRID_SIZE // 2
        
        # Основной цвет
        pygame.draw.circle(surface, FOOD_COLOR, center, radius)
        
        # Более светлый центр
        pygame.draw.circle(surface, (255, 150, 150), center, radius // 2)
        
        # Рисуем частицы
        for particle in self.particles:
            particle.draw(surface)
    
    def create_particles(self):
        x, y = self.position
        for _ in range(15):
            color = random.choice(PARTICLE_COLORS)
            self.particles.append(
                Particle(x * GRID_SIZE + GRID_SIZE // 2, 
                         y * GRID_SIZE + GRID_SIZE // 2, 
                         color)
            )
    
    def update_particles(self):
        for i in range(len(self.particles) - 1, -1, -1):
            if not self.particles[i].update():
                self.particles.pop(i)

class Obstacle:
    def __init__(self):
        self.positions = []
        self.generate()
    
    def generate(self):
        # Генерируем 4 препятствия по углам
        self.positions = []
        for _ in range(4):
            x = random.randint(2, GRID_WIDTH - 4)
            y = random.randint(2, GRID_HEIGHT - 4)
            size = random.randint(1, 3)
            
            # Создаем квадратное препятствие
            for i in range(-size, size + 1):
                for j in range(-size, size + 1):
                    self.positions.append((x + i, y + j))
    
    def draw(self, surface):
        for x, y in self.positions:
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, OBSTACLE_COLOR, rect, border_radius=5)
            
            # Рисуем внутренний квадрат
            inner_rect = pygame.Rect(
                x * GRID_SIZE + GRID_SIZE // 4,
                y * GRID_SIZE + GRID_SIZE // 4,
                GRID_SIZE // 2,
                GRID_SIZE // 2
            )
            pygame.draw.rect(surface, (200, 200, 240), inner_rect, border_radius=3)

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.obstacles = Obstacle()
        self.particles = []
        self.state = "MENU"  # MENU, PLAYING, GAME_OVER
        self.paused = False
        self.level = 1
    
    def reset(self):
        self.snake.reset()
        self.food = Food(self.snake.body)
        self.obstacles = Obstacle()
        self.particles = []
        self.level = 1
    
    def draw_grid(self, surface):
        for x in range(0, WIDTH, GRID_SIZE):
            pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, HEIGHT), 1)
        for y in range(0, HEIGHT, GRID_SIZE):
            pygame.draw.line(surface, GRID_COLOR, (0, y), (WIDTH, y), 1)
    
    def draw_score(self, surface):
        score_text = font_small.render(f"Очки: {self.snake.score}", True, TEXT_COLOR)
        level_text = font_small.render(f"Уровень: {self.level}", True, TEXT_COLOR)
        surface.blit(score_text, (10, 10))
        surface.blit(level_text, (WIDTH - level_text.get_width() - 10, 10))
    
    def draw_menu(self, surface):
        # Заголовок
        title = font_large.render("ЗМЕЙКА", True, SNAKE_HEAD_COLOR)
        subtitle = font_medium.render("Собери специальные бонусы!", True, TEXT_COLOR)
        
        surface.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
        surface.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, HEIGHT // 4 + 80))
        
        # Кнопки
        self.play_button = Button(WIDTH // 2 - 100, HEIGHT // 2, 200, 50, "Играть")
        self.exit_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 80, 200, 50, "Выход")
        
        self.play_button.draw(surface)
        self.exit_button.draw(surface)
    
    def draw_game_over(self, surface):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))
        
        game_over = font_large.render("Игра окончена!", True, (255, 100, 100))
        score_text = font_medium.render(f"Очки: {self.snake.score}", True, TEXT_COLOR)
        
        surface.blit(game_over, (WIDTH // 2 - game_over.get_width() // 2, HEIGHT // 3))
        surface.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
        
        self.menu_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 70, 200, 50, "Меню")
        self.restart_button = Button(WIDTH // 2 - 100, HEIGHT // 2 + 130, 200, 50, "Играть снова")
        
        self.menu_button.draw(surface)
        self.restart_button.draw(surface)
    
    def update(self):
        if self.state == "PLAYING" and not self.paused:
            # Обновление частиц
            self.food.update_particles()
            for i in range(len(self.particles) - 1, -1, -1):
                if not self.particles[i].update():
                    self.particles.pop(i)
            
            # Проверка съедения еды
            if self.snake.check_collision(self.food.position[0], self.food.position[1]):
                self.snake.score += 10
                self.snake.grow_snake(1)
                
                # Создаем частицы для эффекта съедения
                self.food.create_particles()
                
                # Проверка перехода на новый уровень
                if self.snake.score % 50 == 0:
                    self.level += 1
                    # Увеличиваем скорость каждые 50 очков
                    self.snake.speed = min(20, self.snake.speed + 1)
                
                # Создаем новую еду
                self.food = Food(self.snake.body)
            
            # Проверка столкновения с препятствиями
            if self.snake.body[0] in self.obstacles.positions:
                self.state = "GAME_OVER"
            
            # Движение змейки
            if not self.snake.move():
                self.state = "GAME_OVER"
            
            # Проверка выхода за границы
            head_x, head_y = self.snake.body[0]
            if head_x < 0 or head_x >= GRID_WIDTH or head_y < 0 or head_y >= GRID_HEIGHT:
                self.state = "GAME_OVER"
    
    def draw(self, surface):
        # Фон
        surface.fill(BACKGROUND)
        self.draw_grid(surface)
        
        # Рисуем препятствия
        self.obstacles.draw(surface)
        
        # Рисуем еду
        self.food.draw(surface)
        
        # Рисуем змейку
        self.snake.draw(surface)
        
        # Рисуем частицы
        for particle in self.particles:
            particle.draw(surface)
        
        # Рисуем счет
        self.draw_score(surface)
        
        # Пауза
        if self.paused and self.state == "PLAYING":
            pause_text = font_large.render("ПАУЗА", True, (200, 200, 255))
            surface.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 50))
        
        # Меню
        if self.state == "MENU":
            self.draw_menu(surface)
        
        # Игра окончена
        if self.state == "GAME_OVER":
            self.draw_game_over(surface)

# Основной цикл игры
def main():
    game = Game()
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if game.state == "PLAYING":
                    if event.key == pygame.K_UP:
                        game.snake.change_direction(0, -1)
                    elif event.key == pygame.K_DOWN:
                        game.snake.change_direction(0, 1)
                    elif event.key == pygame.K_LEFT:
                        game.snake.change_direction(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        game.snake.change_direction(1, 0)
                    elif event.key == pygame.K_p:
                        game.paused = not game.paused
                    elif event.key == pygame.K_SPACE:
                        # "Изюминка": прыжок через препятствие с потерей очков
                        if game.snake.score >= 5:
                            head_x, head_y = game.snake.body[0]
                            if head_x > 0 and head_x < GRID_WIDTH - 1 and head_y > 0 and head_y < GRID_HEIGHT - 1:
                                game.snake.score -= 5
                                # Прыгаем на 3 клетки вперед
                                dx, dy = game.snake.direction
                                for _ in range(3):
                                    new_head = (game.snake.body[0][0] + dx, game.snake.body[0][1] + dy)
                                    game.snake.body.insert(0, new_head)
                                game.snake.body = game.snake.body[:-3]
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game.state == "MENU":
                    if game.play_button.is_hovered(mouse_pos):
                        game.state = "PLAYING"
                    elif game.exit_button.is_hovered(mouse_pos):
                        pygame.quit()
                        sys.exit()
                
                elif game.state == "GAME_OVER":
                    if game.menu_button.is_hovered(mouse_pos):
                        game.state = "MENU"
                    elif game.restart_button.is_hovered(mouse_pos):
                        game.reset()
                        game.state = "PLAYING"
        
        # Обновление игры
        game.update()
        
        # Отрисовка
        game.draw(screen)
        
        # Обновление кнопок
        if game.state == "MENU":
            game.play_button.is_hovered(mouse_pos)
            game.exit_button.is_hovered(mouse_pos)
        elif game.state == "GAME_OVER":
            game.menu_button.is_hovered(mouse_pos)
            game.restart_button.is_hovered(mouse_pos)
        
        pygame.display.flip()
        
        # Управление скоростью игры
        if game.state == "PLAYING" and not game.paused:
            clock.tick(game.snake.speed)
        else:
            clock.tick(60)

if __name__ == "__main__":
    main()
