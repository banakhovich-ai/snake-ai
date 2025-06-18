import pygame
import sys
import random
import math

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

# Цвета
BACKGROUND = (15, 15, 30)
GRID_COLOR = (30, 30, 50)
SNAKE_COLOR = (50, 200, 150)
FOOD_COLOR = (220, 100, 100)
SPECIAL_FOOD_COLOR = (255, 215, 0)
MENU_BG = (0, 0, 0, 180)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER_COLOR = (100, 180, 255)
GAME_OVER_BG = (0, 0, 0, 200)
PORTAL_COLOR = (138, 43, 226)

# Класс для эффектов частиц
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.size = random.randint(2, 6)
        self.color = color
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

# Класс кнопки для меню
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = BUTTON_COLOR
        self.hover_color = BUTTON_HOVER_COLOR
        self.is_hovered = False
    
    def draw(self, surface, font):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, TEXT_COLOR, self.rect, 2, border_radius=10)
        text_surf = font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
    
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
    
    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

# Класс змейки
class Snake:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.grow = False
        self.grow_counter = 0
        self.speed = 10
        self.score = 0
        self.boost_timer = 0
    
    def change_direction(self, dx, dy):
        # Запрещаем разворот на 180 градусов
        if (dx, dy) != (-self.direction[0], -self.direction[1]):
            self.next_direction = (dx, dy)
    
    def move(self):
        self.direction = self.next_direction
        
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = ((head_x + dx) % GRID_WIDTH, (head_y + dy) % GRID_HEIGHT)
        
        # Проверка столкновения с собой (кроме головы)
        if new_head in self.body[1:]:
            return False
        
        self.body.insert(0, new_head)
        
        if not self.grow:
            self.body.pop()
        else:
            self.grow_counter -= 1
            if self.grow_counter <= 0:
                self.grow = False
        
        return True
    
    def grow_snake(self, amount=1, duration=10):
        self.grow = True
        self.grow_counter += duration
    
    def activate_boost(self, factor=1.5, duration=3):
        self.speed = int(10 * factor)
        self.boost_timer = duration * FPS
    
    def update_boost(self):
        if self.boost_timer > 0:
            self.boost_timer -= 1
            if self.boost_timer <= 0:
                self.speed = 10
    
    def draw(self, surface):
        for i, (x, y) in enumerate(self.body):
            color = SNAKE_COLOR
            # Голова другого оттенка
            if i == 0:
                color = (min(SNAKE_COLOR[0] + 40, 255), 
                         min(SNAKE_COLOR[1] + 40, 255), 
                         min(SNAKE_COLOR[2] + 40, 255))
            
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, (50, 255, 200), rect, 1)
            
            # Рисуем глаза
            if i == 0:
                eye_size = GRID_SIZE // 5
                dx, dy = self.direction
                
                # Левый глаз
                left_eye_x = x * GRID_SIZE + GRID_SIZE // 3
                left_eye_y = y * GRID_SIZE + GRID_SIZE // 3
                
                # Правый глаз
                right_eye_x = x * GRID_SIZE + 2 * GRID_SIZE // 3
                right_eye_y = y * GRID_SIZE + GRID_SIZE // 3
                
                # Корректировка положения глаз в зависимости от направления
                if dy == -1:  # Вверх
                    left_eye_y -= 2
                    right_eye_y -= 2
                elif dy == 1:   # Вниз
                    left_eye_y += 2
                    right_eye_y += 2
                elif dx == -1:  # Влево
                    left_eye_x -= 2
                    right_eye_x -= 2
                elif dx == 1:   # Вправо
                    left_eye_x += 2
                    right_eye_x += 2
                
                pygame.draw.circle(surface, (0, 0, 0), (left_eye_x, left_eye_y), eye_size)
                pygame.draw.circle(surface, (0, 0, 0), (right_eye_x, right_eye_y), eye_size)

