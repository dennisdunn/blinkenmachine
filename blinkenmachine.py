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


class Events:
    def __init__(self):
        self.__callbacks = {}  # keyed lists of thunks

    def invoke(self, event_name):
        for callback in self.__callbacks.get(event_name, []):
            callback()

    def register(self, event_name, callback):
        handlers = self.__callbacks.get(event_name, [])
        handlers.append(callback)
        self.__callbacks[event_name] = handlers

    def deregister(self, event_name, callback):
        try:
            handlers = self.__callbacks.get(event_name, [])
            handlers.remove(callback)
            self.__callbacks[event_name] = handlers
        except:
            pass  # ignore item not in list errors


class Button:
    A = 0
    B = 1
    X = 2
    Y = 3


class Buttons(Events):
    def __init__(self, driver, period=10):
        super().__init__()
        self.board = driver
        self.period = period
        self.timer = Timer()
        self.__enabled = False

    def __button_name(self, button):
        return 'button_' + str(button)

    def __tick(self, timer):
        try:
            for n in range(4):
                if self.board.is_pressed(n):
                    while self.board.is_pressed(n):  # debounce
                        pass
                    super().invoke(self.__button_name(n))
        except:
            self.enabled(False)
            raise

    def enabled(self, enabled=None):
        if enabled == None:
            return self.__enabled
        else:
            self.__enabled = enabled
            if self.__enabled:
                self.timer.init(period=self.period,
                                mode=Timer.PERIODIC,
                                callback=self.__tick)
            else:
                self.timer.deinit()

    def on(self, button, callback):
        super().register(self.__button_name(button), callback)


class VM:
    def __init__(self, driver, period=100):
        self.__display = Display(driver)
        self.__buttons = Buttons(driver)
        self.__events = Events()
        self.__running = False
        self.__timer = Timer()
        self.__period = period
        self.__state = {}
        self.__fsm = None

    def __running_annunciator(self, on):
        Pin(25, Pin.OUT).value(on)

    def __update_display(self, state):
        for (xy, props) in state.items():
            self.__display.set_pixel(xy, props['color'])

    def __cell_is_empty(self, cell):
        return cell[1].get('color', (0, 0, 0)) == (0, 0, 0)

    def __tick(self, timer):
        try:
            state = self.__fsm(self.__state)
            self.__update_display(state)
            self.__state = dict(
                filter(lambda cell: not self.__cell_is_empty(cell), state.items()))
            self.__events.invoke('on_tick')
        except:
            self.enabled(False)
            raise

    def state(self, state=None):
        if state == None:
            return self.__state
        else:
            self.__events.invoke('on_update')
            self.__state = state
        
    def fsm(self, fsm=None):
        if fsm == None:
            return self.__fsm
        else:
            self.__events.invoke('on_load')
            self.__fsm = fsm

    def running(self, running=None):
        if running == None:
            return self.__running
        else:
            self.__running = running
            self.__buttons.enabled(running)
            self.__running_annunciator(running)
            if self.__running:
                self.__events.invoke('on_run')
                self.__timer.init(period=self.__period,
                                mode=Timer.PERIODIC,
                                callback=self.__tick)
            else:
                self.__events.invoke('on_halt')
                self.__timer.deinit()

    def on(self, button, callback):
        self.__buttons.on(button, callback)
        
    def clear(self):
        self.__display.clear()
