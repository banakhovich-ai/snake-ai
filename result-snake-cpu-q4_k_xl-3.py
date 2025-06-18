import pygame
import sys
import random
import math
from pygame import gfxdraw

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

# Цветовая гамма
BACKGROUND = (15, 20, 30)
GRID_COLOR = (30, 35, 45)
SNAKE_HEAD_COLOR = (70, 200, 120)
SNAKE_BODY_COLOR = (50, 160, 90)
FOOD_COLOR = (220, 100, 100)
TEXT_COLOR = (240, 240, 240)
BUTTON_COLOR = (80, 120, 200)
BUTTON_HOVER_COLOR = (100, 140, 220)
BUTTON_TEXT_COLOR = (250, 250, 250)
TELEPORT_COLOR = (180, 80, 200)

# Настройка экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка с Изюминкой")
clock = pygame.time.Clock()

# Шрифты
title_font = pygame.font.SysFont("Arial", 48, bold=True)
font = pygame.font.SysFont("Arial", 28)
small_font = pygame.font.SysFont("Arial", 24)

class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)  # Движение вправо
        self.score = 0
        self.grow_to = 3
        self.last_move_time = pygame.time.get_ticks()
        
    def get_head_position(self):
        return self.positions[0]
    
    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        self.direction = point
    
    def move(self):
        head = self.get_head_position()
        x, y = self.direction
        new_x = (head[0] + x) % GRID_WIDTH
        new_y = (head[1] + y) % GRID_HEIGHT
        new_position = (new_x, new_y)
        
        # Проверка столкновения с собой
        if new_position in self.positions[1:]:
            return False
        
        self.positions.insert(0, new_position)
        if len(self.positions) > self.grow_to:
            self.positions.pop()
        return True
    
    def grow(self):
        self.grow_to += 1
        self.score += 10
    
    def draw(self, surface):
        for i, pos in enumerate(self.positions):
            rect = pygame.Rect((pos[0] * GRID_SIZE, pos[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
            
            # Отрисовка головы
            if i == 0:
                color = SNAKE_HEAD_COLOR
                pygame.draw.rect(surface, color, rect)
                pygame.draw.rect(surface, (30, 100, 60), rect.inflate(-4, -4))
                
                # Глаза змеи
                eye_size = GRID_SIZE // 5
                eye_offset = GRID_SIZE // 3
                
                # Левый глаз
                if self.direction == (1, 0):  # Вправо
                    pygame.draw.circle(surface, (20, 20, 40), 
                                      (rect.right - eye_offset, rect.top + eye_offset), eye_size)
                elif self.direction == (-1, 0):  # Влево
                    pygame.draw.circle(surface, (20, 20, 40), 
                                      (rect.left + eye_offset, rect.top + eye_offset), eye_size)
                elif self.direction == (0, 1):  # Вниз
                    pygame.draw.circle(surface, (20, 20, 40), 
                                      (rect.right - eye_offset, rect.top + eye_offset), eye_size)
                elif self.direction == (0, -1):  # Вверх
                    pygame.draw.circle(surface, (20, 20, 40), 
                                      (rect.left + eye_offset, rect.top + eye_offset), eye_size)
            # Отрисовка тела
            else:
                pygame.draw.rect(surface, SNAKE_BODY_COLOR, rect)
                pygame.draw.rect(surface, (30, 80, 60), rect.inflate(-4, -4))
        
        # Эффект телепортации (изюминка)
        if self.positions[0][0] == 0:  # Левая граница
            pygame.draw.rect(surface, TELEPORT_COLOR, pygame.Rect(0, self.positions[0][1] * GRID_SIZE, 5, GRID_SIZE))
        elif self.positions[0][0] == GRID_WIDTH - 1:  # Правая граница
            pygame.draw.rect(surface, TELEPORT_COLOR, pygame.Rect(WIDTH - 5, self.positions[0][1] * GRID_SIZE, 5, GRID_SIZE))
        elif self.positions[0][1] == 0:  # Верхняя граница
            pygame.draw.rect(surface, TELEPORT_COLOR, pygame.Rect(self.positions[0][0] * GRID_SIZE, 0, GRID_SIZE, 5))
        elif self.positions[0][1] == GRID_HEIGHT - 1:  # Нижняя граница
            pygame.draw.rect(surface, TELEPORT_COLOR, pygame.Rect(self.positions[0][0] * GRID_SIZE, HEIGHT - 5, GRID_SIZE, 5))

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()
        self.eaten_animation = False
        self.animation_time = 0
    
    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    
    def draw(self, surface):
        rect = pygame.Rect((self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, FOOD_COLOR, rect)
        
        # Эффект пульсации
        pulse = abs(math.sin(pygame.time.get_ticks() / 200)) * 5
        pygame.draw.rect(surface, (255, 150, 150), rect.inflate(-pulse, -pulse))
        
        # Анимация поедания
        if self.eaten_animation:
            current_time = pygame.time.get_ticks()
            if current_time - self.animation_time < 300:
                progress = (current_time - self.animation_time) / 300
                size = int(GRID_SIZE * (1 + progress))
                alpha = int(255 * (1 - progress))
                s = pygame.Surface((size, size), pygame.SRCALPHA)
                pygame.draw.circle(s, (*FOOD_COLOR, alpha), (size//2, size//2), size//2)
                surface.blit(s, (rect.centerx - size//2, rect.centery - size//2))
            else:
                self.eaten_animation = False
    
    def eat(self):
        self.eaten_animation = True
        self.animation_time = pygame.time.get_ticks()
        self.randomize_position()

class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.hovered = False
        
    def draw(self, surface):
        color = BUTTON_HOVER_COLOR if self.hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, (60, 100, 180), self.rect.inflate(-4, -4), border_radius=8)
        
        text_surf = font.render(self.text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        return self.hovered
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered and self.action:
                self.action()
                return True
        return False

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.state = "menu"  # menu, playing, game_over
        self.buttons = []
        
        # Создание кнопок меню
        self.create_menu_buttons()
        
        # Звуковые эффекты
        try:
            self.eat_sound = pygame.mixer.Sound(pygame.mixer.Sound(bytearray(random.randint(0, 255) for _ in range(44))))
            self.eat_sound.set_volume(0.3)
        except:
            self.eat_sound = None
        
    def create_menu_buttons(self):
        button_width, button_height = 200, 50
        center_x = WIDTH // 2 - button_width // 2
        
        # Кнопка старта
        start_button = Button(center_x, HEIGHT // 2, button_width, button_height, "Играть", self.start_game)
        # Кнопка выхода
        exit_button = Button(center_x, HEIGHT // 2 + 70, button_width, button_height, "Выход", self.exit_game)
        
        self.buttons = [start_button, exit_button]
        
        # Кнопки для конца игры
        self.restart_button = Button(center_x, HEIGHT // 2 + 20, button_width, button_height, "Играть снова", self.start_game)
        self.menu_button = Button(center_x, HEIGHT // 2 + 80, button_width, button_height, "Меню", self.show_menu)
    
    def start_game(self):
        self.snake.reset()
        self.food.randomize_position()
        self.state = "playing"
    
    def exit_game(self):
        pygame.quit()
        sys.exit()
    
    def show_menu(self):
        self.state = "menu"
    
    def game_over(self):
        self.state = "game_over"
    
    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if self.state == "menu":
                for button in self.buttons:
                    button.handle_event(event)
            
            elif self.state == "playing":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.snake.turn((0, -1))
                    elif event.key == pygame.K_DOWN:
                        self.snake.turn((0, 1))
                    elif event.key == pygame.K_LEFT:
                        self.snake.turn((-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        self.snake.turn((1, 0))
                    elif event.key == pygame.K_ESCAPE:
                        self.show_menu()
            
            elif self.state == "game_over":
                self.restart_button.handle_event(event)
                self.menu_button.handle_event(event)
    
    def update(self):
        if self.state == "playing":
            if not self.snake.move():
                self.game_over()
                return
            
            # Проверка поедания еды
            if self.snake.get_head_position() == self.food.position:
                self.snake.grow()
                self.food.eat()
                if self.eat_sound:
                    self.eat_sound.play()
    
    def draw(self):
        # Отрисовка фона
        screen.fill(BACKGROUND)
        
        # Отрисовка сетки
        for x in range(0, WIDTH, GRID_SIZE):
            pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT), 1)
        for y in range(0, HEIGHT, GRID_SIZE):
            pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y), 1)
        
        if self.state == "menu":
            self.draw_menu()
        elif self.state == "playing":
            # Отрисовка объектов игры
            self.food.draw(screen)
            self.snake.draw(screen)
            
            # Отрисовка счета
            score_text = font.render(f"Счет: {self.snake.score}", True, TEXT_COLOR)
            screen.blit(score_text, (10, 10))
            
            # Подсказка
            hint_text = small_font.render("ESC: Меню", True, TEXT_COLOR)
            screen.blit(hint_text, (WIDTH - hint_text.get_width() - 10, 10))
        
        elif self.state == "game_over":
            self.draw_game_over()
    
    def draw_menu(self):
        # Заголовок
        title = title_font.render("ЗМЕЙКА", True, TEXT_COLOR)
        subtitle = font.render("С телепортацией через границы", True, (180, 180, 255))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//4))
        screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, HEIGHT//4 + 60))
        
        # Обработка наведения на кнопки
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.check_hover(mouse_pos)
            button.draw(screen)
        
        # Декоративная змейка
        for i in range(10):
            pos_x = WIDTH // 4 + i * 20
            pos_y = HEIGHT - 100
            size = GRID_SIZE - i
            pygame.draw.rect(screen, SNAKE_BODY_COLOR, 
                            (pos_x, pos_y, size, size))
            pygame.draw.rect(screen, (30, 80, 60), 
                            (pos_x+2, pos_y+2, size-4, size-4))
        
        # Инструкция
        help_text = small_font.render("Используйте стрелки для управления змейкой", True, TEXT_COLOR)
        screen.blit(help_text, (WIDTH//2 - help_text.get_width()//2, HEIGHT - 40))
    
    def draw_game_over(self):
        # Прозрачный фон
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        # Текст
        title = title_font.render("ИГРА ОКОНЧЕНА!", True, (220, 100, 100))
        score_text = font.render(f"Ваш счет: {self.snake.score}", True, TEXT_COLOR)
        
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//3))
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//3 + 70))
        
        # Обработка наведения на кнопки
        mouse_pos = pygame.mouse.get_pos()
        self.restart_button.check_hover(mouse_pos)
        self.menu_button.check_hover(mouse_pos)
        
        self.restart_button.draw(screen)
        self.menu_button.draw(screen)

# Основная функция игры
def main():
    game = Game()
    
    while True:
        game.process_events()
        game.update()
        game.draw()
        
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
