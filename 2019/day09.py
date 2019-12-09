from aoc_utilities import get_instructions
import os
from intcode import Intcode


def get_answer(data, part2=False, mode=None):
    program = [int(x) for x in data[0].split(',')]


    if mode is None:
        if part2:
            comp = Intcode(program, secondary=0, input=2)
        else:
            comp = Intcode(program, secondary=0)
    else:
        if part2:
            comp = Intcode(program, mode=mode, secondary=0, input=2)
        else:
            comp = Intcode(program, mode=mode, secondary=0)
    return comp.run()


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
    # sample = ['109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99']
    # print(get_answer(sample))
    # sample = ['1102,34915192,34915192,7,4,7,99,0']
    # print(get_answer(sample))
    # sample = ['104,1125899906842624,99']
    # print(get_answer(sample))
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))