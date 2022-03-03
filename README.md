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

The **Blinken Machine** is a computing device for playing with cellular automata. This tiny computer
is built with a Raspberry Pi Pico mated with the Pimoroni Pico Unicorn Pack. It runs
MicroPython as its "BIOS" and an instance of the ```VM``` class as its "operating system."
Input is through the ```Buttons``` class and output is handled by the ```Display``` class.

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

### Events

An *Events* instance handles registering, deregistering, and invoking callbacks for named events.

#### Methods

* ```Events(args)```
    * The *args* argument will be passed to the registered callbacks.
* ```invoke(event_name)```
    * Call the registerd callbacks for *event_name*.
* ```register(event_name, callback)```
    * Add the *callback* to the list of methods for *event_name*.
* ```deregister(event_name, callback)```
    * Remove the *callback* for *event_name*.

### Buttons

Provides a callback mechanism for button presses on the Pimoroni Pico Unicorn board. Button presses are debounced before invoking the callback. The buttons are named **Buttons.A**, **Buttons.B**, **Buttons.X**, **Buttons.Y**.

#### Methods

* ```Buttons(driver, events, period)```
    * The *driver* argument is the picounicorn module, *events* is an instance of an **Events**, and *period* is the polling delay.
* ```enable()```
    * Start polling the buttons on the Unicorn board.
* ```disable()```
    * Stop polling the buttons.

### VM

The **Blinken Machine** *VM* continuously applies a finite state machine to a state object. At each timestep the new state is calcualted by applying the FSM function to the current state, the new state is
displayed, and finally the current state is updated to the new state.

Event handlers can be registered for the **on_load**, **on_update**, **on_run**, and **on_halt**
events.

#### Methods

* ```VM(driver)```
    * Initialize a VM with the picounicorn *driver*.
* ```load(fsm)```
    * Set the VM fsm to the provided *fsm* method.
* ```update(state)```
    * Set the VM state to the provided *state* object.
* ```run()```
    * Start exeution.
* ```halt()```
    * Halt exeution.

### Next Steps

* Add support for 1-dimensional cellular automata. Each time the bottom row is recalculated, 
all of the rows move up one row.
* Add a *WA-TOR* demo. Each cell in *Conway's Life* is very simple, it is either **dead**, **alive** or 
**empty**. A cell in *WA-TOR* has three states as well, **fish**, **shark**, or **empty** but 
then it also has properties like **age** and **hunger**.
* Add a DSL for describing a cellular atomaton and a parser for that language.
