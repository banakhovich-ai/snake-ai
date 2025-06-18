```text
Prompt
- Tokens: 59
- Time: 22913.838 ms
- Speed: 2.6 t/s
Generation
- Tokens: 8915
- Time: 1622339.932 ms
- Speed: 5.5 t/s
```

<think>
Мы создадим игру "Змейка" с использованием библиотеки Pygame.
 Особенности:
   - Игровое поле с сеткой
   - Приятная цветовая гамма
   - Меню (начало, пауза, конец игры)
   - Анимация поедания еды (например, эффект при съедании)
   - Интересная изюминка: добавим возможность ускорения змейки при удерживании клавиши (или что-то подобное, но чтобы не усложнять, можно сделать, что змейка растет не на 1 сегмент, а на 2 при съедании определенной еды, но для начала сделаем классику, а потом добавим изюминку)

 План:
   1. Инициализация Pygame и настройка окна.
   2. Определение цветов.
   3. Создание классов: Змейка, Еда, Игра.
   4. Реализация движения змейки.
   5. Обработка столкновений (со стенами и с собой).
   6. Меню: начальное, пауза, конец игры.
   7. Анимация поедания еды (можем сделать вспышку или эффект частиц, но для простоты начнем с вспышки).
   8. Сетка на поле.

 Изюминка: пусть иногда появляется "особая" еда, которая дает больше очков и заставляет змейку расти быстрее (например, на 3 сегмента) и при этом дает временное ускорение. Также при съедании обычной еды, змейка растет на 1. Специальная еда будет появляться реже и исчезать через некоторое время.

 Однако, чтобы не слишком усложнять, можно сначала сделать базовую версию, а потом добавить эту изюминку.

 Но по условию требуется интересная изюминка, поэтому добавим:
   - Обычная еда (зеленая) - добавляет 1 очко, змейка растет на 1 сегмент.
   - Особая еда (красная) - появляется редко (раз в 5 обычных ед), добавляет 5 очков, змейка растет на 3 сегмента, и на короткое время (на 10 шагов) скорость змейки увеличивается.

 Также добавим меню с кнопками:
   - Начать игру
   - Выход

 При паузе (по нажатию клавиши ESC) покажем меню паузы.

 Анимацию поедания сделаем так: при съедании еды, в месте съедания на несколько кадров отобразим эффект (например, круги, расходящиеся от центра).

 Но для начала структура:

 Классы:
   - Game: основной класс игры, содержит игровой цикл, обработку событий, отрисовку.
   - Snake: змейка, содержит список сегментов, направление, методы для движения, рисования, проверки столкновений.
   - Food: еда, имеет координаты, тип (обычная или особая), метод отрисовки.
   - SpecialFood: наследник от Food, с дополнительным поведением (исчезает через время).

 Однако, можно обойтись без наследования, просто в классе Food добавить атрибут `special`.

 Шаги:

 1. Настройка Pygame и окна.
 2. Цвета.
 3. Класс Snake.
 4. Класс Food.
 5. Меню.
 6. Эффекты.

 Начнем с базовой реализации.

 Важно: Сетка рисуется как горизонтальные и вертикальные линии.

 Для анимации поедания: будем хранить список эффектов (координаты, время жизни). При съедании добавляем эффект в список и обновляем его в каждом кадре.

 Для меню: создадим функции, которые будут рисовать кнопки и обрабатывать клики.

 Изюминка: особая еда с временным эффектом ускорения и большим ростом.

 Реализуем:

   - В классе Game: два типа еды. Обычная еда и особая еда. Обычная появляется всегда, а особая с вероятностью 20% каждые 5 съеденных обычных ед (или просто раз в 5 ед? или случайно). Или можно по времени? Лучше: каждые 10 очков появляется особая еда, и она живет 50 шагов змейки, потом исчезает.

  Но для простоты: пусть особые еды появляются случайно с малой вероятностью каждые 10 кадров (но это не привязано к очкам). Или раз в 5 съеденных ед? Счетчик съеденной еды: при съедании обычной еды увеличиваем счетчик. Если счетчик кратен 5, то создаем особую еду (но только одну, и если она уже есть, то не создаем).

  Однако, можно сделать, что особые еды появляются независимо от обычных, но реже. И они исчезают через 100 кадров.

 Реализация:

   В классе Game:
     foods = []  # список еды (и обычная, и особая). Обычная еда всегда одна? Нет, в классике одна. Но у нас два типа, и они могут быть одновременно. Пусть одновременно на поле одна обычная и одна особенная (но не обязательно).

   Правила:
     - Обычная еда всегда одна на поле. Когда съедена, создается новая обычная.
     - Особая еда появляется редко и существует ограниченное время. Одновременно может быть только одна особая еда.

   Алгоритм появления особой еды:
     - Будем иметь счетчик: special_food_counter. Каждые 100 кадров (или каждые 10 съеденных обычных ед) создаем особую еду, если ее еще нет.

   Или по времени: каждые 10 секунд (если нет особой еды).

   Но для простоты: каждые 500 кадров (если счетчик достиг 500, то создаем особую еду и сбрасываем счетчик). Но если особая еда уже есть, то не создаем. А если создали, то счетчик сбрасываем.

   Также добавим, что особая еда исчезает через 300 кадров (если не съедена).

   При съедении особой еды:
        - увеличиваем счет на 5
        - увеличиваем длину змейки на 3
        - устанавливаем эффект ускорения на 50 кадров (скорость змейки увеличивается в 2 раза)

   Скорость змейки: у нас обычно шаг через определенное количество кадров (например, каждые 10 кадров). При ускорении - каждые 5 кадров.

   Также нужно, чтобы эффект ускорения пропал через 50 кадров.

   Для этого в змейке можно хранить:
        speed_boost = 0   # оставшееся время (в кадрах) ускорения

   И в каждом кадре уменьшать на 1, если >0.

   А скорость движения: если speed_boost > 0, то двигаем каждые 5 кадров, иначе каждые 10.

   Но у нас игровой цикл с постоянной частотой кадров (например, 30 FPS). Тогда можно установить два таймера для движения: обычный и ускоренный.

   Или можно хранить счетчик кадров для движения: 
        В каждом кадре: если ускорение, то двигаем каждые 5 кадров, иначе каждые 10.

   Но тогда движение будет неравномерным. Лучше хранить время последнего движения, и двигать по истечении интервала.

   Для простоты: будем обновлять змейку не каждый кадр, а по таймеру.

   Вместо этого можно использовать переменную `frames` для отслеживания времени.

   Идея:

        frames += 1
        if frames % (10 if not speed_boost else 5) == 0:
            snake.move()

   Но при этом frames растет непрерывно, и при ускорении движение будет вдвое чаще.

   Однако, при снятии ускорения интервал снова станет 10.

   Но что, если frames кратно и 5 и 10? Тогда при переходе из ускорения в обычный режим, если frames%10==0, то мы переместимся? Да, но после ускорения мы пропустим несколько шагов? Не обязательно: если мы в ускорении двигаемся каждые 5 кадров, то при снятии ускорения следующий шаг будет на 10 кадров? Нет, потому что мы в каждом кадре проверяем: если ускорение, то двигаем каждые 5, иначе каждые 10. Но если сняли ускорение, то счетчик кадров frames продолжает расти, и если мы в кадре, который делится на 5, но не делится на 10, то мы не двигаем. Так что будет пропуск.

   Лучше хранить отдельный счетчик шагов для движения.

   Альтернатива: использовать время (в миллисекундах) и двигать по времени.

   Но для простоты будем использовать счетчик кадров и условие:

        move_interval = 5 if speed_boost else 10
        if frames % move_interval == 0:
            snake.move()

   Проблема: когда снимается ускорение, счетчик frames не сбрасывается, и если после снятия ускорения frames % 10 не равен 0, то змейка не двинется пока не наступит следующий интервал. Это задержка до 9 кадров.

   Чтобы избежать задержки, можно хранить счетчик времени с последнего движения.

   Будем делать так:

        current_time = pygame.time.get_ticks()
        move_interval = 100 if speed_boost else 200   # миллисекунды

        if current_time - last_move_time >= move_interval:
            snake.move()
            last_move_time = current_time

   Это более правильно.

   Поэтому перестроим движение на основе времени.

   Но в нашем простом случае, если мы не хотим усложнять, можно и на кадрах, но будем использовать второй вариант.

   Однако, для простоты кода, давайте пока оставим на кадрах, но будем сбрасывать счетчик frames при изменении состояния ускорения.

   При съедании особой еды:
        - устанавливаем speed_boost = 50   (в кадрах)
        - сбрасываем счетчик frames в 0? не обязательно.

   Но тогда движение в первый же кадр после съедания? Да, но мы можем не двигаться, если frames не кратно интервалу. Поэтому лучше сбросить счетчик движения.

   Однако, мы можем изменить систему: будем хранить отдельно счетчик для движения. Не привязываться к frames, а иметь:

        move_counter = 0

        В основном цикле:
          move_counter += 1
          if speed_boost:
            required = 5
          else:
            required = 10
          if move_counter >= required:
            move_counter = 0
            snake.move()

   Тогда при изменении состояния ускорения, мы просто меняем required, и move_counter уже накоплен. И при следующем кадре, если move_counter >= required, то движение произойдет.

   Этот способ не вызывает задержки, потому что мы используем накопление.

   Пример: 
        Допустим, мы были в обычном режиме (required=10) и у нас move_counter=8.
        Затем мы съели особую еду, теперь required=5.
        В следующем кадре: move_counter становится 9 -> не двигаем.
          Но 9 >= 5 -> да, двигаем! И сбрасываем move_counter в 0.

   Это неправильно, потому что в обычном режиме мы накопили 8, а после ускорения мы должны были двигаться уже через 1 кадр (8+1=9, что больше 5?).

   Правильнее: когда меняется режим, не сбрасывать счетчик, а просто продолжить накопление. Но тогда движение может произойти слишком быстро.

   Чтобы этого избежать, можно оставить как есть, но тогда при ускорении мы двигаемся сразу же, если move_counter накопил хотя бы 5? А если до этого мы были в обычном режиме и накопили 8, то сразу двигаем.

   Но это нормально: змейка ускорилась и должна сразу отреагировать.

   Поэтому так и сделаем.

   В коде:

        move_counter = 0
        required = 10   # обычная скорость

        В цикле:
            move_counter += 1
            current_required = 5 if speed_boost > 0 else 10
            if move_counter >= current_required:
                snake.move()
                move_counter = 0

   При этом, если состояние ускорения изменилось, то в следующем кадре мы сравним move_counter (который уже >0) с новым current_required. Если current_required уменьшилось (5 вместо 10), то условие выполнится.

   Это нормально.

   Теперь о змейке:

        Класс Snake:
            __init__(self, ...)
            body = []   # список сегментов (каждый сегмент - (x, y))
            direction = (1,0)   # начальное направление вправо

        move(self):
            # добавляем новую голову в зависимости от направления
            # и если не съедена еда, то удаляем хвост

        draw(self, screen): # рисуем каждый сегмент

        check_collision(self): # с собой и стенами

   Еда:

        Класс Food:
            pos = (x, y)   # в пределах сетки
            special = False

        draw(self, screen): 
            if special:
                color = RED
            else:
                color = GREEN

        В игре:
            food_list = [обычная еда] + (особая еда, если есть)

   Обработка съедания:

        Проверяем, если голова змейки совпадает с позицией еды.
        Если съели обычную:
            очки += 1
            длина змейки увеличивается (не удаляем хвост в следующем шаге N раз, где N=1) -> для этого в змейке в методе move мы обычно удаляем хвост, но если нужно увеличить, то в этом шаге не удаляем. Но обычно в классике: при съедании устанавливаем флаг, что съели, и при движении мы добавляем голову, но не удаляем хвост. И только после этого снимаем флаг.

        Поэтому в классе Snake добавим:
            grow = 0   # на сколько сегментов нужно вырасти

        При съедании обычной еды: snake.grow += 1
        При съедании особой: snake.grow += 3

        В методе move:
            # добавляем новую голову
            # если grow > 0, то не удаляем хвост и уменьшаем grow на 1
            # иначе удаляем хвост

   Это классический подход.

   Теперь о сетке:

        Рисуем сетку: вертикальные и горизонтальные линии с шагом GRID_SIZE.

   Цвета:

        BACKGROUND = (15, 15, 15)   # темно-серый
        GRID_COLOR = (40, 40, 40)
        SNAKE_COLOR = (0, 255, 0)
        FOOD_COLOR = (255, 0, 0)
        SPECIAL_FOOD_COLOR = (255, 165, 0)   # оранжевый

   Меню:

        Будем иметь состояние игры: 
          'menu', 'playing', 'pause', 'game_over'

        В состоянии 'menu' рисуем меню с кнопками "Начать игру", "Выход".
        В 'playing' - основной игровой процесс.
        В 'pause' - при нажатии ESC, показываем меню паузы (продолжить, выйти в меню).
        В 'game_over' - показываем итоги и кнопки (снова играть, меню).

   Анимация поедания:

        Эффект: в момент съедания еды, рисуем несколько кругов, которые расширяются и исчезают.

        Класс Effect:
            def __init__(self, pos):
                self.pos = pos
                self.radius = 0
                self.max_radius = 20
                self.speed = 5   # скорость роста радиуса
                self.lifetime = 20   # сколько кадров живет

            def update(self):
                self.radius += self.speed
                self.lifetime -= 1
                if self.lifetime <= 0:
                    return False   # удалить
                return True

            def draw(self, screen):
                alpha = min(255, self.lifetime * 12)   # чтобы угасал
                color = (255, 255, 0, alpha)   # желтый, с прозрачностью
                pygame.draw.circle(screen, color, self.pos, self.radius, 1)

        Но для простоты без прозрачности: тогда цвет будет меняться.

        Но в Pygame рисование с прозрачностью сложнее, поэтому сделаем просто желтые круги, которые увеличиваются и исчезают по времени.

        Однако, мы не можем использовать прозрачность без создания поверхности с альфа-каналом.

        Поэтому просто нарисуем несколько колец с увеличивающимся радиусом и уменьшающейся толщиной? Или просто кольца, которые становятся больше и бледнее.

        Но для начала сделаем без прозрачности: цвет фона с прозрачностью мы не можем легко менять. Поэтому просто нарисуем кольцо желтым, которое расширяется и исчезает.

        Вместо этого можно сделать частицы? Но для простоты ограничимся одним эффектом на каждое съедание.

        В игре храним список эффектов: effects = []

        При съедании еды (любой) создаем эффект в позиции еды и добавляем в список.

        В основном цикле обновляем и удаляем те, которые закончились.

   Начнем писать.

   Из-за сложности, мы не будем реализовывать абсолютно все детали, но постараемся.

   Код будет длинным, но структурированным.

   Размеры:
        WIDTH, HEIGHT = 800, 600
        GRID_SIZE = 20   # размер клетки

        Тогда поле в клетках: 
            grid_width = WIDTH // GRID_SIZE
            grid_height = HEIGHT // GRID_SIZE

   Координаты змейки и еды - в клетках, затем при рисовании умножаем на GRID_SIZE.

   Движение: направление в клетках (не в пикселях).

   Начальная позиция змейки: центр.

   Направление: вправо.

   Еда: случайная позиция (но не на змейке).

   Реализуем проверку при генерации еды: не попадать на змейку.

   Теперь приступим к кодированию.
