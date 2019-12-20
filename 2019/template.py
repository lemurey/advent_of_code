from aoc_utilities import get_instructions
import os


def get_answer(data, part2=False):
    pass


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))
