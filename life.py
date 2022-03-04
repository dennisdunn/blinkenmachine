from blinkenmachine import VM
import picounicorn
import urandom

picounicorn.init()
vm = VM(picounicorn)


def fsm(state):

    def count_neighbors(state):
        counts = {}
        for cell in state:
            if state[cell]['alive']:  # only update neighbors of alive cells
                for dx in [-1,  0, 1]:
                    for dy in [-1, 0, 1]:
                        (x, y) = cell
                        pos = (x+dx, y+dy)
                        if pos != cell:
                            if pos in counts:
                                counts[pos] += 1
                            else:
                                counts[pos] = 1
        return counts

    next = {}
    counts = count_neighbors(state)
    for cell in counts:
        if cell in state:  # alive
            if counts[cell] == 2 | counts[cell] == 3:
                next[cell] = state[cell]  # stayed alive
            else:
                next[cell] = {'color': (0, 0, 0), 'alive': False}  # died
        else:  # dead
            if counts[cell] == 3:
                next[cell] = {'color': (0, 255, 0), 'alive': True}  # born
    return next


def randomize(size):
    state = {}
    (max_x, max_y) = size
    for x in range(max_x):
        for y in range(max_y):
            if urandom.random() < 0.25:
                state[(x, y)] = {'color': (0, 255, 0), 'alive': True}
    return state


def refresh(vm):
    if len(vm.state)==0:
        vm.display.clear()
        vm.events.disable()
        vm.update(randomize(vm.display.size()))
        vm.display.set(vm.state)
        vm.events.enable()
        
    
vm.load(fsm)
refresh(vm)

vm.events.register('on_update', refresh)
vm.run()
