from aoc_utilities import get_instructions
import os
from intcode import Intcode


def to_ascii(string):
        if not string.endswith('\n'):
            string += '\n'
        vals = []
        for char in string:
            vals.append(ord(char))
        return vals


class Droid:
    def __init__(self, program):
        self.core = Intcode(program, mode='ascii robot')

    def run(self):
        while True:
            self.check_output()
            command = input()
            self.core.secondary = to_ascii(command)

    def check_output(self):
        while True:
            self.core.waiting = False
            val = self.core.run()
            if val < 0 or val > 128:
                print(val)
                return
            else:
                print(chr(val), end='')
            if chr(val) in (':', '?'):
                return




def get_answer(data, part2=False):
    program = list(map(int, data[0].split(',')))
    robot = Droid(program)
    robot.run()


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))
