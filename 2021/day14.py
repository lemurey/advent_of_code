from aoc_utilities import get_instructions
from pathlib import Path

from collections import Counter, defaultdict


def get_rules(data):
    start_line = data[0]
    rules = {}
    for line in data[1:]:
        if line == '':
            continue
        pre, post = line.split(' -> ')
        rules[pre] = post

    start = Counter()
    for i, _ in enumerate(start_line):
        pair = start_line[i:i + 2]
        if len(pair) < 2:
            continue
        start[pair] += 1

    return rules, start


def run_insertion_v2(counts, rules):
    new = Counter()
    for k, v in counts.items():
        if k in rules:
            new[k[0] + rules[k]] += v
            new[rules[k] + k[1]] += v
    return new


def get_singles(counts, string):
    singles = Counter()
    for (k0, k1), v in counts.items():
        singles[k0] += v
        singles[k1] += v
    singles[string[0]] += 1
    singles[string[-1]] += 1
    return singles


def get_answer(data, part2=False):
    rules, output = get_rules(data)
    if part2:
        times = 40
    else:
        times = 10
    for _ in range(times):
        output = run_insertion_v2(output, rules)

    singles = get_singles(output, data[0])

    return ((singles.most_common()[0][1] // 2) -
            (singles.most_common()[-1][1] // 2))


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''NNCB

# CH -> B
# HH -> N
# CB -> H
# NH -> C
# HB -> C
# HC -> B
# HN -> C
# NN -> C
# BH -> H
# NC -> B
# NB -> B
# BN -> B
# BB -> N
# BC -> B
# CC -> N
# CN -> C'''.split('\n')
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
