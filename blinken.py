import utime
import urandom
from machine import Timer


class Patterns (dict):
    def __init__(self) -> None:
        super().__init__()
        self.seed = 0.25
        self.update({
            'blinker': set([(5, 3), (6, 3), (7, 3)]),
            'glider': set([(3, 1), (1, 2), (3, 2), (2, 3), (3, 3)])
        })

    def random(self, size):
        (max_x, max_y) = size
        cells = set()
        for x in range(max_x-1):
            for y in range(max_y):
                if urandom.random() < self.seed:
                    cells.add((x, y))
        return cells


class Display:
    def __init__(self, driver) -> None:
        self.board = driver
        self.width = self.board.get_width()
        self.height = self.board.get_height()
        self.timer = Timer()

    def size(self):
        return (self.width, self.height)

    def clear(self):
        for x in range(self.width):
            for y in range(self.height):
                self.board.set_pixel_value(x, y, 0)

    def set(self, cells, color):
        (r, g, b) = color
        for cell in cells:
            (x, y) = cell
            self.board.set_pixel(x % self.width, y % self.height, r, g, b)

    def unset(self, cells):
        for cell in cells:
            (x, y) = cell
            self.board.set_pixel_value(x % self.width, y % self.height, 0)

    def blinken(self, running=True, period=10):
        def light_one_up(timer):
            x = urandom.randint(0, 15)
            y = urandom.randint(0, 6)
            r = urandom.randint(0, 255)
            g = urandom.randint(0, 255)
            b = urandom.randint(0, 255)
            self.board.set_pixel(x, y, r, g, b)

        if running:
            self.timer.init(period=period, mode=Timer.PERIODIC,
                            callback=light_one_up)
        else:
            self.timer.deinit()


class Buttons:
    A = 0
    B = 1
    X = 2
    Y = 3

    def __init__(self, driver, period=10) -> None:
        self.board = driver
        self.timer = Timer()
        self.period = period
        self.callbacks = {}

    def on(self, button, callback):
        self.callbacks[button] = callback

    def enable(self):
        self.timer.init(period=self.period, mode=Timer.PERIODIC,
                        callback=self.dispatch)

    def disable(self):
        self.timer.deinit()

    def dispatch(self, timer):
        for button in self.callbacks:
            if self.board.is_pressed(button):
                while self.board.is_pressed(button):
                    pass
                self.callbacks[button]()


class Rules:
    def __init__(self) -> None:
        pass

    def apply(self, current):
        return current
