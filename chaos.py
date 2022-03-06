import urandom
from misc import randxy, randcolor

def fsm(driver):
    width =  driver.get_width()
    height = driver.get_height()

    def _fsm(state):
        next = {}
        next[randxy((width, height))] = {'color': randcolor()}
        return next

    return _fsm
