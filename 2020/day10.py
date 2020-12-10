from aoc_utilities import get_instructions
from pathlib import Path
from collections import defaultdict


def get_counts(arr):
    counts = {}
    encoding = []
    prev_diff = 0
    c = 0
    for v1, v2 in zip(arr[:-1], arr[1:]):
        diff = v2 - v1
        if diff not in counts:
            counts[diff] = 0

        if diff == 3:
            encoding.append((c))
            c = 0
        else:
            c += 1

        counts[diff] += 1
    return counts, encoding


def get_answer(data, part2=False):
    adapters = [0]
    max_a = 0
    for num in data:
        n = int(num)
        if n > max_a:
            max_a = n
        adapters.append(n)
    adapters.append(max_a + 3)
    adapters = sorted(adapters)

    counts, encoding = get_counts(adapters)

    print(counts[1] * counts[3])

    val = 1
    lookups = {0: 1, 1: 1, 2: 2, 3: 4, 4: 7} # manually did these
    for x in encoding:
        val *= lookups[x]

    return val


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)

    print(get_answer(inputs))
