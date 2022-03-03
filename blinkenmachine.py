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

    def __init__(self, driver, eventMgr, period=10) -> None:
        self.events = eventMgr
        self.board = driver
        self.period = period
        self.timer = Timer()

    def enable(self):
        def on_timestep(timer):
            for button in self.events.callbacks:
                if self.board.is_pressed(button):
                    while self.board.is_pressed(button):  # debounce
                        pass
                    self.events.invoke(button)

        self.timer.init(period=self.period,
                        mode=Timer.PERIODIC,
                        callback=on_timestep)

    def disable(self):
        self.timer.deinit()


class CallbackManager:
    def __init__(self, args={}):
        self.callbacks = {}  # keyed lists of functions
        self.callback_args = args

    def invoke(self, event_name):
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


class VM:
    def __init__(self, driver):
        self.display = Display(driver)
        self.events = CallbackManager(self)
        self.buttons = Buttons(driver, self.events)
        self.timer = Timer()
        self.period = 100
        self.state = {}
        self.fsm = None

    def update(self, state={}):
        self.events.invoke('on_update')
        self.state = state

    def load(self, fsm=None):
        self.events.invoke('on_load')
        self.fsm = fsm

    def run(self):
        self.events.invoke('on_run')
        self.buttons.enable()

        def on_timestep(timer):
            if self.fsm != None:
                self.update(self.fsm(self.state))
                self.display.set(self.state)

        self.timer.init(period=self.period,
                        mode=Timer.PERIODIC,
                        callback=on_timestep)

    def halt(self):
        self.call_handler('on_halt')
        self.buttons.disable()
        self.timer.deinit()
