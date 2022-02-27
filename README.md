Das Blinken Machine
===

> ### ***Achtung!***
> Alle touristen und non-technischen lookenpeepers! 
>
> Das machine is nicht fur fingerpoken und mittengrabben. Is easy schnappen der springenwerk, blowenfusen und poppencorken mit spitzen sparken. 
>
> Das machine is diggen by experten only. Is nicht fur gerwerken by das dummkopfen. Das rubbernecken sightseeren keepen das cottenpicken hands in das pockets. 
>
> Relaxen und watchen das blinkenlights.
>
> [Wikipedia](https://en.wikipedia.org/wiki/Blinkenlights)

The Blinken Machine is an environment consisting of a Raspberry Pi Pico mated with the Pimoroni Pico Unicorn built for playing with cellular automata. The ```VM``` continuously executes a finite state machine and passes the current state to a callback which can then update a ```Display``` instance. An instance of the ```Buttons``` class registers callbacks for the ***A***, ***B***, ***X***, and ***Y*** buttons of the Unicorn board. 

### Examples

* *demo1.py* 
    * Lights random pixels on the display.
* *demo2.py*
    * Implements *Conway's Game of Life*. The **A** button restarts the ```VM```
    with a new initial pattern.

Here's a simple demo that illustrates setting up the ```VM```.

```
from blinkenmachine import VM

vm = VM(print)
vm.start(0, lambda x: x + 1)
```

blinkenmachine Module
---

### Display

The *Display* class controls access to the LEDs on the Pico Unicorn board. A *cell* is
an ```(x, y)``` tuple while a *color* is an ```(r, g, b)``` tuple.

#### Methods

* ```Display(driver)```
    * The *driver*  argument is the object returned by ```import picounicorn```.
* ```size()```
    * Returns the size of the LED grid as a ```(width, height)``` tuple.
* ```clear()```
    * Sets all of the pixels to black.
* ```set_pixel(cell, color)```
    * Set the *cell* to the specified *color*.
* ```set(cells, color)```
    * Given the iterable of *cells*, set them to the provided *color*.
* ```unset(cells)```
    * Set each cell of *cells* to black.

### Buttons

Provides a callback mechanism for button presses on the Pimoroni Pico Unicorn board. Button presses are debounced before invoking the callback. The buttons are named **Buttons.A**, **Buttons.B**, **Buttons.X**, **Buttons.Y**.

#### Methods

* ```Buttons(driver, freq)```
    * The *driver* argument is the picounicorn module and *freq* is the polling frequency.
* ```register(button, callback)```
    * Register a *callback* for the given *button*.  You can register multiple callbacks for a single button.
* ```deregister(button, callback)```
    * Unregister the *callback* for the *button*. 
* ```enable()```
    * Start polling the buttons on the Unicorn board.
* ```disable()```
    * Stop polling the buttons.

### VM

The **Blinken Machine** ```VM``` continuously applies a function to state. The function implements a finite-state-machine and at each timestep takes the current state of the FSM and returns a 
```(previous_state, next_state)``` tuple.

#### Methods

* ```VM(callback, freq)```
    * Call the *callback* function *freq* times per second with the result of the FSM state changes.
* ```start(initial_state, fsm)```
    * Start executing the *fsm* finite-state-machine with the given *initial_state*.
* ```halt()```
    * Stop exeution.

### Next Steps

The ultimate goal is to have a DSL for defining the FSM of the cellular automaton. 
A parser and compiler turn the DSL into code for the VM to execute, possibly by transpiling
to python.