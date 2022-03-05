import urandom


def randxy(size):
    (width, height) = size
    return (urandom.randint(0, width), urandom.randint(0, height))


def randcolor():
    if urandom.random() < 0.75:
        return (urandom.randint(0, 255), urandom.randint(0, 255), urandom.randint(0, 255))
    else:
        return (0, 0, 0)

def randstate(size, colorf=randcolor):
    state = {}
    (max_x, max_y) = size
    for x in range(max_x):
        for y in range(max_y):
            if urandom.random() < 0.25:
                state[(x, y)] = {'color': randcolor()}
    return state

patterns = {
    'block': {
        (7, 2): {'color': (0, 255, 0)},
        (8, 2): {'color': (0, 255, 0)},
        (7, 3): {'color': (0, 255, 0)},
        (8, 3): {'color': (0, 255, 0)}
    },

    'blinker': {
        (7, 3): {'color': (0, 255, 0)},
        (7, 4): {'color': (0, 255, 0)},
        (7, 5): {'color': (0, 255, 0)}
    },

    'glider': {
        (1, 0): {'color': (0, 255, 0)},
        (2, 1): {'color': (0, 255, 0)},
        (0, 2): {'color': (0, 255, 0)},
        (1, 2): {'color': (0, 255, 0)},
        (2, 2): {'color': (0, 255, 0)}
        }
}
