from aoc_utilities import get_instructions
from pathlib import Path


def parse_lists(data):
    left = []
    right = []
    for entry in data:
        l, r = map(int, entry.split())
        left.append(l)
        right.append(r)
    return left, right


def run_part2(left, right):
    counts = {}
    score = 0

    for entry in right:
        if entry not in counts:
            counts[entry] = 0
        counts[entry] += 1

    for entry in left:
        if entry not in counts:
            continue
        score += entry * counts[entry]

    return score


def get_answer(data, part2=False):
    left, right = parse_lists(data)
    total = 0
    for l, r in zip(sorted(left), sorted(right)):
        d = abs(l - r)
        total += d

    if part2:
        return run_part2(left, right)

    return total


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
