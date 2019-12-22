from aoc_utilities import get_instructions
import os
from intcode import Intcode


def inbeam(comp, x, y):
    comp.reset()
    comp.secondary = [x, y]
    return comp.run()


def search(comp, start_y):
    y_val = start_y
    left = 0
    while True:
        bottom_left = left, y_val
        if inbeam(comp, *bottom_left):
            top_right = bottom_left[0] + 99, bottom_left[1] - 99
            if inbeam(comp, *top_right):
                top_left = bottom_left[0], bottom_left[1] - 99
                return 10000 * top_left[0] + top_left[1]
            else:
                y_val += 1
        else:
            left += 1


def get_answer(data, part2=False):

    program = list(map(int, data[0].split(',')))
    comp = Intcode(program, mode='drone')

    if part2:
        return search(comp, 10)

    x_max = 50
    y_max = 50
    count = 0
    for y in range(y_max):
        for x in range(x_max):
            if inbeam(comp, x, y):
                print('#', end='')
                count += 1
            else:
                print('.', end='')
        print()
    return count


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
