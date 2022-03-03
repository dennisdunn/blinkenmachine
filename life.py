from blinkenmachine import Dacam
import picounicorn
import urandom

picounicorn.init()
vm = VM(picounicorn)


def fsm(state):
    def count_neighbors(state):
        counts = {}
        for cell in state:
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
        else:  # dead
            if counts[cell] == 3:
                next[cell] = {'color': (0, 255, 0)}  # born
    return next


def randomize(self):
    state = {}
    (max_x, max_y) = self.display.size()
    for x in range(max_x):
        for y in range(max_y):
            if urandom.random() < 0.25:
                state[(x, y)] = {'color': (0, 255, 0)} 
    return


def reset(dacam):
    print('halted...')
    dacam.randomize(lambda: {'color': (0, 255, 0)})
    dacam.run()
    
vm.load(fsm)
vm.run()
