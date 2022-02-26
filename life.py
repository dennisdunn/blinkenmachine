import picounicorn

from blinkenmachine import Display, Buttons, VM
from conwayslife import Patterns, ConwaysLife as rules

picounicorn.init()

disp = Display(picounicorn)


def update(current):
    disp.clear()
    disp.set(current, (0, 255, 0))


vm = VM(update)


b = Buttons(picounicorn)
b.register(Buttons.A, lambda: vm.start(Patterns.blinker, rules()))
b.register(Buttons.B, vm.halt)
b.enable()
