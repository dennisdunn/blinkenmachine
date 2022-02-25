import picounicorn
from blinkenmachine import VM, Display, Buttons
from conwayslife import ConwaysLife, Patterns

picounicorn.init()

display = Display(picounicorn)
buttons = Buttons(picounicorn)

def update(current):
    display.clear()
    display.set(current, (0, 255, 0))

vm = VM(update)

def reset():
    print('starting...')
    vm.halt()
    vm.start(Patterns.random(), ConwaysLife())

buttons.on(Buttons.A, reset)
buttons.enable()
