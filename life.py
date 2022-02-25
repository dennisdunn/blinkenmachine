import picounicorn
import utime
import urandom
from machine import Timer
# from blinken import PatternLib

from blinken import Display, Buttons,Rules

picounicorn.init()


# class VM:
#     def __init__(self, display, buttons) -> None:
#         self.disp = display
#         self.inputs = buttons
#         self.running = False
#         self.timestep = 0.1

#     def start(self, current, rules):
#         self.running = True
#         while self.running:
#             # self.inputs.dispatch(self)
#             next = rules.apply(current)
#             disp.clear(current - next)
#             disp.set(next, (0, 255, 0))
#             # print('current=',current)
#             # print('next=',next)
#             current = next
#             utime.sleep(self.timestep)

#     def halt(self):
#         self.running = False

#     def pause(self):
#         self.running = not self.running



# class ConwaysLife(blinken.Rules):
#     def __init__(self) -> None:
#         super().__init__()

#     def apply(self, current):
#         next = set()
#         counts = self.count_neighbors(current)
#         for cell in counts:
#             if cell in current:  # alive
#                 if counts[cell] == 2 | counts[cell] == 3:
#                     next.add(cell)
#             else:  # dead
#                 if counts[cell] == 3:
#                     next.add(cell)
#         return next

#     def count_neighbors(self, current):
#         counts = {}
#         for cell in current:
#             for dx in [-1,  0, 1]:
#                 for dy in [-1, 0, 1]:
#                     (x, y) = cell
#                     pos = (x-dx, y-dy)
#                     if pos in counts:
#                         counts[pos] += 1
#                     else:
#                         counts[pos] = 1
#         return counts


# lib = PatternLib()

disp = Display(picounicorn)

b = Buttons(picounicorn)
b.on(Buttons.A, lambda:disp.blinken())
b.on(Buttons.B, lambda :disp.blinken(False))
b.on(Buttons.Y,lambda: disp.clear())
b.enable()
while True:
    pass

# vm = VM(disp, buttons)

# vm.start(lib['blinker'], ConwaysLife())
