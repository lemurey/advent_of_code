from aoc_utilities import get_instructions
from pathlib import Path


def parse_inupts(data):
    groups = []
    group = {}
    size = 0
    for row in data:
        if row == '':
            group['size'] = size
            groups.append(group)
            group = {}
            size = 0
            continue
        for entry in row:
            if entry not in group:
                group[entry] = 0
            group[entry] += 1
        size += 1
    group['size'] = size
    groups.append(group)
    return groups


def get_answer(data, part2=False):
    groups = parse_inupts(data)
    count = 0
    p2 = 0
    for group in groups:
        size = group['size']
        for k, v in group.items():
            if k == 'size':
                continue
            if v == size:
                p2 += 1
            count += 1
    return count, p2


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))
