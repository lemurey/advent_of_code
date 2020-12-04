from aoc_utilities import get_instructions
from pathlib import Path


def solve_part1(arr):
    store = {}
    for entry in arr:
        store[2020 - entry] = entry

    for entry in arr:
        if entry in store:
            return entry * store[entry]


def solve_part2(arr):
    store1 = {}
    store2 = {}
    for n1 in arr:
        for n2 in arr:
            if (2020 - n1 - n2) in arr:
                return (2020 - n1 - n2) * n1 * n2


def get_answer(data, part2=False):
    store = {}
    data = set([int(x) for x in data])

    if not part2:
        return solve_part1(data)
    return solve_part2(data)


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)

    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))