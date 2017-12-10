from aoc_utilities import get_instructions
from functools import reduce
from utilities import timeit
import os


def reverse(array, length, position):
    if position + length >= len(array):
        new_vals = array[position:]
        new_vals += array[:(position + length) % 256]
    else:
        new_vals = array[position:(position + length)]

    new_vals = new_vals[::-1]

    for index in range(length):
        replace = (position + index) % 256

        array[replace] = new_vals[index]


def many_xor(array):
    return reduce(lambda x, y: x ^ y, array)


def knothash(data):
    sequence = update_data(data)
    vals = list(range(256))
    position = 0
    skip_size = 0
    for _ in range(64):
        for length in sequence:
            reverse(vals, length, position)
            position = (position + length + skip_size) % 256
            skip_size += 1
    prev_index = 0
    hash_list = []
    for index in range(16, 256 + 1, 16):
        sub_list = vals[prev_index:index]
        prev_index = index
        hash_list.append(many_xor(sub_list))
    return ''.join('{:02X}'.format(d) for d in hash_list).lower()


def update_data(data):
    output = []
    for character in data:
        output.append(ord(character))
    output.extend([17, 31, 73, 47, 23])
    return output


def run_part_1(data):
    vals = list(range(256))
    position = 0
    skip_size = 0
    for entry in data.split(','):
        length = int(entry)
        reverse(vals, length, position)
        position = (position + length + skip_size) % 256
        skip_size += 1
    return vals[0] * vals[1]


@timeit
def get_answer(data, part2=False):
    if not part2:
        return run_part_1(data)
    return knothash(data)


if __name__ == '__main__':
    day = int(os.path.basename(__file__).split('.')[0].split('y')[1])
    inputs = get_instructions(day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
