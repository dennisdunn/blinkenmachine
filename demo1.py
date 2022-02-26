import urandom
import picounicorn
from machine import Timer
from blinkenmachine import Display

picounicorn.init()

display = Display(picounicorn)

def rcell(size):
    (width, height) = size
    return (urandom.randint(0, width), urandom.randint(0, height))


def rcolor():
    return (urandom.randint(0, 255), urandom.randint(0, 255), urandom.randint(0, 255))

timer = Timer()
timer.init(period=10,
           mode=Timer.PERIODIC,
           callback=lambda timer: display.set_pixel(rcell(display.size()), rcolor()))
