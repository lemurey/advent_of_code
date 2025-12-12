from aoc_utilities import get_instructions
from pathlib import Path


def parse_input(lines):
    sizes = (7, 7, 7, 7, 6, 5)
    areas = []
    presents = []
    for i, line in enumerate(lines):
        if i < 30:
            continue
        size, rest = line.split(': ')
        a, b = map(int, size.split('x'))
        areas.append(a * b)
        cur = []
        for entry in rest.split(' '):
            cur.append(int(entry))
        presents.append(cur)
    return sizes, areas, presents


def get_answer(data, part2=False):
    sizes, areas, presents = parse_input(data)
    total = 0
    for a, pres in zip(areas, presents):
        cur = 0
        for s, p in zip(sizes, pres):
            cur += s * p
        if a >= cur:
            total += 1
    return total

if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))
