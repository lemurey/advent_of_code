from aoc_utilities import get_instructions
from pathlib import Path
from operator import add, mul
from functools import reduce

OPS = {'*': mul, '+': add}

def parse_input(data, part2):
    store = []
    if not part2:
        for row in data:
            store.append(row.split())
        return [x for x in zip(*store[::-1])]
    ## python zip truncates at smallest row, not all my rows are the same
    ## length, so pad any shorter ones with spaces to make the flipping work
    length = max(len(row) for row in data)
    new = []
    for row in data:
        if len(row) < length:
            row = row + ' ' * (length - len(row))
        new.append(row)
    flipped = zip(*new)
    store = []
    op = None
    nums = []
    for entry in flipped:
        num = ''
        if all(x == ' ' for x in entry):
            store.append((op, *nums))
            op = None
            nums = []
            continue
        for val in entry:
            if val in '*+':
                op = val
            elif val == ' ':
                continue
            else:
                num += val
        nums.append(num)
    store.append((op, *nums))
    return store


def get_answer(data, part2=False):
    problems = parse_input(data, part2)
    # for row in problems:
    #     print(row)
    total = 0
    for row in problems:
        op, nums = row[0], map(int, row[1:])
        if op == '*':
            val = reduce(OPS[op], nums, 1)
        else:
            val = reduce(OPS[op], nums, 0)
        total += val
    return total


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)

#     inputs = '''123 328  51 64 
#  45 64  387 23 
#   6 98  215 314
# *   +   *   +  '''.split('\n')

    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
