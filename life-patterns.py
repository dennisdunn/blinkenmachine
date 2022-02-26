
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