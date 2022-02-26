import urandom
import picounicorn
from life import fsm
from blinkenmachine import VM, Display, Buttons

picounicorn.init()

display = Display(picounicorn)
buttons = Buttons(picounicorn)


def update(state):
    (previous, current) = state
    display.unset(previous - current)
    display.set(current - previous, (0, 255, 0))

vm = VM(update)

def rpattern(size):
    (max_x, max_y) = size
    cells = set()
    for x in range(max_x-1):
        for y in range(max_y-1):
            if urandom.random() < 0.25:
                cells.add((x, y))
    return cells

def reset():
    display.clear()
    vm.halt()
    vm.start(rpattern(display.size()), fsm)

buttons.register(Buttons.A, reset)
buttons.enable()

reset()
