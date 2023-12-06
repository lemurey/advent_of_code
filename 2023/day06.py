from aoc_utilities import get_instructions
from pathlib import Path

from math import floor, ceil


def run_race(total_time, hold_time):
    speed = hold_time
    distance = speed * (total_time - hold_time)
    return distance


def fast_version(total_time, r):
    '''
    just need to solve h**2 - ht + r = 0, it's time for the quadratic formula!
    (t +/- (t**2 - 4r) ** 1/2) / 2

    this is for exact equality, so add a small amount to r to gauruntee victory
    '''
    r += 0.01
    o1 = (total_time + ((total_time**2) - (4 * r))**0.5) / 2
    o2 = (total_time - ((total_time**2) - (4 * r))**0.5) / 2
    # we want  times greater than the smaller and less than larger
    o1, o2 = sorted((o1, o2))

    return ceil(o1), floor(o2)


def get_answer(data, part2=False):
    if part2:
        times = [int(''.join(x.strip() for x in data[0].split(':')[1].split()))]
        records = [int(''.join(x.strip() for x in data[1].split(':')[1].split()))]
    else:
        times = [int(x.strip()) for x in data[0].split(':')[1].split()]
        records = [int(x.strip()) for x in data[1].split(':')[1].split()]

    modes = 1
    for t, r in zip(times, records):
        l, h = fast_version(t, r)
        modes *= (h - l) + 1
    return modes



if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''Time:      7  15   30
# Distance:  9  40  200'''.split('\n')
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
