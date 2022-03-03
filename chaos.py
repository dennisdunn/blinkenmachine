from blinkenmachine import VM
import picounicorn
import urandom

picounicorn.init()
vm = VM(picounicorn)

size = vm.display.size()

def fsm(state):

    def rcell():
        (width, height) = size
        return (urandom.randint(0, width), urandom.randint(0, height))

    def rcolor():
        if urandom.random() < 0.25:
            return (0,0,0)
        else:
            return (urandom.randint(0, 255), urandom.randint(0, 255), urandom.randint(0, 255))

    next = {}
    next[rcell()] = {'color': rcolor()}
    return next


vm.load(fsm)
vm.register('on_update', lambda vm :vm.display.clear())
vm.run()
