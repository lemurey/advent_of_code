from aoc_utilities import get_instructions
import os

from intcode import Intcode


class Robot:
    def __init__(self, program, start_val=0):
        self.position = 0
        self.direction = 1j
        self.painted = set()
        self.core = Intcode(program, input=0, mode='robot')
        self.left = 1j
        self.right = -1j
        self.panels = {0: start_val}

    def run(self):
        while not self.core.halted:
            self.step()

    def step(self):
        if self.position not in self.panels:
            self.panels[self.position] = 0
        color = self.panels[self.position]
        if color == 0: # black
            self.core.secondary = 0
        else: # white
            self.core.secondary = 1

        val_1 = self.core.run()
        self.core.waiting = False
        if val_1 == 0:
            self.panels[self.position] = 0
        else:
            self.panels[self.position] = 1

        self.painted.add(self.position)
        val_2 = self.core.run()
        self.core.waiting = False
        if val_2 == 0:
            self.direction *= self.left
            self.position += self.direction
        else:
            self.direction *= self.right
            self.position += self.direction


def show_grid(grid):
    min_y = int(min(grid, key=lambda x: x.imag).imag)
    max_y = int(max(grid, key=lambda x: x.imag).imag)
    min_x = int(min(grid, key=lambda x: x.real).real)
    max_x = int(max(grid, key=lambda x: x.real).real)

    for y in reversed(range(min_y, max_y + 1)):
        row = ''
        for x in range(min_x, max_x + 1):
            position = x + y*1j
            if position in grid:
                val = grid[position]
            else:
                val = 0
            if val == 0:
                row += ' '
            else:
                row += '█'
        print(row)
    return

def get_answer(data, part2=False):
    program = list(map(int, data[0].split(',')))
    if part2:
        robot = Robot([x for x in program], 1)
        robot.run()
        show_grid(robot.panels)
        return
    robot = Robot([x for x in program], 0)
    robot.run()
    return len(robot.painted)


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
