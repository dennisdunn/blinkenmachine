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

#### Example
```
import picounicorn as driver
from blinkenmachine import VM, Button
import chaos

driver.init()
vm = VM(driver)
vm.buttons[Button.A].register(lambda:vm.display.clear())
vm.load(chaos.init(driver))
vm.run()
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

Provides a callback mechanism for button presses on the Pimoroni Pico Unicorn pack. Button presses are debounced before invoking the callback.

#### Methods

* ```Button(driver, id, period=10)```
    * The *driver* argument is the picounicorn module, *id* is one of **Button.A**, **Button.B**, **Button.X**, **Button.Y**, and *period* is the polling delay.
* ```enable()```
    * Start polling the buttons on the Unicorn board.
* ```disable()```
    * Stop polling the buttons.
* ```register(thunk)```
    * Register the thunk as the callback for the button.
* ```deregister(thunk)```
    * Deregister the given thunk.

#### Example
```
from blinkenmachine import Button
import picounicorn as driver

driver.init()
btn_a = Button(driver, Button.A)
btn_a.register(lambda: print('button A pressed...'))
btn_a.enable()
```

### VM

The **Blinken Machine** *VM* continuously applies a finite state machine to a state object. At each timestep the new state is calcualted by applying the FSM function to the current state, the current state is updated to the new state, and finally the new state is displayed.

The *state* argument passed to the FSM function is a dictionary whose keys are *(x, y)* tuples and whose
values are dictionarys.

```
state = {(1,1):{'color':(255, 0, 0)}, (2,3):{'color':(255, 255, 0)}}
```

Event handlers can be registered for the **on_load**, **on_update**, **on_run**, and **on_halt** events.

#### Methods

* ```VM(driver)```
    * Initialize a VM with the picounicorn *driver*.
* ```load(fsm)```
    * Set the VM fsm to the provided *fsm* method.
* ```set(state)```
    * Set the VM state to the provided *state* object.
* ```run()```
    * Start exeution.
* ```halt()```
    * Halt exeution.

### Next Steps

* Add support for 1-dimensional cellular automata. Each time the bottom row is recalculated, 
all of the rows move up one row.
* Add a *WA-TOR* demo. Each cell in *Conway's Life* is very simple, it is either **dead** or **alive**. A cell in *WA-TOR* has three states, **fish**, **shark**, or **empty** but 
then it also has properties like **age** and **hunger**.
* Add a DSL for describing a cellular atomaton and a parser for that language.
