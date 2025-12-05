from aoc_utilities import get_instructions
from pathlib import Path


def parse_input(data):
    ranges = {}
    values = []
    get_ranges = True
    for row in data:
        if row == '':
            get_ranges = False
            continue
        if get_ranges:
            low, high = sorted(map(int, row.split('-')))
            if low not in ranges:
                ranges[low] = []
            ranges[low].append(high)
        else:
            values.append(int(row))
    return ranges, values


def get_all_ids(ranges):
    low = None
    high = None
    filtered = {}
    for k in sorted(ranges):
        if low is None:
            low = k
        if high is not None:
            if k > high:
                filtered[low] = high
                low = k
                high = None
        check = max(ranges[k])
        if high is None:
            high = check
        if check > high:
            high = check
    filtered[low] = high
    num_ids = 0
    for low, high in filtered.items():
        num_ids += high - low + 1
    return num_ids



def get_answer(data, part2=False):
    ranges, values = parse_input(data)

    if part2:
        return get_all_ids(ranges)

    count = 0
    for val in values:
        add = False
        for k in ranges:
            if val >= k:
                for v in ranges[k]:
                    if val <= v:
                        add = True
                        break
        if add:
            count += 1
    return count


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)

#     inputs = '''3-5
# 10-14
# 16-20
# 12-18

# 1
# 5
# 8
# 11
# 17
# 32'''.split('\n')

    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
