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

The **Blinken Machine** is a petri dish for playing with cellular automata. 

#### Examples
```
import picounicorn as driver
from blinkenmachine import VM, Button
import chaos

driver.init()
vm = VM(driver)
vm.on(Button.A, vm.clear)
vm.fsm(chaos.init(driver))
vm.running(True)
```

```
import picounicorn as driver
from blinkenmachine import VM
from misc import patterns
from life import fsm

driver.init()
vm = VM(driver)
vm.fsm(fsm)
vm.state(patterns['glider'])
vm.running(True)
```

### Display

The *Display* class controls access to the LEDs on the Pico Unicorn pack. A *cell* is
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

### Events

An *Events* instance handles registering, deregistering, and invoking callbacks for named events. Callbacks are thunks so you'll want to close over any references.

#### Methods

* ```Events()```
* ```invoke(event_name)```
    * Call the registerd callbacks for *event_name*.
* ```register(event_name, thunk)```
    * Add the *thunk* to the list of callbacks for *event_name*.
* ```deregister(event_name, thunk)```
    * Remove the *thunk* for *event_name*.

### Button

Provides names for the 4 buttons on the Pimoroni Pico Unicorn pack.

* ```Button.A```
* ```Button.B```
* ```Button.X```
* ```Button.Y```


### Buttons

Provides a callback mechanism for button presses on the Pimoroni Pico Unicorn pack. Button presses are debounced before invoking the callback.

#### Methods

* ```Buttons(driver, period=10)```
    * The *driver* argument is the picounicorn module, *period* is the polling delay.
* ```enabled(enabled=None)```
    * Start polling the buttons on the Unicorn board if *enabled* otherwise stop polling.
* ```on(button, thunk)```
    * Register the *thunk* as the callback for the *button*.

#### Example
```
from blinkenmachine import Button, Buttons
import picounicorn as driver

driver.init()
buttons = Buttons(driver)
buttons.on(Button.A, lambda: print('button A pressed...'))
buttons.enabled(True)
```

### VM

The **Blinken Machine** *VM* continuously applies a finite state machine to a state object. At each timestep the new state is calculated by applying the FSM function to the current state, the new state
is displayed, and finally the current state is updated to the new state minus any dead cells.

The *state* argument passed to the FSM function is a sparse matrix implemented as a dictionary whose keys are *(x, y)* tuples and whose values are dictionarys. A cell is **alive** if it is a member of the state and its ```color``` property is something other than ```(0, 0, 0)```. In following example, cells ```(1,1)``` and ```(2,3)``` are **alive** while all other cells are **dead**.
```
state = {(1,1):{'color':(255, 0, 0)}, (5,5):{'color':(0, 0, 0)}, (2,3):{'color':(255, 255, 0)}}
```

#### Events

Event handlers can be registered for:
* ```on_load```
    * Invoked when setting the FSM function.
* ```on_tick```
    * Invoked on each generation.
* ```on_update```
    * Invoked when setting the state to a new value.
* ```on_run```
    * Invoked when setting the *running* flag.
* ```on_halt```
    * Invoked when clearing the *running* flag.

#### Methods

* ```VM(driver)```
    * Initialize a VM with the picounicorn *driver*.
* ```fsm(fsm=None)```
    * Set the VM fsm to the provided *fsm* method.
* ```state(state=None)```
    * Set the VM state to the provided *state* object.
* ```running(running=None)```
    * If *running* is True then start exeution, otherwise halt.
* ```on(button, thunk)```
    * Register the *thunk* as the callback for *button*.
* ```clear()```
    * Clear the LED matrix.

### Next Steps

* Add support for 1-dimensional cellular automata. Each time the bottom row is recalculated, 
all of the rows move up one row.
* Add a *WA-TOR* demo. Each cell in *Conway's Life* is very simple, it is either **dead** or **alive**. A cell in *WA-TOR* has three states, **fish**, **shark**, or **empty** but 
then it also has properties like **age** and **hunger**.
* Add a DSL for describing a cellular atomaton and a parser for that language.
