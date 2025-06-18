import pygame
import sys
import random
import time

# Инициализация Pygame
pygame.init()

# Размеры экрана
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# Цвета
BACKGROUND = (15, 35, 45)  # Темно-синий
GRID_COLOR = (25, 55, 70)  # Синий с оттенком серого
SNAKE_COLOR = (100, 200, 100)  # Зеленый
SNAKE_HEAD_COLOR = (120, 240, 120)  # Яркий зеленый
FOOD_COLOR = (255, 100, 100)  # Красный
TEXT_COLOR = (220, 220, 220)  # Светло-серый
BUTTON_COLOR = (70, 130, 180)  # Голубой
BUTTON_HOVER_COLOR = (90, 150, 200)  # Светло-голубой
OBSTACLE_COLOR = (180, 70, 70)  # Кирпично-красный
PARTICLE_COLORS = [(255, 215, 0), (255, 140, 0), (255, 69, 0)]  # Желтый, оранжевый, красный

# Создание экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка с Изюминкой")
clock = pygame.time.Clock()

# Шрифты
font = pygame.font.SysFont('Arial', 32)
small_font = pygame.font.SysFont('Arial', 24)

class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN])
        self.score = 0
        self.grow = False
        
    def get_head_position(self):
        return self.positions[0]
    
    def update(self):
        head = self.get_head_position()
        x, y = head
        
        if self.direction == pygame.K_RIGHT:
            x = (x + GRID_SIZE) % WIDTH
        elif self.direction == pygame.K_LEFT:
            x = (x - GRID_SIZE) % WIDTH
        elif self.direction == pygame.K_UP:
            y = (y - GRID_SIZE) % HEIGHT
        elif self.direction == pygame.K_DOWN:
            y = (y + GRID_SIZE) % HEIGHT
            
        self.positions.insert(0, (x, y))
        
        if not self.grow:
            self.positions.pop()
        else:
            self.grow = False
            self.length += 1
    
    def draw(self, surface):
        for i, pos in enumerate(self.positions):
            # Рисуем голову змейки другим цветом
            if i == 0:
                pygame.draw.rect(surface, SNAKE_HEAD_COLOR, pygame.Rect(pos[0], pos[1], GRID_SIZE, GRID_SIZE))
                # Глаза для головы
                eye_size = GRID_SIZE // 4
                eye_offset = GRID_SIZE // 3
                
                # Положение глаз зависит от направления
                if self.direction == pygame.K_RIGHT:
                    pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(pos[0] + GRID_SIZE - eye_offset, pos[1] + eye_offset, eye_size, eye_size))
                    pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(pos[0] + GRID_SIZE - eye_offset, pos[1] + GRID_SIZE - eye_offset - eye_size, eye_size, eye_size))
                elif self.direction == pygame.K_LEFT:
                    pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(pos[0] + eye_offset - eye_size, pos[1] + eye_offset, eye_size, eye_size))
                    pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(pos[0] + eye_offset - eye_size, pos[1] + GRID_SIZE - eye_offset - eye_size, eye_size, eye_size))
                elif self.direction == pygame.K_UP:
                    pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(pos[0] + eye_offset, pos[1] + eye_offset - eye_size, eye_size, eye_size))
                    pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(pos[0] + GRID_SIZE - eye_offset - eye_size, pos[1] + eye_offset - eye_size, eye_size, eye_size))
                elif self.direction == pygame.K_DOWN:
                    pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(pos[0] + eye_offset, pos[1] + GRID_SIZE - eye_offset, eye_size, eye_size))
                    pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(pos[0] + GRID_SIZE - eye_offset - eye_size, pos[1] + GRID_SIZE - eye_offset, eye_size, eye_size))
            else:
                # Тело змейки
                pygame.draw.rect(surface, SNAKE_COLOR, pygame.Rect(pos[0], pos[1], GRID_SIZE, GRID_SIZE))
                # Границы для сегментов тела
                pygame.draw.rect(surface, (50, 120, 50), pygame.Rect(pos[0], pos[1], GRID_SIZE, GRID_SIZE), 1)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = FOOD_COLOR
        self.randomize_position()
        self.particles = []
        
    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, 
                       random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, pygame.Rect(self.position[0], self.position[1], GRID_SIZE, GRID_SIZE))
        # Добавляем блик для еды
        highlight_size = GRID_SIZE // 3
        pygame.draw.ellipse(surface, (255, 200, 200), 
                           pygame.Rect(self.position[0] + highlight_size//2, 
                                     self.position[1] + highlight_size//2, 
                                     highlight_size, highlight_size))
        
    def create_particles(self, position):
        # Создаем частицы для анимации поедания
        for _ in range(15):
            particle = {
                'pos': [position[0] + GRID_SIZE // 2, position[1] + GRID_SIZE // 2],
                'color': random.choice(PARTICLE_COLORS),
                'size': random.randint(2, 6),
                'speed': [random.uniform(-3, 3), random.uniform(-3, 3)],
                'life': random.randint(20, 40)
            }
            self.particles.append(particle)
            
    def update_particles(self):
        for particle in self.particles[:]:
            particle['pos'][0] += particle['speed'][0]
            particle['pos'][1] += particle['speed'][1]
            particle['life'] -= 1
            
            if particle['life'] <= 0:
                self.particles.remove(particle)
                
    def draw_particles(self, surface):
        for particle in self.particles:
            pygame.draw.circle(surface, particle['color'], 
                              (int(particle['pos'][0]), int(particle['pos'][1])), 
                              particle['size'])

class Obstacle:
    def __init__(self):
        self.positions = []
        
    def add_obstacle(self):
        # Добавляем новое препятствие
        pos = (random.randint(1, GRID_WIDTH - 2) * GRID_SIZE, 
             random.randint(1, GRID_HEIGHT - 2) * GRID_SIZE)
        
        # Убедимся, что препятствие не появляется на змейке или еде
        self.positions.append(pos)
        
    def draw(self, surface):
        for pos in self.positions:
            pygame.draw.rect(surface, OBSTACLE_COLOR, pygame.Rect(pos[0], pos[1], GRID_SIZE, GRID_SIZE))
            # Добавляем текстуру для препятствия
            pygame.draw.line(surface, (150, 40, 40), (pos[0], pos[1]), (pos[0] + GRID_SIZE, pos[1] + GRID_SIZE), 2)
            pygame.draw.line(surface, (150, 40, 40), (pos[0] + GRID_SIZE, pos[1]), (pos[0], pos[1] + GRID_SIZE), 2)

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
        
    def check_click(self, pos):
        return self.rect.collidepoint(pos)

def draw_grid(surface):
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(surface, GRID_COLOR, (0, y), (WIDTH, y))

def draw_score(surface, score):
    text = font.render(f"Очки: {score}", True, TEXT_COLOR)
    surface.blit(text, (10, 10))

def draw_game_over(surface, score):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    surface.blit(overlay, (0, 0))
    
    text = font.render("Игра окончена!", True, TEXT_COLOR)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    surface.blit(text, text_rect)
    
    score_text = font.render(f"Очки: {score}", True, TEXT_COLOR)
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    surface.blit(score_text, score_rect)
    
    # Кнопка "Играть снова"
    play_again_btn = Button(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50, "Играть снова")
    play_again_btn.draw(surface)
    
    # Кнопка "Выход"
    exit_btn = Button(WIDTH // 2 - 100, HEIGHT // 2 + 120, 200, 50, "Выход")
    exit_btn.draw(surface)
    
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                play_again_btn.check_hover(event.pos)
                exit_btn.check_hover(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_btn.check_click(event.pos):
                    return True
                elif exit_btn.check_click(event.pos):
                    pygame.quit()
                    sys.exit()
        
        play_again_btn.draw(surface)
        exit_btn.draw(surface)
        pygame.display.update()
        clock.tick(60)

def main_menu():
    # Создаем кнопки
    play_btn = Button(WIDTH // 2 - 100, HEIGHT // 2, 200, 50, "Играть")
    exit_btn = Button(WIDTH // 2 - 100, HEIGHT // 2 + 80, 200, 50, "Выход")
    
    title_font = pygame.font.SysFont('Arial', 64)
    title_text = title_font.render("Змейка", True, TEXT_COLOR)
    subtitle_text = small_font.render("Особенная версия с препятствиями!", True, TEXT_COLOR)
    
    # Анимация частиц для меню
    particles = []
    for _ in range(50):
        particles.append({
            'pos': [random.randint(0, WIDTH), random.randint(0, HEIGHT)],
            'color': random.choice(PARTICLE_COLORS),
            'size': random.randint(2, 4),
            'speed': [random.uniform(-0.5, 0.5), random.uniform(0.5, 1.5)],
            'life': random.randint(50, 150)
        })
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_btn.check_click(mouse_pos):
                    return
                elif exit_btn.check_click(mouse_pos):
                    pygame.quit()
                    sys.exit()
        
        # Обновление частиц
        for particle in particles:
            particle['pos'][0] += particle['speed'][0]
            particle['pos'][1] += particle['speed'][1]
            particle['life'] -= 0.5
            if particle['life'] <= 0:
                particle['life'] = random.randint(50, 150)
                particle['pos'] = [random.randint(0, WIDTH), 0]
                particle['speed'] = [random.uniform(-0.5, 0.5), random.uniform(0.5, 1.5)]
        
        # Отрисовка
        screen.fill(BACKGROUND)
        draw_grid(screen)
        
        # Отрисовка частиц
        for particle in particles:
            pygame.draw.circle(screen, particle['color'], 
                              (int(particle['pos'][0]), int(particle['pos'][1])), 
                              particle['size'])
        
        # Отрисовка заголовка
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(title_text, title_rect)
        
        subtitle_rect = subtitle_text.get_rect(center=(WIDTH // 2, HEIGHT // 4 + 60))
        screen.blit(subtitle_text, subtitle_rect)
        
        # Обновление кнопок
        play_btn.check_hover(mouse_pos)
        exit_btn.check_hover(mouse_pos)
        
        play_btn.draw(screen)
        exit_btn.draw(screen)
        
        pygame.display.update()
        clock.tick(60)

def main():
    main_menu()
    
    while True:
        snake = Snake()
        food = Food()
        obstacles = Obstacle()
        
        # Начальная скорость
        speed = 10
        level = 1
        
        game_over = False
        
        # Главный игровой цикл
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                        # Предотвращение разворота на 180 градусов
                        if (event.key == pygame.K_UP and snake.direction != pygame.K_DOWN) or \
                           (event.key == pygame.K_DOWN and snake.direction != pygame.K_UP) or \
                           (event.key == pygame.K_LEFT and snake.direction != pygame.K_RIGHT) or \
                           (event.key == pygame.K_RIGHT and snake.direction != pygame.K_LEFT):
                            snake.direction = event.key
            
            snake.update()
            
            # Проверка столкновения с едой
            if snake.get_head_position() == food.position:
                snake.grow = True
                snake.score += 10
                food.create_particles(food.position)
                food.randomize_position()
                
                # Проверка, чтобы еда не появилась на змейке или препятствиях
                while any(food.position == pos for pos in snake.positions) or \
                      food.position in obstacles.positions:
                    food.randomize_position()
                
                # Увеличиваем скорость каждые 5 съеденных продуктов
                if snake.score % 50 == 0:
                    speed += 2
                    level += 1
                
                # Добавляем препятствие каждые 30 очков (изюминка)
                if snake.score > 0 and snake.score % 30 == 0:
                    obstacles.add_obstacle()
                    
                    # Проверка, чтобы препятствие не появилось на змейке или еде
                    while any(pos == food.position for pos in obstacles.positions[-1:]) or \
                          any(pos in snake.positions for pos in obstacles.positions[-1:]):
                        obstacles.positions.pop()
                        obstacles.add_obstacle()
            
            # Проверка столкновения с телом
            if any(snake.get_head_position() == pos for pos in snake.positions[1:]):
                game_over = True
            
            # Проверка столкновения с препятствиями
            if snake.get_head_position() in obstacles.positions:
                game_over = True
            
            # Обновление частиц
            food.update_particles()
            
            # Отрисовка
            screen.fill(BACKGROUND)
            draw_grid(screen)
            
            # Отрисовка препятствий
            obstacles.draw(screen)
            
            # Отрисовка еды
            food.draw(screen)
            
            # Отрисовка частиц от еды
            food.draw_particles(screen)
            
            # Отрисовка змейки
            snake.draw(screen)
            
            # Отрисовка счета
            draw_score(screen, snake.score)
            
            # Отображение уровня
            level_text = small_font.render(f"Уровень: {level}", True, TEXT_COLOR)
            screen.blit(level_text, (WIDTH - 150, 10))
            
            pygame.display.update()
            clock.tick(speed)
        
        # После проигрыша
        if draw_game_over(screen, snake.score):
            continue
        else:
            break

if __name__ == "__main__":
    main()
