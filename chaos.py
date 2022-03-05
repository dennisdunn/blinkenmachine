import urandom

def init(driver):
    width =  driver.get_width()
    height = driver.get_height()

    def fsm(state):
        
        def rcell():
            return (urandom.randint(0, width), urandom.randint(0, height))

        def rcolor():
            if urandom.random() < 0.75:
                return (urandom.randint(0, 255), urandom.randint(0, 255), urandom.randint(0, 255))
            else:
                return (0, 0, 0)

        next = {}
        next[rcell()] = {'color': rcolor()}
        return next

    return fsm
