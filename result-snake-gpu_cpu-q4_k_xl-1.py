import pygame
import sys
import random
import math
from pygame import gfxdraw

# Инициализация Pygame
pygame.init()
pygame.font.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = (SCREEN_HEIGHT - 80) // GRID_SIZE  # Оставляем место для интерфейса
SNAKE_SPEED = 10  # Количество кадров на одно движение

# Цвета
BACKGROUND = (15, 20, 30)
GRID_COLOR = (30, 35, 45)
UI_BACKGROUND = (25, 30, 40)
UI_TEXT = (220, 220, 220)
SNAKE_COLOR = (50, 200, 100)
SNAKE_HEAD_COLOR = (70, 230, 120)
FOOD_COLOR = (220, 80, 60)
SPECIAL_FOOD_COLOR = (180, 100, 220)
TELEPORT_COLOR = (80, 150, 220)
TELEPORT_HIGHLIGHT = (120, 200, 255)

# Создание экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Змейка с изюминкой")
clock = pygame.time.Clock()

# Шрифты
title_font = pygame.font.SysFont("Arial", 48, bold=True)
menu_font = pygame.font.SysFont("Arial", 32)
game_font = pygame.font.SysFont("Arial", 24)
small_font = pygame.font.SysFont("Arial", 18)

