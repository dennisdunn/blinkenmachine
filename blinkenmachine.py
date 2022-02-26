from machine import Timer


class Display:
    def __init__(self, driver) -> None:
        self.board = driver
        self.width = self.board.get_width()
        self.height = self.board.get_height()

    def size(self):
        return (self.width, self.height)

    def clear(self):
        for x in range(self.width):
            for y in range(self.height):
                self.board.set_pixel_value(x, y, 0)

    def set_pixel(self, cell, color):
        (x, y) = cell
        (r, g, b) = color
        self.board.set_pixel(x % self.width, y % self.height, r, g, b)

    def set(self, cells, color):
        for cell in cells:
            self.set_pixel(cell, color)

    def unset(self, cells):
        for cell in cells:
            (x, y) = cell
            self.board.set_pixel_value(x % self.width, y % self.height, 0)


class Buttons:
    A = 0
    B = 1
    X = 2
    Y = 3

    def __init__(self, driver, freq=10) -> None:
        self.board = driver
        self.timer = Timer()
        self.period = int(1000/freq)+1
        self.callbacks = {Buttons.A: set(),
                          Buttons.B: set(),
                          Buttons.X: set(),
                          Buttons.Y: set()}

    def register(self, button, callback):
        self.callbacks[button].add(callback)

    def deregister(self, button, callback):
        try:
            self.callbacks[button].remove(callback)
        except:
            pass

    def enable(self):
        def on_timestep(timer):
            for button in self.callbacks:
                if self.board.is_pressed(button):
                    while self.board.is_pressed(button):  # debounce
                        pass
                    for callback in self.callbacks[button]:
                        callback()

        self.timer.init(period=self.period,
                        mode=Timer.PERIODIC,
                        callback=on_timestep)

    def disable(self):
        self.timer.deinit()


class VM:
    def __init__(self, callback, freq=10) -> None:
        self.timer = Timer()
        self.period = int(1000/freq)+1
        self.callback = callback

    def start(self, initial_state, fsm):
        current = initial_state

        def on_timestep(timer):
            next = fsm(current)
            self.callback(current, next)
            current = next

        self.timer.init(period=self.period,
                        mode=Timer.PERIODIC,
                        callback=on_timestep)

    def halt(self):
        self.timer.deinit()
