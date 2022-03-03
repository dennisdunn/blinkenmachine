from machine import Timer
import urandom

# state is a dict of cells
# the key is the xy of the cell
# the value is a dict of properties

# a cell is a tuple of (xy, properties) ie: a dict item

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

    def set_pixel(self, xy, color):
        (x, y) = xy
        (r, g, b) = color
        self.board.set_pixel(x % self.width, y %
                             self.height, r, g, b)  # toroidal display

    def set(self, state):
        for cell in state.items():
            (xy, props) = cell
            self.set_pixel(xy, props['color'])

    def unset(self, state):
        for xy in state:
            self.set_pixel(xy, (0, 0, 0))


class Buttons:
    A = 0
    B = 1
    X = 2
    Y = 3

    def __init__(self, driver, period=10) -> None:
        self.board = driver
        self.period = period
        self.timer = Timer()
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
    def __init__(self, driver):
        self.display = Display(driver)
        self.buttons = Buttons(driver)
        self.timer = Timer()
        self.period = 100
        self.state = {}
        self.fsm = None
        self.handlers = {}  # keyed lists of functions

    def update(self, state={}):
        self.call_handler('on_update')
        self.state = state

    def load(self, fsm=None):
        self.call_handler('on_load')
        self.fsm = fsm

    def run(self):
        self.call_handler('on_run')

        def on_timestep(timer):
            if self.fsm != None:
                next = self.fsm(self.state)
                self.update(next)
                self.display.set(self.state)

        self.timer.init(period=self.period,
                        mode=Timer.PERIODIC,
                        callback=on_timestep)

    def halt(self):
        self.call_handler('on_halt')
        self.timer.deinit()

    def call_handler(self, event_name):
        for fn in self.handlers.get(event_name, []):
            fn(self)

    def register(self, event_name, fn):
        handlers = self.handlers.get(event_name, [])
        handlers.append(fn)
        self.handlers[event_name] = handlers

    def deregister(self, event_name, fn):
        try:
            handlers = self.handlers.get(event_name, [])
            handlers.remove(fn)
            self.handlers[event_name] = handlers
        except:
            pass  # ignore item not in list errors
