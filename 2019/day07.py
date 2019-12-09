from aoc_utilities import get_instructions
import os
from intcode import Intcode
from itertools import cycle, permutations

def parse_inputs(data):
    return list(map(int, data[0].split(',')))


class Runner():
    def __init__(self, sequences, program):
        self.sequences = sequences
        self.program = program
        self.max_output = 0

    def run(self):
        for sequence in self.sequences:
            self.run_one(sequence)
        return self.max_output

    def run_one(self, sequence):
        input_val = 0
        self.final = {'A': False,
                      'B': False,
                      'C': False,
                      'D': False,
                      'E': False}

        comps = []
        for phase, ind in zip(sequence, 'ABCDE'):
            comp = Intcode([x for x in self.program],
                           input=phase,
                           secondary=input_val,
                           mode='linked',
                           parent=self,
                           indicator=ind
                           )
            comps.append(comp)
        comps = cycle(comps)

        while not self.final['E']:
            comp = next(comps)
            comp.secondary = input_val
            comp.waiting = False
            input_val = comp.run()

        if input_val > self.max_output:
            self.max_output = input_val


def get_answer(data, part2=False):
    program = parse_inputs(data)

    sequences = []
    nums = (0, 1, 2, 3, 4)
    if part2:
        nums = (5, 6, 7, 8, 9)

    sequences = list(permutations(nums, 5))

    if part2:
        r = Runner(sequences, program)
        return r.run()

    max_output = 0
    input_val = 0
    for sequence in sequences:
        input_val = 0
        for phase in sequence:
            comp = Intcode([x for x in program], input=phase,
                           secondary=input_val, mode='')
            input_val = comp.run()
        if input_val > max_output:
            max_output = input_val

    return max_output


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
