from aoc_utilities import get_instructions
import os

import numpy as np

# rack id: x coordinate plus 10
# power level: rack id times y
# power level: power level + serial number (input)
# update power level to power level * rack ID
# keep only hundreds digit
# subtract 5 from level

X_SIZE = 300
Y_SIZE = 300

def calc_level(x, y, serial):
    rid = x + 10
    val = ((rid * y) + serial) * rid
    digit = (val / 100) % 10
    return digit - 5


def calc_powers(serial):
    grid = np.zeros(shape=(300, 300))
    for y in xrange(X_SIZE):
        for x in xrange(Y_SIZE):
            value = calc_level(x + 1, y + 1, serial)
            grid[x, y] = value
    return grid


def calc_sum(grid, x, y, offset=3, show_grid=False):
    if show_grid:
        return grid[x:x + 3, y:y + 3]
    return grid[x:x + offset, y:y + offset].sum()


def get_answer(data, part2=False):
    grid = calc_powers(data)
    max_power = 0
    max_id = (0, 0)

    if part2:
        offset = xrange(1, 301)
    else:
        offset = [3]

    for os in offset:
        for x in xrange(X_SIZE - os):
            for y in xrange(Y_SIZE - os):
                power = calc_sum(grid, x, y, os)
                if power > max_power:
                    max_power = power
                    max_id = (x + 1, y + 1, os)
    return max_id


if __name__ == '__main__':

    inputs = 9306
    # inputs = 42
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))