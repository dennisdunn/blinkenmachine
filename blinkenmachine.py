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

        if len(self.callbacks) > 0:
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
                
    def __update_display(self, state):
        for (xy, props) in state.items():
            self.display.set_pixel(xy, props['color'])
            
    def __cell_is_empty(self, cell):
        return cell[1].get('color', (0,0,0)) == (0,0,0)
    
    def set(self, state):
        self.state = state

    def load(self, fsm):
        self.events.invoke('on_load')
        self.fsm = fsm

    def run(self):
        def update(timer):
            try:
                state = self.fsm(self.state)
                self.__update_display(state)
                self.state = dict(filter(lambda  cell: not self.__cell_is_empty(cell), state.items()))
                self.events.invoke('on_update')
            except:
                self.halt()
                raise
            
        self.__buttons_enable(True)
        self.__running_annunciator(True)
        self.events.invoke('on_run')
        self.timer.init(period=self.period,
                        mode=Timer.PERIODIC,
                        callback=update)

    def halt(self):
        self.__buttons_enable(False)
        self.__running_annunciator(False)
        self.events.invoke('on_halt')
        self.timer.deinit()
