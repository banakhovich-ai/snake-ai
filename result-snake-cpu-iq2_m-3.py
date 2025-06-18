import pygame
import sys
import random
import math

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GRID_SIZE = 25
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
FPS = 60

# Цвета
BACKGROUND = (15, 20, 30)
GRID_COLOR = (30, 35, 45)
SNAKE_COLOR = (50, 180, 80)
SNAKE_HEAD_COLOR = (70, 200, 100)
FOOD_COLOR = (220, 60, 60)
SPECIAL_FOOD_COLOR = (220, 200, 60)
TEXT_COLOR = (240, 240, 240)
MENU_BG = (25, 30, 40)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER = (100, 160, 210)

class Snake:
    def __init__(self):
        self.reset()
        self.head_color = SNAKE_HEAD_COLOR
        self.body_color = SNAKE_COLOR
    
    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        # Генерируем начальные сегменты змейки
        self.direction = random.choice([(1, 0), (0, 1), (-1, 0), (0, -1)])
        dx, dy = self.direction
        for i in range(1, self.length):
            self.positions.append((self.positions[0][0] - dx * i, self.positions[0][1] - dy * i))
        self.next_direction = self.direction
        self.grow_pending = 0
    
    def update_direction(self, direction):
        # Запрещаем движение в противоположном направлении
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.next_direction = direction
    
    def move(self):
        self.direction = self.next_direction
        dx, dy = self.direction
        head_x, head_y = self.positions[0]
        new_head = ((head_x + dx) % GRID_WIDTH, (head_y + dy) % GRID_HEIGHT)
        
        # Добавляем новую голову
        self.positions.insert(0, new_head)
        
        # Удаляем хвост, если не нужно расти
        if self.grow_pending <= 0:
            self.positions.pop()
        else:
            self.grow_pending -= 1
    
    def grow(self, amount=1):
        self.grow_pending += amount
        self.length += amount
    
    def draw(self, surface):
        # Рисуем тело змейки
        for i, (x, y) in enumerate(self.positions):
            color = self.head_color if i == 0 else self.body_color
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, color, rect, border_radius=7)
            
            # Рисуем глаза на голове
            if i == 0:
                eye_size = GRID_SIZE // 5
                eye_offset = GRID_SIZE // 3
                pygame.draw.circle(surface, (15, 15, 25), 
                                 (x * GRID_SIZE + eye_offset, y * GRID_SIZE + eye_offset), eye_size)
                pygame.draw.circle(surface, (15, 15, 25), 
                                 (x * GRID_SIZE + GRID_SIZE - eye_offset, 
                                  y * GRID_SIZE + eye_offset), eye_size)

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.spawn()
        self.eaten_animation = 0
    
    def spawn(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), 
                        random.randint(0, GRID_HEIGHT - 1))
    
    def draw(self, surface):
        x, y = self.position
        rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        
        if self.eaten_animation > 0:
            size = GRID_SIZE * (1 + 0.5 * math.sin(self.eaten_animation * 0.3))
            offset = (GRID_SIZE - size) / 2
            pygame.draw.rect(surface, FOOD_COLOR, 
                            (x * GRID_SIZE + offset, y * GRID_SIZE + offset, size, size), 
                            border_radius=int(size/2))
            self.eaten_animation -= 1
        else:
            pygame.draw.rect(surface, FOOD_COLOR, rect, border_radius=12)

class SpecialFood(Food):
    def __init__(self):
        super().__init__()
        self.active = False
        self.lifetime = 0
        self.effects = ['grow', 'speed', 'slow']
        self.effect = random.choice(self.effects)
        self.rotation = 0
    
    def spawn(self):
        super().spawn()
        self.active = True
        self.lifetime = 300  # 5 секунд при 60 FPS
    
    def update(self):
        if self.active:
            self.lifetime -= 1
            self.rotation = (self.rotation + 5) % 360
            if self.lifetime <= 0:
                self.active = False
    
    def draw(self, surface):
        if not self.active:
            return
        
        x, y = self.position
        size = GRID_SIZE - 5
        center_x = x * GRID_SIZE + GRID_SIZE // 2
        center_y = y * GRID_SIZE + GRID_SIZE // 2
        
        # Рисуем вращающуюся звезду
        points = []
        for i in range(5):
            angle = math.radians(self.rotation + i * 72)
            outer_x = center_x + size * math.cos(angle)
            outer_y = center_y + size * math.sin(angle)
            points.append((outer_x, outer_y))
            
            inner_angle = math.radians(self.rotation + 36 + i * 72)
            inner_x = center_x + size * 0.4 * math.cos(inner_angle)
            inner_y = center_y + size * 0.4 * math.sin(inner_angle)
            points.append((inner_x, inner_y))
        
        pygame.draw.polygon(surface, SPECIAL_FOOD_COLOR, points)

