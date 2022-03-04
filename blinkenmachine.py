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


class Buttons:
    A = 0
    B = 1
    X = 2
    Y = 3

    def __init__(self, driver, callbacks, period=10) -> None:
        self.events = callbacks
        self.period = period
        self.board = driver
        self.timer = Timer()
        
    def on(self, button, callback):
        self.events.register(button, callback)
        
    def off(self, button, callback):
        self.events.deregister(button, callback)

    def enable(self):
        def on_timestep(timer):
            for button in self.events.callbacks:
                if self.board.is_pressed(button):
                    while self.board.is_pressed(button):  # debounce
                        pass
                    self.events.invoke(button)

        self.events.enable()
        self.timer.init(period=self.period,
                        mode=Timer.PERIODIC,
                        callback=on_timestep)

    def disable(self):
        self.events.disable()
        self.timer.deinit()


class Events:
    def __init__(self, args={}):
        self.callbacks = {}  # keyed lists of functions
        self.callback_args = args
        self.enabled = False

    def invoke(self, event_name):
        if self.enabled:
            for callback in self.callbacks.get(event_name, []):
                callback(self.callback_args)

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

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False


class VM:
    def __init__(self, driver):
        self.buttons = Buttons(driver, Events(self))
        self.display = Display(driver)
        self.events = Events(self)
        self.timer = Timer()
        self.period = 100
        self.state = {}
        self.fsm = None

    def __running_annunciator(self, on):        
        Pin(25, Pin.OUT).value(on)
        
    def update(self, state={}):
        self.events.invoke('on_update')
        self.state = state

    def load(self, fsm=None):
        self.events.invoke('on_load')
        self.display.clear()
        self.fsm = fsm

    def run(self):
        self.events.invoke('on_run')
        self.__running_annunciator(True)
        self.buttons.enable()
        self.events.enable()

        def on_timestep(timer):
            if self.fsm != None:
                self.update(self.fsm(self.state))
                self.events.invoke('on_display')
                self.display.set(self.state)

        self.timer.init(period=self.period,
                        mode=Timer.PERIODIC,
                        callback=on_timestep)

    def halt(self):
        self.events.invoke('on_halt')
        self.__running_annunciator(False)
        self.buttons.disable()
        self.events.disable()
        self.timer.deinit()
