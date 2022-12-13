from aoc_utilities import get_instructions
from pathlib import Path
from itertools import zip_longest
import json
from functools import cmp_to_key


def parse_instructions(data):
    packets = []
    left = None
    for line in data.split('\n\n'):
        left, right = map(json.loads, line.split('\n'))
        packets.append((left, right))
    return packets


def compare(left, right):
    for l, r in zip_longest(left, right):
        if l is None:
            return 1
        if r is None:
            return -1
        if isinstance(l, int) and isinstance(r, int):
            if l < r:
                return 1
            elif r < l:
                return -1
        elif isinstance(l, list) and isinstance(r, list):
            val = compare(l, r)
            if val is not 'continue':
                return val
        elif isinstance(l, list) and isinstance(r, int):
            val = compare(l, [r])
            if val is not 'continue':
                return val
        elif isinstance(l, int) and isinstance(r, list):
            val = compare([l], r)
            if val is not 'continue':
                return val
    else:
        return 'continue'


def get_answer(data, part2=False):
    packets = parse_instructions('\n'.join(data))
    correct = []
    if part2:
        lp, rp = zip(*packets)
        packets = list(lp) + list(rp)
        packets.append([[2]])
        packets.append([[6]])
        packets_sorted = sorted(packets, key=cmp_to_key(compare), reverse=True)
        i1 = packets_sorted.index([[2]])
        i2 = packets_sorted.index([[6]])
        return (i1 + 1) * (i2 + 1)
    for i, (left, right) in enumerate(packets, start=1):
        if compare(left, right) == 1:
            correct.append(i)
    return sum(correct)


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''[1,1,3,1,1]
# [1,1,5,1,1]

# [[1],[2,3,4]]
# [[1],4]

# [9]
# [[8,7,6]]

# [[4,4],4,4]
# [[4,4],4,4,4]

# [7,7,7,7]
# [7,7,7]

# []
# [3]

# [[[]]]
# [[]]

# [1,[2,[3,[4,[5,6,7]]]],8,9]
# [1,[2,[3,[4,[5,6,0]]]],8,9]'''.split('\n')
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