class Game:
    def __init__(self, surface):
        self.surface = surface
        self.snake = Snake()
        self.food = Food()
        self.special_food = SpecialFood()
        self.score = 0
        self.game_over = False
        self.paused = False
        self.level = 1
        self.speed = 10
        self.font = pygame.font.SysFont('Arial', 24)
        self.big_font = pygame.font.SysFont('Arial', 48, bold=True)
        self.move_counter = 0
    
    def reset(self):
        self.snake.reset()
        self.food.spawn()
        self.special_food.active = False
        self.score = 0
        self.game_over = False
        self.paused = False
        self.level = 1
        self.speed = 10
    
    def update(self):
        if self.paused or self.game_over:
            return
        
        self.move_counter += 1
        
        # Движение змейки с учетом скорости
        if self.move_counter >= max(1, 10 - self.speed // 2):
            self.move_counter = 0
            self.snake.move()
            
            # Проверка столкновения с собой
            head = self.snake.positions[0]
            if head in self.snake.positions[1:]:
                self.game_over = True
            
            # Проверка съедания обычной еды
            if head == self.food.position:
                self.snake.grow()
                self.score += 1
                self.food.spawn()
                self.food.eaten_animation = 10
                
                # Увеличиваем уровень каждые 5 очков
                if self.score % 5 == 0:
                    self.level += 1
                    self.speed = min(20, self.speed + 1)
            
            # Проверка съедания специальной еды
            if self.special_food.active and head == self.special_food.position:
                effect = self.special_food.effect
                if effect == 'grow':
                    self.snake.grow(3)
                elif effect == 'speed':
                    self.speed = min(20, self.speed + 3)
                elif effect == 'slow':
                    self.speed = max(5, self.speed - 3)
                self.score += 3
                self.special_food.active = False
            
            # Случайное появление специальной еды
            if not self.special_food.active and random.random() < 0.005:
                self.special_food.spawn()
                # Гарантируем, что специальная еда не появляется поверх обычной
                while self.special_food.position == self.food.position:
                    self.special_food.spawn()
            
            # Обновление специальной еды
            self.special_food.update()
    
    def draw(self):
        # Рисуем фон
        self.surface.fill(BACKGROUND)
        
        # Рисуем сетку
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(self.surface, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.surface, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))
        
        # Рисуем еду
        self.food.draw(self.surface)
        
        # Рисуем специальную еду
        self.special_food.draw(self.surface)
        
        # Рисуем змейку
        self.snake.draw(self.surface)
        
        # Рисуем UI
        score_text = self.font.render(f'Score: {self.score}', True, TEXT_COLOR)
        level_text = self.font.render(f'Level: {self.level}', True, TEXT_COLOR)
        self.surface.blit(score_text, (10, 10))
        self.surface.blit(level_text, (10, 40))
        
        # Эффект паузы
        if self.paused:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            self.surface.blit(overlay, (0, 0))
            pause_text = self.big_font.render("PAUSED", True, TEXT_COLOR)
            text_rect = pause_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.surface.blit(pause_text, text_rect)
        
        # Экран окончания игры
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.surface.blit(overlay, (0, 0))
            game_over_text = self.big_font.render("GAME OVER", True, (220, 80, 80))
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
            self.surface.blit(game_over_text, text_rect)
            
            restart_text = self.font.render("Press SPACE to restart or ESC for menu", True, TEXT_COLOR)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 30))
            self.surface.blit(restart_text, restart_rect)

class Menu:
    def __init__(self, surface):
        self.surface = surface
        self.buttons = [
            {"text": "Start Game", "action": "start"},
            {"text": "Quit", "action": "quit"}
        ]
        self.selected = 0
        self.title_font = pygame.font.SysFont('Arial', 64, bold=True)
        self.button_font = pygame.font.SysFont('Arial', 36)
    
    def draw(self):
        self.surface.fill(MENU_BG)
        
        # Рисуем заголовок
        title = self.title_font.render("SNAKE GAME", True, TEXT_COLOR)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4))
        self.surface.blit(title, title_rect)
        
        # Рисуем кнопки
        for i, button in enumerate(self.buttons):
            color = BUTTON_HOVER if i == self.selected else BUTTON_COLOR
            text = self.button_font.render(button["text"], True, TEXT_COLOR)
            rect = pygame.Rect(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 + i*70, 300, 50)
            pygame.draw.rect(self.surface, color, rect, border_radius=10)
            text_rect = text.get_rect(center=rect.center)
            self.surface.blit(text, text_rect)
        
        # Подсказка управления
        hint_font = pygame.font.SysFont('Arial', 18)
        hint = hint_font.render("Use arrow keys to move. Press P to pause.", True, (150, 150, 150))
        self.surface.blit(hint, (SCREEN_WIDTH//2 - hint.get_width()//2, SCREEN_HEIGHT - 40))
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.buttons)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.buttons)
            elif event.key == pygame.K_RETURN:
                return self.buttons[self.selected]["action"]
        return None

# Основная функция
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Змейка")
    clock = pygame.time.Clock()
    
    menu = Menu(screen)
    game = Game(screen)
    
    current_screen = "menu"
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if current_screen == "menu":
                action = menu.handle_event(event)
                if action == "start":
                    current_screen = "game"
                elif action == "quit":
                    pygame.quit()
                    sys.exit()
            
            elif current_screen == "game":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        game.snake.update_direction((0, -1))
                    elif event.key == pygame.K_DOWN:
                        game.snake.update_direction((0, 1))
                    elif event.key == pygame.K_LEFT:
                        game.snake.update_direction((-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        game.snake.update_direction((1, 0))
                    elif event.key == pygame.K_p:
                        game.paused = not game.paused
                    elif event.key == pygame.K_SPACE and game.game_over:
                        game.reset()
                    elif event.key == pygame.K_ESCAPE:
                        current_screen = "menu"
        
        # Обновление игры
        if current_screen == "game":
            game.update()
        
        # Отрисовка
        if current_screen == "menu":
            menu.draw()
        elif current_screen == "game":
            game.draw()
        
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
