from aoc_utilities import get_instructions


def get_next(index, length, mode):
    if mode == 'part1':
        next_index = (index + 1)
    else:
        next_index = (index + length // 2)
    return next_index % length


def compute_sum(data, mode):
    total = 0
    N = len(data)
    for i, digit in enumerate(data):
        next_index = get_next(i, N, mode)
        if digit == data[next_index]:
            total += int(digit)
    return total


if __name__ == '__main__':
    inputs = get_instructions(1)
    print(compute_sum(inputs, mode='part1'))
    print(compute_sum(inputs, mode='part2'))
