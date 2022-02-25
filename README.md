Das Blinken Machine
===

> ### ***Achtung!***
> Alle touristen und non-technischen 
lookenpeepers! 
> Das machine is nicht fur fingerpoken und mittengrabben. Is easy schnappen der springenwerk, blowenfusen und poppencorken mit spitzen sparken. 
> Das machine is diggen by experten only. Is nicht fur gerwerken by das dummkopfen. Das rubbernecken sightseeren keepen das cottenpicken hands in das pockets. 
> Relaxen und watchen das blinkenlights.

The Blinken Machine is a VM that runs on a Raspberry Pi Pico mated with the Pimoroni Pico Unicorn. The VM continuously executes a finite state machine and updates the display with the current state of the FSM.

### Conways Game of Life
```
import picounicorn
from blinkenmachine import VM, Display, Patterns
from conwayslife import ConwaysLife

picounicorn.init()

display = Display(picounicorn)
vm = VM()
vm.start(ConwaysLife(), Patterns.blinker)
```

### Other Fun Stuff
```
import picounicorn
from blinkenmachine import Display

picounicorn.init()

display = Display(picounicorn)
display.blinken(picounicorn)
```

```
import picounicorn
from blinkenmachine import VM, Display, Patterns, Buttons
from conwayslife import ConwaysLife

picounicorn.init()

vm = VM()
display = Display(picounicorn)
buttons = Buttons(picounicorn)

def reset():
    vm.halt()
    vm.start(ConwaysLife(), Patterns.random())

buttons.on(Buttons.A, reset)
```