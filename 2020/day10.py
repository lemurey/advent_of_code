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
        if prev_diff == diff:
            c += 1
        else:
            if prev_diff != 0:
                encoding.append((prev_diff, c))
            c = 1
        counts[diff] += 1
        prev_diff = diff
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
    lookups = {1: 1, 2: 2, 3: 4, 4: 7}
    for x in encoding:
        if x[0] != 1:
            continue
        val *= lookups[x[1]]

    return val


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)

    print(get_answer(inputs))
