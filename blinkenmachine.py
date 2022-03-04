from machine import Timer, Pin


class Display:
    def __init__(self, driver) -> None:
        self.height = driver.get_height()
        self.width = driver.get_width()
        self.board = driver

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


class Button():
    A = 0
    B = 1
    X = 2
    Y = 3

    def __init__(self, driver, button_id=0, period=10):
        self.board = driver
        self.id = button_id
        self.period = period
        self.timer = Timer()
        self.callbacks = []

    def enable(self):
        def on_timestep(timer):
            if self.board.is_pressed(self.id):
                while self.board.is_pressed(self.id):  # debounce
                    pass
                for callback in self.callbacks:
                    callback()

        self.timer.init(period=self.period,
                        mode=Timer.PERIODIC,
                        callback=on_timestep)

    def disable(self):
        self.timer.deinit()

    def register(self, callback):
        self.callbacks.append(callback)

    def deregister(self, callback):
        self.callbacks.remove(callback)


class Events:
    def __init__(self):
        self.callbacks = {}  # keyed lists of thunks

    def invoke(self, event_name):
        for callback in self.callbacks.get(event_name, []):
            callback()

    def register(self, event_name, callback):
        handlers = self.callbacks.get(event_name, [])
        handlers.append(callback)
        self.callbacks[event_name] = handlers

    def deregister(self, event_name, callback):
        try:
            handlers = self.callbacks.get(event_name, [])
            handlers.remove(callback)
            self.callbacks[event_name] = handlers
        except:
            pass  # ignore item not in list errors


class VM:
    def __init__(self, driver, period=100):
        self.display = Display(driver)
        self.events = Events()
        self.timer = Timer()
        self.period = period
        self.buttons = {Button.A: Button(driver, Button.A),
                        Button.B: Button(driver, Button.B),
                        Button.X: Button(driver, Button.X),
                        Button.Y: Button(driver, Button.Y)}
        self.state = {}
        self.fsm = None

    def __running_annunciator(self, on):
        Pin(25, Pin.OUT).value(on)

    def __buttons_enable(self, enabled):
        for id in self.buttons:
            if enabled:
                self.buttons[id].enable()
            else:
                self.buttons[id].disable()
                
    def update(self, state={}):
        self.events.invoke('on_update')
        self.state = state

    def load(self, fsm=None):
        self.events.invoke('on_load')
        self.display.clear()
        self.fsm = fsm

    def run(self):
        def on_timestep(timer):
            if self.fsm != None:
                self.update(self.fsm(self.state))
                self.events.invoke('on_display')
                self.display.set(self.state)

        self.events.invoke('on_run')
        self.__buttons_enable(True)
        self.timer.init(period=self.period,
                        mode=Timer.PERIODIC,
                        callback=on_timestep)
        self.__running_annunciator(True)

    def halt(self):
        self.events.invoke('on_halt')
        self.__buttons_enable(False)
        self.timer.deinit()
        self.__running_annunciator(False)
