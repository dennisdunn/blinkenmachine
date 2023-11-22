
def fsm(driver):
    width =  driver.get_width()
    height = driver.get_height()
    
    def _count_neighbors(state):
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

    def _fsm(state):
        counts = _count_neighbors(state)
        
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
    
    return _fsm
