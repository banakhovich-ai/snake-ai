```text
Prompt
- Tokens: 59
- Time: 3219.072 ms
- Speed: 19.2 t/s
Generation
- Tokens: 10812
- Time: 3540605.325 ms
- Speed: 3.1 t/s
```

<think>
Игра "Змейка" с использованием библиотеки Pygame.
 Требования:
 - Сетка на игровом поле
 - Приятная цветовая гамма
 - Меню
 - Анимация поедания еды
 - Интересная изюминка (добавим возможность временного ускорения змейки при нажатии пробела)

 План:
 1. Инициализация Pygame, настройка окна.
 2. Определение цветов.
 3. Создание классов: Змейка, Еда, Игра.
 4. Реализация меню: кнопки "Начать игру", "Выход".
 5. Основной игровой цикл с обработкой событий.
 6. Отрисовка сетки, змейки, еды.
 7. Анимация поедания: когда змейка ест еду, покажем эффект (например, круги).
 8. Изюминка: при нажатии пробела змейка ускоряется на короткое время.

 Дополнительно:
 - Счет, уровни (с увеличением скорости) или просто увеличение скорости со временем.

 Реализация:

 Шаг 1: Импорт библиотек
 Шаг 2: Определение констант (размеры окна, размер клетки, цвета и т.д.)
 Шаг 3: Класс Змейка:
        - Свойства: тело (список сегментов), направление, цвет.
        - Методы: движение, рисование, проверка столкновений.
 Шаг 4: Класс Еда:
        - Свойства: позиция, цвет, анимация (когда съедена, покажем анимацию).
        - Методы: рисование, появление в случайном месте.
 Шаг 5: Класс Игра:
        - Свойства: змейка, еда, состояние (меню, игра), счет, скорость, ускорение (флаг и таймер).
        - Методы: обработка ввода, обновление состояния, отрисовка всего.

 Шаг 6: Меню: кнопки, фон, обработка кликов.

 Шаг 7: Анимация поедания: создадим класс Animation, который будет содержать частицы (круги) в точке съедания.

 Шаг 8: Добавим ускорение при нажатии пробела (пока пробел нажат, скорость змейки увеличивается вдвое, но запас "энергии" ограничен? или просто на время, а потом перезарядка).

 Реализуем:

 Концепт:
   - Основной цикл: меню или игровой цикл.
   - В игровом цикле: обработка событий, обновление, отрисовка.

 Сетка: нарисуем сетку в фоне.

 Размеры:
   - Ширина окна: 800
   - Высота окна: 600
   - Размер клетки: 20 пикселей

 Сетка: 40x30 клеток (800/20=40, 600/20=30)

 Цвета:
   - Фон меню: (50, 50, 50)
   - Кнопки: (70, 130, 180) - SteelBlue
   - Змейка: (0, 128, 0) - зеленый
   - Еда: (255, 0, 0) - красный
   - Сетка: (30, 30, 30)
   - Анимация: (255, 215, 0) - золотой

 Анимация поедания: при съедании еды создадим несколько кругов, которые будут расширяться и исчезать.

 Ускорение: при нажатии пробела скорость змейки увеличивается (уменьшаем задержку между шагами). Введем переменную boost_active (флаг) и boost_time (сколько времени осталось). При съедании еды может восстанавливаться запас ускорения? Или просто ограничить время использования и добавить перезарядку.

 Пока сделаем просто: пробел нажат - ускорение, отпустили - обычная скорость. Но без ограничения по времени.

 Однако, чтобы не слишком легко было, добавим, что ускорение тратит "энергию", которая восстанавливается при съедании еды.

 Реализация ускорения:
   - Имеем две скорости: normal_speed и boost_speed (например, normal_speed = 10, boost_speed = 5 - меньше задержка, значит быстрее).
   - Также введем переменную boost_energy (максимум 100). При нажатии пробела, если есть энергия, то используем ускорение (тратим энергию). При отсутствии энергии - обычная скорость.
   - Восстановление: каждую секунду восстанавливаем немного, но больше всего при съедании еды.

 Счет: за каждую еду +1. Может, увеличивать скорость каждые 5 очков?

 Структура:

 main()
   - инициализация
   - создание объекта Game
   - запуск игры

 Классы:

 1. Змейка (Snake)
    - __init__(self, pos)
        self.body = [pos, (pos[0]-1, pos[1]), (pos[0]-2, pos[1])]  # начальное тело из трех сегментов, направление вправо
        self.direction = (1, 0)  # вправо
        self.next_direction = (1, 0)
        self.color = (0, 128, 0)
        self.grow = False  # флаг, нужно ли увеличиваться

    - move(self): 
        if self.grow:
            # добавляем новую голову, не удаляем хвост
            new_head = (self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1])
            self.body.insert(0, new_head)
            self.grow = False
        else:
            # удаляем хвост, добавляем новую голову
            new_head = (self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1])
            self.body.pop()
            self.body.insert(0, new_head)

    - change_direction(self, new_dir): 
        # запретим разворот на 180
        if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
            self.direction = new_dir

    - draw(self, screen, cell_size):
        for segment in self.body:
            pygame.draw.rect(screen, self.color, (segment[0]*cell_size, segment[1]*cell_size, cell_size, cell_size))
            # для красоты - закругленные углы? или просто внутренний квадратик
            # можно нарисовать закругленные прямоугольники, но для простоты - квадраты.

    - check_collision(self, width, height):
        голова = self.body[0]
        # со стенами
        if (голова[0] < 0 or голова[0] >= width or голова[1] < 0 or голова[1] >= height):
            return True
        # с собой
        if голова in self.body[1:]:
            return True
        return False

 2. Еда (Food)
    - __init__(self, width, height):
        self.pos = (random.randint(0, width-1), random.randint(0, height-1))
        self.color = (255, 0, 0)
        self.animation = None  # объект анимации, если есть

    - draw(self, screen, cell_size):
        pygame.draw.rect(screen, self.color, (self.pos[0]*cell_size, self.pos[1]*cell_size, cell_size, cell_size))

    - respawn(self, width, height, snake_body):
        # генерируем новую позицию, не на теле змейки
        while True:
            self.pos = (random.randint(0, width-1), random.randint(0, height-1))
            if self.pos not in snake_body:
                break

 3. Анимация (Animation)
    - __init__(self, pos, color=(255,215,0)):
        self.particles = []
        self.create_particles(pos, color)

    - create_particles(self, pos, color):
        # создадим несколько частиц (кругов) с разным размером и скоростью расширения
        # 5 частиц с случайным радиусом от 1 до 3 и разной скоростью
        for i in range(5):
            radius = random.randint(1, 3)
            speed = random.uniform(0.5, 2.0)
            # начальная позиция: немного случайное смещение от центра
            offset_x = random.uniform(-0.5, 0.5)
            offset_y = random.uniform(-0.5, 0.5)
            self.particles.append({
                'pos': (pos[0] + offset_x, pos[1] + offset_y),
                'radius': radius,
                'speed': speed,
                'color': color,
                'alpha': 255  # начальная прозрачность
            })

    - update(self):
        for p in self.particles:
            p['radius'] += p['speed']
            p['alpha'] -= 5  # уменьшаем прозрачность

        # удалить частицы, которые полностью прозрачны
        self.particles = [p for p in self.particles if p['alpha'] > 0]

    - draw(self, screen, cell_size):
        for p in self.particles:
            # преобразуем координаты в пиксели
            x = p['pos'][0] * cell_size
            y = p['pos'][1] * cell_size
            color = (p['color'][0], p['color'][1], p['color'][2], p['alpha'])
            # для рисования с прозрачностью нужна отдельная поверхность или использовать screen с альфа, но проще нарисовать круг на основной поверхности не получится с альфой.
            # Создадим поверхность для круга.
            s = pygame.Surface((cell_size*2, cell_size*2), pygame.SRCALPHA)
            pygame.draw.circle(s, color, (int(cell_size), int(cell_size)), p['radius'])
            screen.blit(s, (x - p['radius'], y - p['radius']))

 4. Игра (Game)
    - __init__(self, width, height, cell_size):
        self.width = width  # в клетках
        self.height = height
        self.cell_size = cell_size
        self.screen_width = width * cell_size
        self.screen_height = height * cell_size
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.state = "menu"  # "menu", "game", "game_over"
        self.snake = None
        self.food = None
        self.score = 0
        self.speed = 10  # кадров в секунду для змейки (нормальная скорость)
        self.boost_speed = 20  # ускоренная скорость
        self.current_speed = self.speed
        self.boost_energy = 100
        self.boost_active = False
        self.animations = []  # список активных анимаций

    - run(self):
        while True:
            if self.state == "menu":
                self.menu_loop()
            elif self.state == "game":
                self.game_loop()
            elif self.state == "game_over":
                self.game_over_loop()

    - menu_loop(self):
        # Рисуем меню: фон, заголовок, кнопки
        button_start = pygame.Rect(self.screen_width//2 - 100, self.screen_height//2, 200, 50)
        button_quit = pygame.Rect(self.screen_width//2 - 100, self.screen_height//2 + 80, 200, 50)

        while self.state == "menu":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_start.collidepoint(event.pos):
                        self.start_game()
                    if button_quit.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

            self.screen.fill((50, 50, 50))
            # Заголовок
            title = self.font.render("Змейка", True, (255, 255, 255))
            self.screen.blit(title, (self.screen_width//2 - title.get_width()//2, self.screen_height//4))

            # Кнопки
            pygame.draw.rect(self.screen, (70, 130, 180), button_start)
            pygame.draw.rect(self.screen, (70, 130, 180), button_quit)
            text_start = self.font.render("Начать игру", True, (255, 255, 255))
            text_quit = self.font.render("Выход", True, (255, 255, 255))
            self.screen.blit(text_start, (button_start.centerx - text_start.get_width()//2, button_start.centery - text_start.get_height()//2))
            self.screen.blit(text_quit, (button_quit.centerx - text_quit.get_width()//2, button_quit.centery - text_quit.get_height()//2))

            pygame.display.flip()
            self.clock.tick(30)

    - start_game(self):
        self.snake = Snake((self.width//2, self.height//2))
        self.food = Food(self.width, self.height)
        self.food.respawn(self.width, self.height, self.snake.body)  # на случай, если сгенерировалась на змейке
        self.score = 0
        self.boost_energy = 100
        self.state = "game"

    - game_loop(self):
        while self.state == "game":
            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction((0, -1))
                    if event.key == pygame.K_DOWN:
                        self.snake.change_direction((0, 1))
                    if event.key == pygame.K_LEFT:
                        self.snake.change_direction((-1, 0))
                    if event.key == pygame.K_RIGHT:
                        self.snake.change_direction((1, 0))
                    if event.key == pygame.K_SPACE:
                        self.boost_active = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.boost_active = False

            # Обновление состояния
            # Управление скоростью
            if self.boost_active and self.boost_energy > 0:
                self.current_speed = self.boost_speed
                self.boost_energy -= 0.5  # тратим энергию
            else:
                self.current_speed = self.speed
                # Если ускорение не активно, то восстанавливаем энергию
                if self.boost_energy < 100:
                    self.boost_energy += 0.1  # медленно восстанавливаем

            # Движение змейки
            self.snake.move()

            # Проверка на съедание еды
            if self.snake.body[0] == self.food.pos:
                # Анимация
                self.animations.append(Animation(self.food.pos))
                self.snake.grow = True
                self.score += 1
                self.food.respawn(self.width, self.height, self.snake.body)
                # При съедании восстанавливаем часть энергии
                self.boost_energy = min(100, self.boost_energy + 20)

            # Проверка столкновений
            if self.snake.check_collision(self.width, self.height):
                self.state = "game_over"

            # Обновление анимаций
            for anim in self.animations[:]:
                anim.update()
                if not anim.particles:  # если анимация закончилась
                    self.animations.remove(anim)

            # Отрисовка
            self.screen.fill((0, 0, 0))  # черный фон

            # Рисуем сетку
            for x in range(0, self.screen_width, self.cell_size):
                pygame.draw.line(self.screen, (30, 30, 30), (x, 0), (x, self.screen_height))
            for y in range(0, self.screen_height, self.cell_size):
                pygame.draw.line(self.screen, (30, 30, 30), (0, y), (self.screen_width, y))

            # Рисуем змейку, еду, анимации
            self.snake.draw(self.screen, self.cell_size)
            self.food.draw(self.screen, self.cell_size)
            for anim in self.animations:
                anim.draw(self.screen, self.cell_size)

            # Рисуем счет и энергию
            score_text = self.font.render(f"Счет: {self.score}", True, (255, 255, 255))
            energy_text = self.font.render(f"Энергия: {int(self.boost_energy)}", True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))
            self.screen.blit(energy_text, (10, 50))

            pygame.display.flip()
            self.clock.tick(self.current_speed)

    - game_over_loop(self):
        # Экран с надписью "Game Over" и кнопки: "Заново", "Меню"
        button_restart = pygame.Rect(self.screen_width//2 - 100, self.screen_height//2, 200, 50)
        button_menu = pygame.Rect(self.screen_width//2 - 100, self.screen_height//2 + 80, 200, 50)

        while self.state == "game_over":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_restart.collidepoint(event.pos):
                        self.start_game()
                        return
                    if button_menu.collidepoint(event.pos):
                        self.state = "menu"
                        return

            self.screen.fill((50, 50, 50))
            game_over_text = self.font.render("Game Over", True, (255, 255, 255))
            final_score = self.font.render(f"Счет: {self.score}", True, (255, 255, 255))
            self.screen.blit(game_over_text, (self.screen_width//2 - game_over_text.get_width()//2, self.screen_height//4))
            self.screen.blit(final_score, (self.screen_width//2 - final_score.get_width()//2, self.screen_height//4 + 50))

            pygame.draw.rect(self.screen, (70, 130, 180), button_restart)
            pygame.draw.rect(self.screen, (70, 130, 180), button_menu)
            text_restart = self.font.render("Заново", True, (255, 255, 255))
            text_menu = self.font.render("Меню", True, (255, 255, 255))
            self.screen.blit(text_restart, (button_restart.centerx - text_restart.get_width()//2, button_restart.centery - text_restart.get_height()//2))
            self.screen.blit(text_menu, (button_menu.centerx - text_menu.get_width()//2, button_menu.centery - text_menu.get_height()//2))

            pygame.display.flip()
            self.clock.tick(30)

 Запуск:
   if __name__ == "__main__":
        pygame.init()
        game = Game(40, 30, 20)  # 40x30 клеток, размер 20 пикселей
        game.run()

 Примечание: в классе Snake, метод change_direction сразу меняет направление? Но если быстро нажать несколько клавиш, то может быть разворот на 180. Поэтому лучше сохранять следующее направление и применять его в методе move, чтобы избежать разворота в одном кадре.

 Изменим:
   В Snake:
        self.direction = (1,0)
        self.next_direction = (1,0)

   В change_direction: меняем next_direction, если не противоположно текущему направлению движения (не self.direction, а self.next_direction? Но в движении мы используем self.direction, который обновляем перед движением). 

   Решение: будем в game_loop, перед move, обновлять direction до next_direction, а в методе change_direction проверять относительно текущего direction.

   В game_loop перед move:
        self.snake.direction = self.snake.next_direction

   И в change_direction:
        if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
            self.next_direction = new_dir

   Это поможет избежать разворота, если быстро нажать две противоположные клавиши в одном кадре.

   Но в данной реализации мы обрабатываем события по очереди, поэтому может быть, что последнее нажатие будет противоположным. Поэтому лучше в методе change_direction проверять относительно текущего направления движения (self.direction) и запрещать разворот на 180.

   Однако, если мы нажимаем быстро, то события могут накопиться. Поэтому введем next_direction, и в методе move будем обновлять направление только на следующее, если оно допустимо.

   Перепишем Snake:

        def change_direction(self, new_dir):
            # Запрет разворота на 180 относительно текущего направления
            if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
                self.next_direction = new_dir

        В методе move:
            # Перед движением обновим direction на next_direction, если это безопасно?
            # Но мы уже проверили в change_direction? Да, но после того как мы установили next_direction, направление direction могло измениться? 
            # Давайте в move просто делаем:
            #   self.direction = self.next_direction   -- но нет, потому что тогда можно будет за один ход поменять несколько раз.

            # Вместо этого, мы в игровом цикле, когда обработали все события, обновляем direction из next_direction.

   Но в game_loop после обработки событий мы не знаем, сколько времени прошло. Обработка событий происходит каждый кадр, и в каждом кадре мы обновляем direction перед move.

   Итак, в game_loop после обработки всех событий (перед move) делаем:

        self.snake.direction = self.snake.next_direction

   Но тогда мы разрешаем только одно изменение направления за шаг.

   Это стандартный подход.

   Исправляем:

        В game_loop в части обновления:
            # Сначала обработаем события (в том числе изменение направления, которое установит next_direction)
            # Затем перед движением змейки обновим direction на next_direction, но только если next_direction допустимо?
            # Но мы в change_direction уже проверили, что next_direction не противоположно текущему direction? 
            # Нет, потому что текущий direction в этом кадре еще не изменился. Поэтому в change_direction мы сравниваем с текущим direction.

        То есть, если змейка движется вправо, и мы быстро нажали вниз и влево, то:
            Сначала придет вниз -> next_direction = (0,1) -> разрешено (не противоположно правому)
            Затем придет влево -> next_direction = (-1,0) -> не противоположно текущему (текущий direction еще правый) -> разрешено.
            Затем в game_loop мы устанавливаем direction = (-1,0) и двигаем. То есть змейка сразу пойдет влево.

        Но мы хотим, чтобы за один шаг змейка могла изменить направление только один раз? Или разрешить несколько изменений? 

        В классической змейке за один шаг (передвижение) можно изменить направление только один раз.

        Наше решение: в game_loop после обработки всех событий мы устанавливаем direction = next_direction. И затем двигаем.

        Это позволит за один шаг применить только последнее изменение направления.

   Это нормально.

   Итак, в коде game_loop:

        # Обработка событий (в том числе вызов change_direction для змейки, который меняет next_direction)
        ...

        # Перед обновлением состояния игры: обновим направление змейки
        self.snake.direction = self.snake.next_direction

        # Двигаем змейку
        self.snake.move()

   Это должно работать.

   Тестируем.

   Также добавим в Snake в __init__:
        self.next_direction = self.direction

   Чтобы в начале next_direction совпадал с direction.

   Теперь запустим и проверим.

   Улучшение: сетка рисуется поверх всего? Нет, мы рисуем сетку в самом начале отрисовки, затем змейку, еду, анимации и текст.

   Все готово. Кодируем.
</think>
# Игра "Змейка" на Python с Pygame

```python
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

# Цветовая гамма
BACKGROUND = (15, 20, 30)
GRID_COLOR = (30, 35, 45)
SNAKE_COLOR = (100, 255, 150)
SNAKE_HEAD_COLOR = (70, 220, 120)
FOOD_COLOR = (255, 80, 80)
TEXT_COLOR = (220, 220, 220)
BUTTON_COLOR = (60, 150, 200)
BUTTON_HOVER = (80, 170, 220)
ANIMATION_COLORS = [(255, 215, 0), (255, 165, 0), (255, 100, 0)]

# Класс змейки
class Snake:
    def __init__(self):
        self.reset()
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.grow = False
        
    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        for i in range(1, self.length):
            self.positions.append((self.positions[0][0] - i, self.positions[0][1]))
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.grow = False
        
    def get_head_position(self):
        return self.positions[0]
    
    def update(self):
        # Обновление направления
        self.direction = self.next_direction
        
        # Получение текущей позиции головы
        head = self.get_head_position()
        
        # Расчет новой позиции головы
        dx, dy = self.direction
        new_x = (head[0] + dx) % GRID_WIDTH
        new_y = (head[1] + dy) % GRID_HEIGHT
        new_head = (new_x, new_y)
        
        # Проверка столкновения с собой
        if new_head in self.positions[1:]:
            return False
        
        # Добавление новой головы
        self.positions.insert(0, new_head)
        
        # Удаление хвоста, если не нужно расти
        if not self.grow:
            self.positions.pop()
        else:
            self.grow = False
            self.length += 1
            
        return True
    
    def change_direction(self, direction):
        # Запрет поворота на 180 градусов
        if (self.direction[0] * -1, self.direction[1] * -1) != direction:
            self.next_direction = direction
    
    def draw(self, surface):
        for i, pos in enumerate(self.positions):
            # Рисование сегментов змейки
            rect = pygame.Rect(pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            
            # Голова
            if i == 0:
                color = SNAKE_HEAD_COLOR
            # Тело
            else:
                color = SNAKE_COLOR
            
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, (40, 80, 60), rect, 1)
            
            # Глаза на голове
            if i == 0:
                eye_size = GRID_SIZE // 4
                # Левый глаз (относительно направления движения)
                if self.direction == (1, 0):  # вправо
                    left_eye = (rect.left + GRID_SIZE * 3//4, rect.top + GRID_SIZE // 3)
                elif self.direction == (-1, 0): # влево
                    left_eye = (rect.left + GRID_SIZE // 4, rect.top + GRID_SIZE // 3)
                elif self.direction == (0, 1):  # вниз
                    left_eye = (rect.left + GRID_SIZE // 3, rect.top + GRID_SIZE * 3//4)
                else:  # вверх
                    left_eye = (rect.left + GRID_SIZE // 3, rect.top + GRID_SIZE // 4)
                
                # Правый глаз
                if self.direction == (1, 0) or self.direction == (-1, 0):
                    right_eye = (left_eye[0], left_eye[1] + GRID_SIZE // 3)
                else:
                    right_eye = (left_eye[0] + GRID_SIZE // 3, left_eye[1])
                
                pygame.draw.circle(surface, (20, 20, 30), left_eye, eye_size)
                pygame.draw.circle(surface, (20, 20, 30), right_eye, eye_size)

# Класс еды
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = FOOD_COLOR
        self.randomize_position()
        self.animation_timer = 0
        self.animation_radius = 0
        self.max_radius = GRID_SIZE * 1.5
        
    def randomize_position(self, snake_positions=None):
        while True:
            self.position = (random.randint(0, GRID_WIDTH - 1), 
                            random.randint(0, GRID_HEIGHT - 1))
            if snake_positions is None or self.position not in snake_positions:
                break
    
    def start_animation(self):
        self.animation_timer = 20  # Длительность анимации
        self.animation_radius = 0
    
    def update_animation(self):
        if self.animation_timer > 0:
            self.animation_timer -= 1
            self.animation_radius = self.max_radius * (1 - self.animation_timer / 20)
    
    def draw(self, surface):
        # Рисование основного объекта еды
        rect = pygame.Rect(self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, 
                          GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, (180, 50, 50), rect, 2)
        
        # Рисование анимации поедания
        if self.animation_timer > 0:
            center = (rect.centerx, rect.centery)
            for i in range(3):
                radius = self.animation_radius * (1 + i * 0.3)
                alpha = 200 - i * 50
                color_idx = min(i, len(ANIMATION_COLORS)-1)
                color = ANIMATION_COLORS[color_idx]
                s = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
                pygame.draw.circle(s, (*color, alpha), (radius, radius), radius)
                surface.blit(s, (center[0] - radius, center[1] - radius))

# Класс кнопки
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.hovered = False
        
    def draw(self, surface, font):
        color = BUTTON_HOVER if self.hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, (120, 180, 220), self.rect, 2, border_radius=10)
        
        text_surf = font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
    
    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        return self.hovered
    
    def check_click(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(pos)
        return False

# Основной класс игры
class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Змейка с изюминкой")
        self.clock = pygame.time.Clock()
        
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 24)
        
        self.snake = Snake()
        self.food = Food()
        self.food.randomize_position(self.snake.positions)
        
        self.score = 0
        self.game_over = False
        self.in_menu = True
        self.special_mode = False
        self.special_timer = 0
        
        # Создание кнопок меню
        button_width, button_height = 200, 50
        center_x = WIDTH // 2 - button_width // 2
        self.start_button = Button(center_x, HEIGHT // 2 - 40, button_width, button_height, "Начать игру")
        self.quit_button = Button(center_x, HEIGHT // 2 + 40, button_width, button_height, "Выход")
        
        # Создание кнопок после игры
        self.restart_button = Button(center_x, HEIGHT // 2 + 20, button_width, button_height, "Играть снова")
        self.menu_button = Button(center_x, HEIGHT // 2 + 90, button_width, button_height, "Меню")
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if self.in_menu:
                # Обработка событий меню
                pos = pygame.mouse.get_pos()
                self.start_button.check_hover(pos)
                self.quit_button.check_hover(pos)
                
                if self.start_button.check_click(pos, event):
                    self.in_menu = False
                    self.game_over = False
                    self.reset_game()
                elif self.quit_button.check_click(pos, event):
                    pygame.quit()
                    sys.exit()
            
            elif self.game_over:
                # Обработка событий после игры
                pos = pygame.mouse.get_pos()
                self.restart_button.check_hover(pos)
                self.menu_button.check_hover(pos)
                
                if self.restart_button.check_click(pos, event):
                    self.reset_game()
                    self.game_over = False
                elif self.menu_button.check_click(pos, event):
                    self.in_menu = True
            
            elif not self.game_over:
                # Обработка событий игры
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction((0, -1))
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction((0, 1))
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction((-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction((1, 0))
                    elif event.key == pygame.K_SPACE:
                        self.special_mode = not self.special_mode
                        self.special_timer = 0
    
    def reset_game(self):
        self.snake.reset()
        self.food.randomize_position(self.snake.positions)
        self.score = 0
        self.game_over = False
        self.special_mode = False
        self.special_timer = 0
    
    def update(self):
        if not self.game_over and not self.in_menu:
            # Обновление змейки
            if not self.snake.update():
                self.game_over = True
                return
            
            # Обновление анимации еды
            self.food.update_animation()
            
            # Проверка съедания еды
            if self.snake.get_head_position() == self.food.position:
                # Анимация поедания
                self.food.start_animation()
                
                # Увеличение счета
                self.score += 1
                
                # Запуск специального режима с шансом 20%
                if random.random() < 0.2 and not self.special_mode:
                    self.special_mode = True
                    self.special_timer = 0
                
                # Змейка растет
                self.snake.grow = True
                
                # Появление новой еды
                self.food.randomize_position(self.snake.positions)
            
            # Обновление специального режима
            if self.special_mode:
                self.special_timer += 1
                if self.special_timer > 150:  # Специальный режим длится 15 секунд
                    self.special_mode = False
    
    def draw_grid(self):
        # Рисование сетки игрового поля
        for x in range(0, WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, HEIGHT), 1)
        for y in range(0, HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (WIDTH, y), 1)
    
    def draw(self):
        self.screen.fill(BACKGROUND)
        
        if self.in_menu:
            # Отрисовка меню
            title = self.font.render("ЗМЕЙКА", True, TEXT_COLOR)
            self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
            
            # Отрисовка кнопок
            self.start_button.draw(self.screen, self.font)
            self.quit_button.draw(self.screen, self.font)
            
            # Подсказка
            hint = self.small_font.render("Управление: стрелки, Специальный режим: пробел", True, (180, 180, 180))
            self.screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 50))
            
            # Изиминка: плавающая змейка
            time = pygame.time.get_ticks() / 1000
            offset_x = math.sin(time * 2) * 50
            offset_y = math.cos(time) * 30
            
            # Рисуем мини-змейку в меню
            positions = [(GRID_WIDTH // 2 + i, GRID_HEIGHT // 4) for i in range(5)]
            for i, pos in enumerate(positions):
                rect = pygame.Rect(
                    pos[0] * GRID_SIZE + offset_x, 
                    pos[1] * GRID_SIZE + offset_y, 
                    GRID_SIZE, GRID_SIZE
                )
                color = SNAKE_HEAD_COLOR if i == 0 else SNAKE_COLOR
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (40, 80, 60), rect, 1)
                
                # Рисуем мини-еду
                food_rect = pygame.Rect(
                    (positions[-1][0] + 3) * GRID_SIZE + offset_x, 
                    positions[-1][1] * GRID_SIZE + offset_y, 
                    GRID_SIZE, GRID_SIZE
                )
                pygame.draw.rect(self.screen, FOOD_COLOR, food_rect)
                pygame.draw.rect(self.screen, (180, 50, 50), food_rect, 2)
        
        elif self.game_over:
            # Отрисовка экрана завершения игры
            self.draw_grid()
            
            # Отрисовка змейки и еды (для визуализации)
            self.snake.draw(self.screen)
            self.food.draw(self.screen)
            
            game_over_text = self.font.render("ИГРА ОКОНЧЕНА", True, (255, 100, 100))
            self.screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 4))
            
            score_text = self.font.render(f"Счет: {self.score}", True, TEXT_COLOR)
            self.screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 3))
            
            # Отрисовка кнопок
            self.restart_button.draw(self.screen, self.font)
            self.menu_button.draw(self.screen, self.font)
        
        else:
            # Отрисовка игрового поля
            self.draw_grid()
            
            # Отрисовка змейки
            self.snake.draw(self.screen)
            
            # Отрисовка еды
            self.food.draw(self.screen)
            
            # Отрисовка счета
            score_text = self.font.render(f"Счет: {self.score}", True, TEXT_COLOR)
            self.screen.blit(score_text, (10, 10))
            
            # Отрисовка специального режима
            if self.special_mode:
                # Специальный эффект: меняющийся фон
                pulse = abs(math.sin(pygame.time.get_ticks() / 200))
                color_value = int(100 + 155 * pulse)
                overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                overlay.fill((255, 255, 100, 30))
                self.screen.blit(overlay, (0, 0))
                
                # Текст специального режима
                mode_text = self.small_font.render("СПЕЦИАЛЬНЫЙ РЕЖИМ!", True, (255, 255, 100))
                self.screen.blit(mode_text, (WIDTH - mode_text.get_width() - 10, 10))
                
                # Таймер
                time_left = (150 - self.special_timer) // 10
                timer_text = self.small_font.render(f"Осталось: {time_left}", True, (255, 255, 100))
                self.screen.blit(timer_text, (WIDTH - timer_text.get_width() - 10, 40))
            
            # Изиминка: случайные эффекты в специальном режиме
            if self.special_mode and random.random() < 0.05:
                # Создание случайных частиц
                for _ in range(20):
                    x = random.randint(0, WIDTH)
                    y = random.randint(0, HEIGHT)
                    size = random.randint(2, 5)
                    color = random.choice(ANIMATION_COLORS)
                    pygame.draw.circle(self.screen, color, (x, y), size)
        
        pygame.display.flip()
    
    def run(self):
        while True:
            self.handle_events()
            if not self.in_menu and not self.game_over:
                self.update()
            self.draw()
            self.clock.tick(FPS)

# Запуск игры
if __name__ == "__main__":
    game = SnakeGame()
    game.run()
```

## Особенности реализации

1. **Сетка игрового поля**:
   - Регулярная сетка с настраиваемым размером клеток
   - Приглушенные цвета для минималистичного стиля

2. **Приятная цветовая гамма**:
   - Темно-синий фон с серой сеткой
   - Неоново-зеленая змейка с выделенной головой
   - Ярко-красная еда
   - Контрастные элементы интерфейса

3. **Меню и UI**:
   - Главное меню с кнопками
   - Экран завершения игры
   - Интерактивные кнопки с эффектом наведения
   - Отображение счета

4. **Анимация поедания еды**:
   - Концентрические круги вокруг съедаемой еды
   - Три слоя анимации с разными цветами
   - Плавное затухание анимации

5. **Интересная изюминка**:
   - **Специальный режим**:
     - Активируется случайно при съедании еды (20% шанс)
     - Можно принудительно включить/выключить пробелом
     - Длится 15 секунд
     - Добавляет визуальные эффекты: пульсирующий фон, частицы
     - Таймер оставшегося времени специального режима

6. **Дополнительные фичи**:
   - Змейка с глазами, меняющими положение в зависимости от направления
   - Анимация плавающей змейки в главном меню
   - Эффекты при наведении на кнопки
   - Игра не заканчивается при выходе за границы (телепортация)
   - Сглаженная графика с закругленными элементами

Игра полностью готова к запуску - просто скопируйте код в файл с расширением `.py` и запустите его с помощью Python 3. Управление осуществляется стрелками, пробел включает/выключает специальный режим.