# Класс еды
class Food:
    def __init__(self, snake_body=None):
        if snake_body is None:
            snake_body = []
        self.spawn(snake_body)
        self.particles = []
    
    def spawn(self, snake_body):
        self.position = self.get_free_position(snake_body)
        self.particles = []
    
    def get_free_position(self, snake_body):
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), 
                   random.randint(0, GRID_HEIGHT - 1))
            if pos not in snake_body:
                return pos
    
    def draw(self, surface):
        x, y = self.position
        rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, FOOD_COLOR, rect)
        pygame.draw.rect(surface, (255, 255, 255), rect, 1)
        
        # Рисуем сердцевину
        center_x = x * GRID_SIZE + GRID_SIZE // 2
        center_y = y * GRID_SIZE + GRID_SIZE // 2
        pygame.draw.circle(surface, (255, 200, 200), (center_x, center_y), GRID_SIZE // 3)
    
    def create_particles(self):
        for _ in range(15):
            x = self.position[0] * GRID_SIZE + GRID_SIZE // 2
            y = self.position[1] * GRID_SIZE + GRID_SIZE // 2
            color = (
                FOOD_COLOR[0] + random.randint(0, 50),
                FOOD_COLOR[1] + random.randint(0, 50),
                FOOD_COLOR[2] + random.randint(0, 50)
            )
            self.particles.append(Particle(x, y, color))
    
    def update_particles(self):
        self.particles = [p for p in self.particles if p.update()]
    
    def draw_particles(self, surface):
        for p in self.particles:
            p.draw(surface)

# Класс специальной еды (с эффектом ускорения)
class SpecialFood(Food):
    def __init__(self, snake_body=None):
        super().__init__(snake_body)
        self.timer = 0
        self.active = False
    
    def activate(self, snake_body):
        self.spawn(snake_body)
        self.active = True
        self.timer = 5 * FPS  # 5 секунд активности
    
    def update(self):
        if self.active:
            self.timer -= 1
            if self.timer <= 0:
                self.active = False
    
    def draw(self, surface):
        if not self.active:
            return
        
        x, y = self.position
        rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, SPECIAL_FOOD_COLOR, rect)
        pygame.draw.rect(surface, (255, 255, 200), rect, 1)
        
        # Анимация пульсации
        pulse = (math.sin(pygame.time.get_ticks() * 0.005) + 1) * 0.5
        size = int(GRID_SIZE * 0.8 + pulse * GRID_SIZE * 0.2)
        offset = (GRID_SIZE - size) // 2
        pulse_rect = pygame.Rect(
            x * GRID_SIZE + offset, 
            y * GRID_SIZE + offset, 
            size, 
            size
        )
        pygame.draw.rect(surface, SPECIAL_FOOD_COLOR, pulse_rect)
        
        # Эффект "звезды"
        center_x = x * GRID_SIZE + GRID_SIZE // 2
        center_y = y * GRID_SIZE + GRID_SIZE // 2
        for i in range(6):
            angle = i * 60 + pygame.time.get_ticks() * 0.01 % 360
            rad = math.radians(angle)
            dx = math.cos(rad) * GRID_SIZE // 3
            dy = math.sin(rad) * GRID_SIZE // 3
            pygame.draw.line(
                surface, 
                (255, 255, 200), 
                (center_x, center_y), 
                (center_x + dx, center_y + dy), 
                2
            )

# Класс порталов (изюминка игры)
class Portal:
    def __init__(self):
        self.positions = []
        self.active = False
        self.cooldown = 0
    
    def spawn(self, snake_body, food_pos, special_food_pos):
        self.positions = []
        occupied = snake_body + [food_pos]
        if special_food_pos:
            occupied.append(special_food_pos)
        
        for _ in range(2):
            while True:
                pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
                if pos not in occupied:
                    self.positions.append(pos)
                    occupied.append(pos)
                    break
        
        self.active = True
        self.cooldown = 10 * FPS  # 10 секунд активности
    
    def update(self):
        if self.active:
            self.cooldown -= 1
            if self.cooldown <= 0:
                self.active = False
    
    def teleport(self, snake):
        if not self.active or len(self.positions) < 2:
            return False
        
        head = snake.body[0]
        if head == self.positions[0]:
            snake.body[0] = self.positions[1]
            return True
        elif head == self.positions[1]:
            snake.body[0] = self.positions[0]
            return True
        return False
    
    def draw(self, surface):
        if not self.active:
            return
        
        for i, (x, y) in enumerate(self.positions):
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, PORTAL_COLOR, rect, border_radius=10)
            
            # Анимация вращения
            time_offset = pygame.time.get_ticks() * (1 if i == 0 else -1) * 0.02
            center_x = x * GRID_SIZE + GRID_SIZE // 2
            center_y = y * GRID_SIZE + GRID_SIZE // 2
            radius = GRID_SIZE // 2 - 2
            
            for j in range(8):
                angle = j * 45 + time_offset
                rad = math.radians(angle)
                dx = math.cos(rad) * radius
                dy = math.sin(rad) * radius
                pygame.draw.circle(
                    surface, 
                    (180, 80, 250), 
                    (int(center_x + dx), int(center_y + dy)), 
                    2
                )

