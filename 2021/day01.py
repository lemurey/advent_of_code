from aoc_utilities import get_instructions
from pathlib import Path


def get_increases(values, size):
    prev = None
    increases = 0
    for i, _ in enumerate(values):
        chunk = values[i:i+size]
        if len(chunk) < size:
            return increases
        value = sum(chunk)
        if prev is None:
            pass
        elif value > prev:
            increases += 1
        prev = value
    return increases


def get_answer(data, part2=False):
    values = [int(x) for x in data]
    if part2:
        return get_increases(values, 3)
    return get_increases(values, 1)


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
