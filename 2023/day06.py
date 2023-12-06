from aoc_utilities import get_instructions
from pathlib import Path


def run_race(total_time, hold_time):
    speed = hold_time
    distance = speed * (total_time - hold_time)
    return distance


def get_answer(data, part2=False):
    if part2:
        times = [int(''.join(x.strip() for x in data[0].split(':')[1].split()))]
        records = [int(''.join(x.strip() for x in data[1].split(':')[1].split()))]
    else:
        times = [int(x.strip()) for x in data[0].split(':')[1].split()]
        records = [int(x.strip()) for x in data[1].split(':')[1].split()]

    modes = 1
    for t, r in zip(times, records):
        cur = 0
        for i in range(t):
            d = run_race(t, i)
            if d > r:
                cur += 1
        modes *= cur
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