# Основная функция игры
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Змейка с порталами")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 24)
    title_font = pygame.font.SysFont("Arial", 48, bold=True)
    
    # Состояния игры
    MENU = 0
    PLAYING = 1
    GAME_OVER = 2
    state = MENU
    
    # Создаем кнопки меню
    start_button = Button(WIDTH//2 - 100, HEIGHT//2, 200, 50, "Играть")
    quit_button = Button(WIDTH//2 - 100, HEIGHT//2 + 70, 200, 50, "Выход")
    
    # Игровые объекты
    snake = Snake()
    food = Food(snake.body)
    special_food = SpecialFood()
    portal = Portal()
    
    # Таймеры
    special_food_timer = 0
    portal_timer = 0
    particle_timer = 0
    
    # Главный цикл
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if state == MENU:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_button.is_clicked(mouse_pos, event):
                        state = PLAYING
                        snake.reset()
                        food.spawn(snake.body)
                        special_food.active = False
                        portal.active = False
                    elif quit_button.is_clicked(mouse_pos, event):
                        pygame.quit()
                        sys.exit()
            
            elif state == PLAYING:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        snake.change_direction(0, -1)
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction(0, 1)
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction(1, 0)
                    elif event.key == pygame.K_p:  # Пауза
                        state = MENU
            
            elif state == GAME_OVER:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        state = PLAYING
                        snake.reset()
                        food.spawn(snake.body)
                        special_food.active = False
                        portal.active = False
        
        # Обновление состояний
        if state == PLAYING:
            # Обновление таймеров
            special_food_timer -= 1
            portal_timer -= 1
            particle_timer -= 1
            
            # Генерация специальной еды
            if special_food_timer <= 0 and not special_food.active:
                occupied = snake.body + [food.position]
                special_food.activate(occupied)
                special_food_timer = random.randint(10, 15) * FPS  # 10-15 секунд
            
            # Генерация порталов
            if portal_timer <= 0 and not portal.active and snake.score >= 5:
                occupied = snake.body + [food.position]
                if special_food.active:
                    occupied.append(special_food.position)
                portal.spawn(occupied, food.position, 
                             special_food.position if special_food.active else None)
                portal_timer = 20 * FPS  # 20 секунд до следующего спавна
            
            # Обновление специальной еды
            if special_food.active:
                special_food.update()
            
            # Обновление порталов
            if portal.active:
                portal.update()
                if portal.teleport(snake):
                    snake.score += 2  # Бонус за использование портала
            
            # Обновление буста скорости
            snake.update_boost()
            
            # Перемещение змейки
            for _ in range(snake.speed // 10):
                if not snake.move():
                    state = GAME_OVER
                    break
            
            # Проверка съедания обычной еды
            if snake.body[0] == food.position:
                food.create_particles()
                snake.grow_snake()
                snake.score += 1
                food.spawn(snake.body)
                # Генерация частиц каждые 5 кадров
                particle_timer = 5
            
            # Проверка съедания специальной еды
            if special_food.active and snake.body[0] == special_food.position:
                snake.activate_boost()
                snake.grow_snake(amount=1, duration=15)
                snake.score += 3
                special_food.active = False
            
            # Обновление частиц
            if particle_timer <= 0:
                food.update_particles()
                particle_timer = 5
        
        # Отрисовка
        screen.fill(BACKGROUND)
        
        # Рисование сетки
        for x in range(0, WIDTH, GRID_SIZE):
            pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, GRID_SIZE):
            pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))
        
        if state == MENU:
            # Рисуем меню
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill(MENU_BG)
            screen.blit(overlay, (0, 0))
            
            title = title_font.render("ЗМЕЙКА С ПОРТАЛАМИ", True, TEXT_COLOR)
            screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//4))
            
            start_button.check_hover(mouse_pos)
            quit_button.check_hover(mouse_pos)
            
            start_button.draw(screen, font)
            quit_button.draw(screen, font)
            
            # Инструкция
            inst = font.render("Управление: стрелки, P - пауза", True, TEXT_COLOR)
            screen.blit(inst, (WIDTH//2 - inst.get_width()//2, HEIGHT//4 + 200))
            inst2 = font.render("Порталы телепортируют змейку", True, PORTAL_COLOR)
            screen.blit(inst2, (WIDTH//2 - inst2.get_width()//2, HEIGHT//4 + 250))
        
        elif state == PLAYING:
            # Рисуем игровые объекты
            portal.draw(screen)
            food.draw(screen)
            food.draw_particles(screen)
            
            if special_food.active:
                special_food.draw(screen)
            
            snake.draw(screen)
            
            # Интерфейс
            score_text = font.render(f"Очки: {snake.score}", True, TEXT_COLOR)
            screen.blit(score_text, (10, 10))
            
            # Таймеры
            if special_food.active:
                timer_text = font.render(
                    f"Спец.еда: {special_food.timer//FPS}", 
                    True, SPECIAL_FOOD_COLOR
                )
                screen.blit(timer_text, (10, 40))
            
            if portal.active:
                timer_text = font.render(
                    f"Порталы: {portal.cooldown//FPS}", 
                    True, PORTAL_COLOR
                )
                screen.blit(timer_text, (10, 70))
            
            if snake.boost_timer > 0:
                boost_text = font.render(
                    f"Ускорение: {snake.boost_timer//FPS}", 
                    True, SPECIAL_FOOD_COLOR
                )
                screen.blit(boost_text, (WIDTH - 200, 10))
        
        elif state == GAME_OVER:
            snake.draw(screen)
            food.draw(screen)
            
            # Затемнение
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill(GAME_OVER_BG)
            screen.blit(overlay, (0, 0))
            
            game_over = title_font.render("ИГРА ОКОНЧЕНА", True, (220, 50, 50))
            screen.blit(game_over, (WIDTH//2 - game_over.get_width()//2, HEIGHT//3))
            
            score_text = font.render(f"Очки: {snake.score}", True, TEXT_COLOR)
            screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
            
            restart_text = font.render("Нажмите R для рестарта", True, TEXT_COLOR)
            screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 50))
            
            menu_text = font.render("Нажмите P для выхода в меню", True, TEXT_COLOR)
            screen.blit(menu_text, (WIDTH//2 - menu_text.get_width()//2, HEIGHT//2 + 90))
        
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
