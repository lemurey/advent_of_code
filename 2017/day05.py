from aoc_utilities import get_instructions
from utilities import timeit
import os


def parse_instructions(data):
    output = {}
    for i, line in enumerate(data.split()):
        output[i] = int(line)
    return output


def get_offset(part2, jump):
    if part2 and jump > 2:
        return -1
    else:
        return 1


@timeit
def get_answer(data, part2=False):
    instructions = parse_instructions(data)
    index = 0
    steps = 0
    while index in instructions:
        steps += 1
        jump = instructions[index]
        offset = get_offset(part2, jump)
        instructions[index] += offset
        index += jump
    return steps


if __name__ == '__main__':
    day = int(os.path.basename(__file__).split('.')[0].split('y')[1])
    inputs = get_instructions(day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
