from aoc_utilities import get_instructions
from pathlib import Path

SCORES = dict(zip('abcdefghijklmnopqrstuvwxyz',
              range(1, 27)))
adds = dict(zip('ABCDEFGHIJKLMNOPQRSTUVWXYZ',
              range(27, 53)))
SCORES.update(adds)


def check_pack(contents):
    val = len(contents) // 2
    left = set()
    right = set()
    for idx in range(val):
        l, r = contents[idx], contents[idx + val]
        left.add(l)
        right.add(r)
    return list(left.intersection(right))[0]


def check_group(contents):
    first = set(contents[0])
    second = set(contents[1])
    third = set(contents[2])
    commons = first.intersection(second).intersection(third)
    return list(commons)[0]


def get_answer(data, part2=False):
    total = 0
    group = []
    part2 = 0
    for line in data:
        common = check_pack(line)
        total += SCORES[common]
        group.append(line)
        if len(group) == 3:
            badge = check_group(group)
            part2 += SCORES[badge]
            group = []
    return total, part2


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))