</think>
# Игра "Змейка" на Python с изюминкой

Вот готовая игра "Змейка" с красивым дизайном, анимацией поедания, меню и интересной особенностью - возможностью проходить сквозь стены!

```python
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
```

## Особенности игры:

1. **Сетка и цветовая гамма**:
   - Игровое поле имеет сетку
   - Приятная темная цветовая гамма с акцентами на змейку и еду

2. **Меню**:
   - Главное меню с кнопками "Начать игру" и "Выход"
   - Экран завершения игры с кнопками "Играть снова" и "В меню"

3. **Анимация поедания еды**:
   - При съедении еды появляются частицы, которые разлетаются в разные стороны
   - Особенная еда пульсирует для привлечения внимания

4. **Изюминка**:
   - Змейка может проходить сквозь стены и появляться с противоположной стороны
   - Особая еда (желтая) дает 3 очка и увеличивает длину змейки на 3 сегмента
   - При съедении особой еды змейка входит в "супер режим" с индикатором на экране

5. **Дополнительные особенности**:
   - Глаза у змейки, которые меняют положение в зависимости от направления
   - Счетчик очков
   - Плавные анимации и эффекты
   - Интуитивно понятное управление стрелками

Чтобы запустить игру, просто сохраните код в файл `snake.py` и запустите его с помощью Python (требуется установленный Pygame). Управление осуществляется стрелками клавиатуры.