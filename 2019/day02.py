from aoc_utilities import get_instructions
import os

class Intcode():
    def __init__(self, program):
        self.program = program
        self.orig = [x for x in self.program]

    def code_01(self, index):
        a = self.program[index + 1]
        b = self.program[index + 2]
        c = self.program[index + 3]
        self.program[c] = self.program[a] + self.program[b]

    def code_02(self, index):
        a = self.program[index + 1]
        b = self.program[index + 2]
        c = self.program[index + 3]
        self.program[c] = self.program[a] * self.program[b]

    def run(self):
        cur_ind = 0
        while True:
            which = self.program[cur_ind]
            if which == 1:
                self.code_01(cur_ind)
            elif which == 2:
                self.code_02(cur_ind)
            elif which == 99:
                return
            else:
                raise ValueError('incorrect value')
            cur_ind += 4

    def reset(self, noun, verb):
        self.program = [x for x in self.orig]
        self.program[1] = noun
        self.program[2] = verb


def parse_inputs(data):
    return list(map(int, data[0].split(',')))


def get_answer(data, part2=False):
    inputs = parse_inputs(data)
    inputs[1] = 12
    inputs[2] = 2
    comp = Intcode(inputs)
    if part2:
        for i in range(100):
            for j in range(100):
                comp.reset(i, j)
                comp.run()
                if comp.program[0] == 19690720:
                    return 100 * i + j
    else:
        comp.run()
        return comp.program[0]


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
