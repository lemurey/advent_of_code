from aoc_utilities import get_instructions
from utilities import timeit
import os


def get_counts(line):
    c = {}
    for letter in line:
        if letter not in c:
            c[letter] = 0
        c[letter] += 1
    return c


def comp_lines(a, b):
    diffs = 0
    output = ''
    for c1, c2 in zip(a, b):
        if c1 != c2:
            diffs += 1
        else:
            output += c1
    if diffs == 1:
        return output
    return False


@timeit
def alt_part2(data):
    for i in range(len(data[0])):
        checks = set()
        for line in data:
            update = ''.join([x for j, x in enumerate(line) if j != i])
            if update in checks:
                return update
            checks.add(update)


@timeit
def get_answer(data, part2=False):
    if not part2:
        twos, threes = 0, 0
        for line in data:
            counts = get_counts(line)
            a = any([1 for x in counts if counts[x] == 2])
            b = any([1 for x in counts if counts[x] == 3])
            twos += a
            threes += b
        return twos * threes
    diffs = []
    for i, l1 in enumerate(data):
        for l2 in data[i:]:
            out = comp_lines(l1, l2)
            if out:
                return out


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
    inputs = get_instructions(year, day)
    # print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
    print(alt_part2(inputs))
