import urandom

block = {
    (7, 2): {'color': (0, 255, 0)},
    (8, 2): {'color': (0, 255, 0)},
    (7, 3): {'color': (0, 255, 0)},
    (8, 3): {'color': (0, 255, 0)}
}

blinker = {
    (7, 3): {'color': (0, 255, 0)},
    (7, 4): {'color': (0, 255, 0)},
    (7, 5): {'color': (0, 255, 0)}
}

glider = {
    (1, 0): {'color': (0, 255, 0)},
    (2, 1): {'color': (0, 255, 0)},
    (0, 2): {'color': (0, 255, 0)},
    (1, 2): {'color': (0, 255, 0)},
    (2, 2): {'color': (0, 255, 0)}
}

def randomize(size):
    state = {}
    (max_x, max_y) = size
    for x in range(max_x):
        for y in range(max_y):
            if urandom.random() < 0.25:
                state[(x, y)] = {'color': (0, 255, 0)}
    return state


def fsm(state):

    def count_neighbors(state):
        counts = {}
        for cell in state:
            for dx in [-1,  0, 1]:
                for dy in [-1, 0, 1]:
                    (x, y) = cell
                    pos = (x+dx, y+dy)
                    if cell != pos: # don't count yourself as a neighbor
                        if pos in counts:
                            counts[pos] += 1
                        else:
                            counts[pos] = 1
        return counts

    counts = count_neighbors(state)
    
    next = {}
    for cell in counts:
        if cell in state:  # alive
            if counts[cell] == 2 or counts[cell] == 3:
                next[cell] = state[cell]  # stayed alive
            else:
                next[cell] = {'color': (0, 0, 0)}  # died
        else:  # dead
            if counts[cell] == 3:
                next[cell] = {'color': (0, 255, 0)}  # born
                
    return next
