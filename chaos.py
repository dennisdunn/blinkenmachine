import urandom
from misc import randxy, randcolor

def init(driver):
    width =  driver.get_width()
    height = driver.get_height()

    def fsm(state):
        next = {}
        next[randxy((width, height))] = {'color': randcolor()}
        return next

    return fsm
