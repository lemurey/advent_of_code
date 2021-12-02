from aoc_utilities import get_instructions
from pathlib import Path


def part_2(data):
    aim = 0
    position = 0 + 0j
    directions = {'up': -1,
                  'down': 1,
                  'forward': 1}

    for instruction in data:
        direction, mag = instruction.split(' ')
        if direction == 'forward':
            position += directions[direction] * int(mag)
            position += aim * 1j * int(mag)
        else:
            aim += directions[direction] * int(mag)
    return position.real * position.imag


def get_answer(data, part2=False):

    if part2:
        return part_2(data)

    position = 0 + 0j
    directions = {'up': -1j,
                  'down': 1j,
                  'forward': 1}

    for instruction in data:
        direction, mag = instruction.split(' ')
        position += directions[direction] * int(mag)
    return position.real * position.imag


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
