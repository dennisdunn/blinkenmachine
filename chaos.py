from blinkenmachine import Acam
import picounicorn
import urandom

picounicorn.init()
acam = Acam(picounicorn)

size = acam.display.size()

def fsm(state):

    def rcell():
        (width, height) = size
        return (urandom.randint(0, width), urandom.randint(0, height))

    def rcolor():
        return (urandom.randint(0, 255), urandom.randint(0, 255), urandom.randint(0, 255))

    next = {}
    next[rcell()] = {'color': rcolor()}
    return next


acam.load(fsm)
acam.register('on_update', lambda vm :vm.display.clear())
acam.run()
