from aoc_utilities import get_instructions
from utilities import timeit
import os


def parse_instructions(data):
    output = {}
    for i, line in enumerate(data.split()):
        output[i] = int(line)
    return output


@timeit
def get_answer(data, mode):
    instructions = parse_instructions(data)
    index = 0
    steps = 0
    while index in instructions:
        steps += 1
        jump = instructions[index]
        offset = 1
        if mode != 'part1' and jump >= 3:
            offset = -1
        instructions[index] += offset
        index += jump
    return steps


if __name__ == '__main__':
    day = int(os.path.basename(__file__).split('.')[0].split('y')[1])
    inputs = get_instructions(day)
    print(get_answer(inputs, mode='part1'))
    print(get_answer(inputs, mode='part2'))
