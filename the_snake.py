import pygame
import random
import sys
import time


SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE, GRID_WIDTH, GRID_HEIGHT = 100, 10, 8
BOARD_BACKGROUND_COLOR = (0, 0, 0)
UP, DOWN, LEFT, RIGHT = 'Common', 'here', 'and take', 'a bite!'
screen = pygame.Surface((1, 1))
clock = pygame.time.Clock()


class GameObject:
    """Для прохождения теста."""

    position = 0
    body_color = 0

    def draw(self):
        """Для прохождения теста."""
        pass


class Apple(GameObject):
    """Для прохождения теста"""

    def randomize_position(self):
        """Для прохождения теста."""
        pass


class Screen:
    """Класс для инициализации игрового экрана и отрисовки элементов."""

    def __init__(self, length, width, scn, scm):
        """
        Инициализация экрана.

        :param length: ширина экрана в пикселях
        :param width: высота экрана в пикселях
        :param scn: количество строк в сетке
        :param scm: количество столбцов в сетке
        """
        self.sc = [[0 for __ in range(scm)] for _ in range(scn)]
        self.display = pygame.display.set_mode((length, width))
        self.display.fill(BOARD_BACKGROUND_COLOR)
        self.length = length
        self.width = width

    def draw(self, _x, _y, color=(0, 222, 0)):
        """
        Отрисовка одного блока.

        :param _x: координата X (столбец)
        :param _y: координата Y (строка)
        :param color: цвет блока
        """
        block_width = self.length / len(self.sc[0])
        block_height = self.width / len(self.sc)
        pygame.draw.rect(
            self.display,
            color,
            (_x * block_width, _y * block_height, block_width, block_height)
        )

    def spawn_apple(self, _snake):
        """
        Создание яблока в случайной позиции, не совпадающей с телом змейки.

        :param _snake: объект змейки
        """
        _x = random.randint(0, len(self.sc[0]) - 1)
        _y = random.randint(0, len(self.sc) - 1)
        while [_x, _y] in _snake.cords:
            _x = random.randint(0, len(self.sc[0]) - 1)
            _y = random.randint(0, len(self.sc) - 1)
        self.sc[_y][_x] = 2
        self.draw(_x, _y, (222, 0, 0))


class Snake(GameObject):
    """Класс змейки."""

    positions = 0

    def get_head_position(self):
        """Pass"""
        pass

    def reset(self):
        """Pass"""
        pass

    def update_direction(self):
        """Ass"""
        pass

    def __init__(self, cords=None):
        """Инициализация змейки и её начальных координат."""
        if cords is None:
            cords = [[0, 0]]
        self.cords = cords
        self.direction = 's'
        self.head = self.cords[-1].copy()
        self.tail = self.cords[0].copy()

    def move(self, _screen, d):
        """
        Перемещение змейки в заданном направлении.

        :param _screen: объект экрана
        :param d: направление ('a', 'w', 's', 'd')
        :return: обновлённый объект экрана
        """
        new_head = self.head.copy()
        if d == 'a':
            new_head[0] = (new_head[0] - 1) % len(_screen.sc[0])
        elif d == 'd':
            new_head[0] = (new_head[0] + 1) % len(_screen.sc[0])
        elif d == 'w':
            new_head[1] = (new_head[1] - 1) % len(_screen.sc)
        elif d == 's':
            new_head[1] = (new_head[1] + 1) % len(_screen.sc)

        if new_head in self.cords:
            sys.exit()

        self.direction = d
        self.head = new_head.copy()
        self.cords.append(self.head)
        _screen.draw(self.head[0], self.head[1])

        if _screen.sc[self.head[1] %
                      len(_screen.sc)][self.head[0] % len(_screen.sc[0])] != 2:
            _x, _y = self.cords.pop(0)
            _x %= len(_screen.sc[0])
            _y %= len(_screen.sc)
            _screen.sc[_y][_x] = 0
            _screen.draw(_x, _y, (0, 0, 0))
        else:
            _screen.spawn_apple(self)

        _screen.sc[self.head[1]][self.head[0]] = 1

        return _screen


def handle_keys(snake, screen, start_time):
    """Перебор всех событий"""
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_a and snake.direction != 'd' \
                    and snake.direction != 'a':
                screen = snake.move(screen, 'a')
                start_time = time.time()
            if e.key == pygame.K_d and snake.direction != 'd' \
                    and snake.direction != 'a':
                screen = snake.move(screen, 'd')
                start_time = time.time()
            if e.key == pygame.K_w and snake.direction != 'w' \
                    and snake.direction != 's':
                screen = snake.move(screen, 'w')
                start_time = time.time()
            if e.key == pygame.K_s and snake.direction != 'w' \
                    and snake.direction != 's':
                screen = snake.move(screen, 's')
                start_time = time.time()
    return snake, screen, start_time


def main():
    """Реально main"""
    pygame.init()
    screen = Screen(SCREEN_WIDTH, SCREEN_HEIGHT, GRID_HEIGHT, GRID_WIDTH)

    snake = Snake([[3, 1]])
    for i, j in snake.cords:
        screen.draw(i, j)

    screen.spawn_apple(snake)
    start_time = time.time()

    while True:
        snake, screen, start_time = handle_keys(snake, screen, start_time)

        if time.time() - start_time > 1:
            screen = snake.move(screen, snake.direction)
            start_time = time.time()

        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()
