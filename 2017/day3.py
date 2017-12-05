from aoc_utilities import get_instructions
from utilities import timeit
import os


def make_mods(size, direction='negative'):
    if direction == 'negative':
        mod_vals = [-1, 1j, 1, -1j]
    else:
        mod_vals = [1j, -1, -1j, 1]

    mods = {i * (size - 1): mod_vals[i] for i in range(1, 4)}
    return mod_vals[0], mods


def check_neighbors(values, key):
    dirs = (complex( 0,  1),
        complex( 0, -1),
        complex( 1,  0),
        complex(-1,  0),
        complex( 1,  1),
        complex(-1, -1),
        complex( 1, -1),
        complex(-1,  1)
        )
    total = 0
    for check in dirs:
        if check + key in values:
            total += values[key + check]
    return total


def next_square(values, key, size, steps, n):
    mod, mods = make_mods(size, direction='positive')
    for step, _ in enumerate(xrange(steps), 1):
        if step in mods:
            mod = mods[step]
        total = check_neighbors(values, key)
        values[key] = total
        if total > n:
            return False, total, values
        key = key + mod
    return key, total, values


def part2(n):
    key = complex(0, 0)
    values = {key: 1}
    iterations = 1
    prev_size = 1
    key = key + complex(1, 0)
    for size, _ in get_size(n):
        steps = size ** 2 - prev_size
        key, total, values = next_square(values, key, size, steps, n)
        if not key:
            return total
        prev_size = size ** 2


def distance(loc):
    return int(abs(loc.real) + abs(loc.imag))


def get_size(value):
    size = 1
    spot = 0
    if value == 1:
        yield 1, 0
        return
    while size ** 2 <= value:
        size += 2
        spot += 1
        yield size, spot


def part1(n):
    size, spot = list(get_size(n))[-1]
    place = complex(spot, -spot)
    check = size ** 2
    mod, mods = make_mods(size)
    step = 0
    while (check - step) != n:
        step += 1
        place += mod
        if step in mods:
            mod = mods[step]
    return distance(place)


@timeit
def get_answer(data, mode):
    value = int(data)
    if mode == 'part1':
        return part1(value)
    else:
        return part2(value)


if __name__ == '__main__':
    day = int(os.path.basename(__file__).split('.')[0].split('y')[1])
    inputs = get_instructions(day)
    print(get_answer(inputs, mode='part1'))
    print(get_answer(inputs, mode='part2'))
