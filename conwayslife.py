import urandom
from blinkenmachine import Rules

class Patterns (dict):
    probablility = 0.25
    blinker = set([(5, 3), (6, 3), (7, 3)])
    glider = set([(3, 1), (1, 2), (3, 2), (2, 3), (3, 3)])

    @classmethod
    def random(self, size):
        (max_x, max_y) = size
        cells = set()
        for x in range(max_x-1):
            for y in range(max_y):
                if urandom.random() < Patterns.probablility:
                    cells.add((x, y))
        return cells

class ConwaysLife(Rules):
    def __init__(self) -> None:
        super().__init__()

    def apply(self, current):
        next = set()
        counts = self.count_neighbors(current)
        for cell in counts:
            if cell in current:  # alive
                if counts[cell] == 2 | counts[cell] == 3:
                    next.add(cell)
            else:  # dead
                if counts[cell] == 3:
                    next.add(cell)
        return next

    def count_neighbors(self, current):
        counts = {}
        for cell in current:
            for dx in [-1,  0, 1]:
                for dy in [-1, 0, 1]:
                    (x, y) = cell
                    pos = (x-dx, y-dy)
                    if pos in counts:
                        counts[pos] += 1
                    else:
                        counts[pos] = 1
        return counts
