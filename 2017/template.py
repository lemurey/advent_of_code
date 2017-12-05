from aoc_utilities import get_instructions
import os


def get_answer(data, mode):
    pass


if __name__ == '__main__':
    day = int(os.path.basename(__file__).split('.')[0].split('y')[1])
    inputs = get_instructions(day)
    print(get_answer(inputs, mode='part1'))
    print(get_answer(inputs, mode='part2'))
