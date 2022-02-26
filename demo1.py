import picounicorn
import urandom
from blinkenmachine import Display

picounicorn.init()

display = Display(picounicorn)

display.blinken()


    def blinken(self, running=True, freq=1000):
        period = int(1000/freq)+1

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