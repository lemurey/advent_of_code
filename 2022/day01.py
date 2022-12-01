from aoc_utilities import get_instructions
from pathlib import Path


def parse_instructions(data):
    elves = []
    temp = []
    for line in data:
        if line == '':
            elves.append(tuple(temp))
            temp = []
        else:
            temp.append(int(line))
    return elves


def get_answer(data, part2=False):
    elves = parse_instructions(data)
    if part2:
        vals = map(sum, elves)
        return sum(sorted(vals, reverse=True)[:3])

    max_val = 0
    for food in elves:
        val = sum(food)
        if val > max_val:
            max_val = val
    return max_val


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