class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)  # Начальное направление: вправо
        self.score = 0
        self.grow_to = 3
        self.speed_boost = 0
        self.teleport_cooldown = 0
        
    def get_head_position(self):
        return self.positions[0]
    
    def update(self):
        # Уменьшение времени эффектов
        if self.speed_boost > 0:
            self.speed_boost -= 1
        if self.teleport_cooldown > 0:
            self.teleport_cooldown -= 1
            
        # Добавление новой головы
        head = self.get_head_position()
        new_x = (head[0] + self.direction[0]) % GRID_WIDTH
        new_y = (head[1] + self.direction[1]) % GRID_HEIGHT
        new_position = (new_x, new_y)
        
        # Проверка столкновения с собой
        if new_position in self.positions[1:]:
            return False  # Игра окончена
        
        self.positions.insert(0, new_position)
        
        # Уменьшение длины змейки, если не нужно расти
        if len(self.positions) > self.grow_to:
            self.positions.pop()
            
        return True
    
    def render(self, surface):
        # Рисуем голову
        head = self.positions[0]
        self.draw_rounded_rect(surface, 
                               head[0] * GRID_SIZE, 
                               head[1] * GRID_SIZE, 
                               GRID_SIZE, GRID_SIZE, 
                               SNAKE_HEAD_COLOR, 5)
        
        # Глаза на голове
        eye_size = GRID_SIZE // 5
        eye_offset = GRID_SIZE // 3
        
        # Позиции глаз в зависимости от направления
        dx, dy = self.direction
        if dx == 1:  # Вправо
            left_eye = (head[0] * GRID_SIZE + GRID_SIZE - eye_offset, head[1] * GRID_SIZE + eye_offset)
            right_eye = (head[0] * GRID_SIZE + GRID_SIZE - eye_offset, head[1] * GRID_SIZE + GRID_SIZE - eye_offset)
        elif dx == -1:  # Влево
            left_eye = (head[0] * GRID_SIZE + eye_offset, head[1] * GRID_SIZE + eye_offset)
            right_eye = (head[0] * GRID_SIZE + eye_offset, head[1] * GRID_SIZE + GRID_SIZE - eye_offset)
        elif dy == 1:  # Вниз
            left_eye = (head[0] * GRID_SIZE + eye_offset, head[1] * GRID_SIZE + GRID_SIZE - eye_offset)
            right_eye = (head[0] * GRID_SIZE + GRID_SIZE - eye_offset, head[1] * GRID_SIZE + GRID_SIZE - eye_offset)
        else:  # Вверх
            left_eye = (head[0] * GRID_SIZE + eye_offset, head[1] * GRID_SIZE + eye_offset)
            right_eye = (head[0] * GRID_SIZE + GRID_SIZE - eye_offset, head[1] * GRID_SIZE + eye_offset)
        
        pygame.draw.circle(surface, (255, 255, 255), left_eye, eye_size)
        pygame.draw.circle(surface, (255, 255, 255), right_eye, eye_size)
        pygame.draw.circle(surface, (0, 0, 0), left_eye, eye_size // 2)
        pygame.draw.circle(surface, (0, 0, 0), right_eye, eye_size // 2)
        
        # Рисуем тело
        for i, pos in enumerate(self.positions[1:]):
            # Плавное изменение цвета тела
            color_factor = max(0.6, 1.0 - (i / len(self.positions) * 0.4))
            color = (
                int(SNAKE_COLOR[0] * color_factor),
                int(SNAKE_COLOR[1] * color_factor),
                int(SNAKE_COLOR[2] * color_factor)
            )
            self.draw_rounded_rect(surface, 
                                  pos[0] * GRID_SIZE, 
                                  pos[1] * GRID_SIZE, 
                                  GRID_SIZE, GRID_SIZE, 
                                  color, 4)
    
    def draw_rounded_rect(self, surface, x, y, width, height, color, radius):
        """Рисует закругленный прямоугольник"""
        rect = pygame.Rect(x, y, width, height)
        
        # Рисуем углы
        gfxdraw.filled_circle(surface, rect.left + radius, rect.top + radius, radius, color)
        gfxdraw.filled_circle(surface, rect.right - radius - 1, rect.top + radius, radius, color)
        gfxdraw.filled_circle(surface, rect.left + radius, rect.bottom - radius - 1, radius, color)
        gfxdraw.filled_circle(surface, rect.right - radius - 1, rect.bottom - radius - 1, radius, color)
        
        # Рисуем основные части
        pygame.draw.rect(surface, color, (rect.left + radius, rect.top, rect.width - 2 * radius, rect.height))
        pygame.draw.rect(surface, color, (rect.left, rect.top + radius, rect.width, rect.height - 2 * radius))

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()
        self.timer = 0
        self.special_timer = 0
        self.active = True
    
    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), 
                        random.randint(0, GRID_HEIGHT - 1))
    
    def render(self, surface):
        if not self.active:
            return
            
        # Плавное мерцание
        pulse = (math.sin(pygame.time.get_ticks() * 0.01) + 1) * 0.1 + 0.8
        color = (
            min(255, int(FOOD_COLOR[0] * pulse)),
            min(255, int(FOOD_COLOR[1] * pulse)),
            min(255, int(FOOD_COLOR[2] * pulse))
        )
        
        x = self.position[0] * GRID_SIZE + GRID_SIZE // 2
        y = self.position[1] * GRID_SIZE + GRID_SIZE // 2
        
        # Рисуем яблоко
        pygame.draw.circle(surface, color, (x, y), GRID_SIZE // 2)
        
        # Рисуем блик
        pygame.draw.circle(surface, (255, 255, 255, 128), (x - GRID_SIZE//6, y - GRID_SIZE//6), GRID_SIZE//6, 1)
        
        # Рисуем стебелек
        pygame.draw.line(surface, (50, 150, 50), (x, y - GRID_SIZE//2), (x + GRID_SIZE//4, y - GRID_SIZE//4), 2)

class SpecialFood(Food):
    def __init__(self):
        super().__init__()
        self.timer = 200  # Время существования
        self.active = False
    
    def randomize_position(self):
        self.position = (random.randint(2, GRID_WIDTH - 3), 
                        random.randint(2, GRID_HEIGHT - 3))
    
    def render(self, surface):
        if not self.active:
            return
            
        # Плавное изменение цвета и размера
        pulse = math.sin(pygame.time.get_ticks() * 0.02) * 0.2 + 0.8
        size = GRID_SIZE * 0.7 * pulse
        color = SPECIAL_FOOD_COLOR
        
        # Мерцание
        if self.timer < 60:
            flicker = pygame.time.get_ticks() // 100 % 2 == 0
            if flicker:
                return
        
        x = self.position[0] * GRID_SIZE + GRID_SIZE // 2
        y = self.position[1] * GRID_SIZE + GRID_SIZE // 2
        
        # Рисуем звезду
        self.draw_star(surface, x, y, size, color)
    
    def draw_star(self, surface, x, y, size, color):
        points = []
        for i in range(5):
            angle = math.pi/2 + i * 2*math.pi/5
            outer_x = x + size * math.cos(angle)
            outer_y = y + size * math.sin(angle)
            points.append((outer_x, outer_y))
            
            inner_angle = angle + math.pi/5
            inner_x = x + size/2 * math.cos(inner_angle)
            inner_y = y + size/2 * math.sin(inner_angle)
            points.append((inner_x, inner_y))
        
        pygame.draw.polygon(surface, color, points)

class Teleport:
    def __init__(self):
        self.positions = [(0, 0), (0, 0)]
        self.reset_timer = 0
        self.active = False
    
    def generate(self):
        self.active = True
        # Генерируем две случайные позиции
        pos1 = (random.randint(0, GRID_WIDTH - 1), 
                random.randint(0, GRID_HEIGHT - 1))
        pos2 = (random.randint(0, GRID_WIDTH - 1), 
                random.randint(0, GRID_HEIGHT - 1))
        
        # Убедимся, что позиции не слишком близки
        while abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) < 10:
            pos2 = (random.randint(0, GRID_WIDTH - 1), 
                    random.randint(0, GRID_HEIGHT - 1))
        
        self.positions = [pos1, pos2]
        self.reset_timer = 300  # Телепорт существует 300 кадров
    
    def render(self, surface):
        if not self.active:
            return
            
        self.reset_timer -= 1
        if self.reset_timer <= 0:
            self.active = False
            return
            
        # Анимированная связь между телепортами
        pulse = abs(math.sin(pygame.time.get_ticks() * 0.01)) * 0.5 + 0.5
        line_color = (
            int(TELEPORT_COLOR[0] * pulse),
            int(TELEPORT_COLOR[1] * pulse),
            int(TELEPORT_COLOR[2] * pulse)
        )
        
        # Рисуем линию между телепортами (только если оба активны)
        x1 = self.positions[0][0] * GRID_SIZE + GRID_SIZE // 2
        y1 = self.positions[0][1] * GRID_SIZE + GRID_SIZE // 2
        x2 = self.positions[1][0] * GRID_SIZE + GRID_SIZE // 2
        y2 = self.positions[1][1] * GRID_SIZE + GRID_SIZE // 2
        
        pygame.draw.line(surface, line_color, (x1, y1), (x2, y2), 2)
        
        # Рисуем телепорты
        for i, pos in enumerate(self.positions):
            x = pos[0] * GRID_SIZE + GRID_SIZE // 2
            y = pos[1] * GRID_SIZE + GRID_SIZE // 2
            
            # Внешнее кольцо
            pygame.draw.circle(surface, TELEPORT_HIGHLIGHT, (x, y), GRID_SIZE // 2, 2)
            
            # Внутренний круг
            inner_size = GRID_SIZE // 3
            pygame.draw.circle(surface, TELEPORT_COLOR, (x, y), inner_size)

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.special_food = SpecialFood()
        self.teleport = Teleport()
        self.game_over = False
        self.paused = False
        self.menu = True
        self.frame_count = 0
        self.eating_animation = False
        self.eating_pos = (0, 0)
        self.eating_timer = 0
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                # Управление в меню
                if self.menu:
                    if event.key == pygame.K_SPACE:
                        self.menu = False
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                        
                # Управление в игре
                else:
                    if event.key == pygame.K_ESCAPE:
                        self.menu = True
                        
                    if event.key == pygame.K_p:
                        self.paused = not self.paused
                        
                    if not self.paused and not self.game_over:
                        # Управление змейкой
                        if event.key == pygame.K_UP and self.snake.direction != (0, 1):
                            self.snake.direction = (0, -1)
                        elif event.key == pygame.K_DOWN and self.snake.direction != (0, -1):
                            self.snake.direction = (0, 1)
                        elif event.key == pygame.K_LEFT and self.snake.direction != (1, 0):
                            self.snake.direction = (-1, 0)
                        elif event.key == pygame.K_RIGHT and self.snake.direction != (-1, 0):
                            self.snake.direction = (1, 0)
                        elif event.key == pygame.K_t and self.snake.teleport_cooldown <= 0:
                            self.activate_teleport()
    
    def activate_teleport(self):
        if not self.teleport.active:
            return
            
        head = self.snake.get_head_position()
        for i, pos in enumerate(self.teleport.positions):
            if head == pos:
                # Телепортируем змейку к другому телепорту
                target = self.teleport.positions[1 if i == 0 else 0]
                self.snake.positions[0] = target
                self.snake.teleport_cooldown = 30
                return
    
    def reset_game(self):
        self.snake.reset()
        self.food.randomize_position()
        self.special_food.active = False
        self.special_food.timer = 200
        self.teleport.active = False
        self.game_over = False
        self.paused = False
        self.frame_count = 0
        self.eating_animation = False
        
    def update(self):
        if self.menu or self.paused or self.game_over:
            return
            
        self.frame_count += 1
        speed_factor = 1.0
        
        # Проверяем буст скорости
        if self.snake.speed_boost > 0:
            speed_factor = 1.5
            
        # Двигаем змейку через определенное количество кадров
        if self.frame_count % max(1, int(SNAKE_SPEED / speed_factor)) == 0:
            if not self.snake.update():
                self.game_over = True
                return
                
            # Проверяем столкновение с едой
            head = self.snake.get_head_position()
            
            # Обычная еда
            if head == self.food.position and self.food.active:
                self.snake.grow_to += 1
                self.snake.score += 10
                self.food.randomize_position()
                self.food.active = True
                self.eating_animation = True
                self.eating_pos = head
                self.eating_timer = 10
                
                # Шанс появления специальной еды
                if random.random() < 0.3:
                    self.special_food.randomize_position()
                    self.special_food.active = True
                    self.special_food.timer = 200
                    
                # Шанс появления телепорта
                if random.random() < 0.4:
                    self.teleport.generate()
            
            # Специальная еда
            if (self.special_food.active and 
                head == self.special_food.position):
                self.snake.grow_to += 3
                self.snake.score += 30
                self.special_food.active = False
                self.eating_animation = True
                self.eating_pos = head
                self.eating_timer = 15
                
                # Даем буст скорости
                self.snake.speed_boost = 150
                
                # Шанс появления телепорта
                if random.random() < 0.6:
                    self.teleport.generate()
            
            # Телепорт
            if self.teleport.active:
                for i, pos in enumerate(self.teleport.positions):
                    if head == pos and self.snake.teleport_cooldown <= 0:
                        self.activate_teleport()
                        break
        
        # Обновляем специальную еду
        if self.special_food.active:
            self.special_food.timer -= 1
            if self.special_food.timer <= 0:
                self.special_food.active = False
                
        # Обновляем анимацию поедания
        if self.eating_animation:
            self.eating_timer -= 1
            if self.eating_timer <= 0:
                self.eating_animation = False
    
    def draw_grid(self):
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT - 80), 1)
        for y in range(0, SCREEN_HEIGHT - 80, GRID_SIZE):
            pygame.draw.line(screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y), 1)
    
    def draw_ui(self):
        # Панель внизу
        pygame.draw.rect(screen, UI_BACKGROUND, (0, SCREEN_HEIGHT - 80, SCREEN_WIDTH, 80))
        pygame.draw.line(screen, GRID_COLOR, (0, SCREEN_HEIGHT - 80), (SCREEN_WIDTH, SCREEN_HEIGHT - 80), 2)
        
        # Счет
        score_text = game_font.render(f"Счет: {self.snake.score}", True, UI_TEXT)
        screen.blit(score_text, (20, SCREEN_HEIGHT - 60))
        
        # Длина змейки
        length_text = game_font.render(f"Длина: {self.snake.grow_to}", True, UI_TEXT)
        screen.blit(length_text, (200, SCREEN_HEIGHT - 60))
        
        # Специальные эффекты
        if self.snake.speed_boost > 0:
            boost_text = game_font.render(f"Буст скорости: {self.snake.speed_boost//10}", True, (220, 180, 60))
            screen.blit(boost_text, (400, SCREEN_HEIGHT - 60))
        
        if self.snake.teleport_cooldown > 0:
            tele_text = game_font.render(f"Телепорт: {self.snake.teleport_cooldown//10}", True, TELEPORT_COLOR)
            screen.blit(tele_text, (400, SCREEN_HEIGHT - 30))
        elif self.teleport.active:
            tele_text = game_font.render(f"Телепорт активен!", True, TELEPORT_HIGHLIGHT)
            screen.blit(tele_text, (400, SCREEN_HEIGHT - 30))
        
        # Управление
        controls_text = small_font.render("Стрелки: движение, T: телепорт, P: пауза, ESC: меню", True, (150, 150, 170))
        screen.blit(controls_text, (20, SCREEN_HEIGHT - 30))
    
    def draw_eating_animation(self):
        if not self.eating_animation:
            return
            
        x = self.eating_pos[0] * GRID_SIZE + GRID_SIZE // 2
        y = self.eating_pos[1] * GRID_SIZE + GRID_SIZE // 2
        
        # Количество кругов
        circles = 8
        max_radius = GRID_SIZE * (self.eating_timer / 10) * 1.5
        
        for i in range(circles):
            angle = 2 * math.pi * i / circles
            radius = max_radius * (1 - self.eating_timer / 10)
            offset_x = math.cos(angle) * radius
            offset_y = math.sin(angle) * radius
            
            color = (
                255 - int(100 * self.eating_timer / 10),
                200 - int(50 * self.eating_timer / 10),
                100 - int(40 * self.eating_timer / 10)
            )
            
            pygame.draw.circle(screen, color, (int(x + offset_x), int(y + offset_y)), 4)
    
    def draw_menu(self):
        # Заголовок
        title = title_font.render("ЗМЕЙКА С ИЗЮМИНКОЙ", True, (70, 220, 180))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
        
        # Инструкция
        inst_text = menu_font.render("Нажмите ПРОБЕЛ для начала игры", True, (200, 200, 100))
        screen.blit(inst_text, (SCREEN_WIDTH // 2 - inst_text.get_width() // 2, 250))
        
        # Особенности
        features = [
            "- Специальная еда дает бонусы и буст скорости",
            "- Телепорты для мгновенного перемещения",
            "- Красивая анимация поедания еды",
            "- Плавная змейка с закругленными углами"
        ]
        
        for i, feature in enumerate(features):
            feat_text = game_font.render(feature, True, (180, 180, 220))
            screen.blit(feat_text, (SCREEN_WIDTH // 2 - feat_text.get_width() // 2, 320 + i * 40))
        
        # Управление
        controls = small_font.render("Управление: Стрелки - движение, T - телепорт, P - пауза, ESC - меню", True, (150, 150, 170))
        screen.blit(controls, (SCREEN_WIDTH // 2 - controls.get_width() // 2, SCREEN_HEIGHT - 50))
    
    def draw_game_over(self):
        if not self.game_over:
            return
            
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        game_over = title_font.render("ИГРА ОКОНЧЕНА", True, (220, 100, 100))
        screen.blit(game_over, (SCREEN_WIDTH // 2 - game_over.get_width() // 2, 200))
        
        score_text = menu_font.render(f"Ваш счет: {self.snake.score}", True, (220, 220, 150))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 300))
        
        restart = menu_font.render("Нажмите R для новой игры", True, (150, 220, 150))
        screen.blit(restart, (SCREEN_WIDTH // 2 - restart.get_width() // 2, 400))
        
        menu_text = game_font.render("Нажмите ESC для выхода в меню", True, (180, 180, 220))
        screen.blit(menu_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, 480))
    
    def draw_pause(self):
        if not self.paused:
            return
            
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        pause = title_font.render("ПАУЗА", True, (220, 220, 150))
        screen.blit(pause, (SCREEN_WIDTH // 2 - pause.get_width() // 2, 250))
        
        inst = game_font.render("Нажмите P для продолжения", True, (180, 180, 220))
        screen.blit(inst, (SCREEN_WIDTH // 2 - inst.get_width() // 2, 350))
    
    def render(self):
        # Рисуем сетку
        self.draw_grid()
        
        # Рисуем еду
        self.food.render(screen)
        self.special_food.render(screen)
        
        # Рисуем телепорты
        self.teleport.render(screen)
        
        # Рисуем змейку
        self.snake.render(screen)
        
        # Рисуем анимацию поедания
        self.draw_eating_animation()
        
        # Рисуем интерфейс
        self.draw_ui()
        
        # Рисуем экран меню
        if self.menu:
            self.draw_menu()
        
        # Рисуем экран завершения игры
        if self.game_over:
            self.draw_game_over()
            
        # Рисуем экран паузы
        if self.paused:
            self.draw_pause()

# Основная функция
def main():
    game = Game()
    
    while True:
        game.handle_events()
        game.update()
        
        # Обработка клавиш на экране окончания игры
        if game.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                game.reset_game()
            elif keys[pygame.K_ESCAPE]:
                game.menu = True
                game.game_over = False
        
        screen.fill(BACKGROUND)
        game.render()
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
