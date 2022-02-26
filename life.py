
def fsm(cells):
    def count_neighbors(cells):
        counts = {}
        for cell in cells:
            for dx in [-1,  0, 1]:
                for dy in [-1, 0, 1]:
                    (x, y) = cell
                    pos = (x-dx, y-dy)
                    if pos in counts:
                        counts[pos] += 1
                    else:
                        counts[pos] = 1
        return counts

    next = set()
    counts = count_neighbors(cells)
    for cell in counts:
        if cell in cells:  # alive
            if counts[cell] == 2 | counts[cell] == 3:
                next.add(cell) # stayed alive
        else:  # dead
            if counts[cell] == 3:
                next.add(cell) # born
    return next
