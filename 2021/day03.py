from aoc_utilities import get_instructions
from pathlib import Path


def get_counts(data):
    counts = {i: {'0': 0, '1': 0} for i, _ in enumerate(data[0])}
    for entry in data:
        for i, val in enumerate(entry):
            counts[i][val] += 1
    return counts


def part_1(counts):
    gamma = ''
    epsilon = ''
    for i in range(len(counts)):
        e = min(counts[i].items(), key=lambda x: x[1])[0]
        g = max(counts[i].items(), key=lambda x: x[1])[0]
        gamma += g
        epsilon += e
    return int(gamma, 2) * int(epsilon, 2)


def part_2(data, counts):
    o_sub = data[:]
    c_sub = data[:]
    oxy = run_rating(o_sub, counts, 0)
    c02 = run_rating(c_sub, counts, 1)
    return int(oxy, 2) * int(c02, 2)


def run_rating(sub, counts, which=0):
    for i in range(len(counts)):
        min_val = min(counts[i].items(), key=lambda x: x[1])
        max_val = max(counts[i].items(), key=lambda x: x[1])
        if min_val[1] == max_val[1]:
            val = ('1', '0')[which]
        else:
            val = (max_val[0], min_val[0])[which]
        sub = [x for x in sub if x[i] == val]
        counts = get_counts(sub)
        if len(sub) == 1:
            return sub[0]


def get_answer(data, part2=False):
    counts = get_counts(data)
    print(counts)
    if part2:
        return part_2(data, counts)
    return part_1(counts)


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
