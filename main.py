from picounicorn import PicoUnicorn
from blinkenmachine import VM, Button
from chaos import fsm as chaos
from life import fsm as life
from misc import patterns, randstate

driver = PicoUnicorn()

vm = VM(driver)


def run(inp):
    fsm, state = inp
    vm.running(False)
    vm.clear()
    vm.fsm(fsm)
    vm.state(state)
    vm.running(True)


run((life(driver), patterns['glider']))

