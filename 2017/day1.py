from aoc_utilities import get_instructions
import os


def get_next(index, length, mode):
    if mode == 'part1':
        next_index = (index + 1)
    else:
        next_index = (index + length // 2)
    return next_index % length


def get_answer(data, mode):
    total = 0
    N = len(data)
    for i, digit in enumerate(data):
        next_index = get_next(i, N, mode)
        if digit == data[next_index]:
            total += int(digit)
    return total


if __name__ == '__main__':
    day = int(os.path.basename(__file__).split('.')[0].split('y')[1])
    inputs = get_instructions(day)
    print(get_answer(inputs, mode='part1'))
    print(get_answer(inputs, mode='part2'))
