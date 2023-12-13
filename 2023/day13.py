from aoc_utilities import get_instructions
from pathlib import Path


def parse_data(data):
    patterns = []
    cur_pattern = []
    for row in data:
        if row == '':
            patterns.append(cur_pattern)
            cur_pattern = []
            continue
        cur_pattern.append(row)
    patterns.append(cur_pattern)
    return patterns


def run_check(p, size, c_val):
    checks = []
    for b in range(size):
        diffs = 0
        checked = False
        for o in range(1, b+1):
            l = b - o
            r = b + o - 1
            if (l < 0) or (r > size-1):
                if (l < 0) and (r < size -1):
                    valid = False
                break
            lc = ''.join(row[l] for row in p)
            rc = ''.join(row[r] for row in p)
            checked = True
            for ll, rr in zip(lc, rc):
                if ll != rr:
                    diffs += 1
        if diffs == c_val and checked:
            return b
    return 0


def check_pattern(p, c_val=0):
    x_size = len(p[0])
    y_size = len(p)

    x_check = run_check(p, x_size, c_val)
    y_check = run_check(list(zip(*p)), y_size, c_val)

    return x_check, y_check



def get_answer(data, part2=False):
    patterns = parse_data(data)
    total = 0
    for pattern in patterns:
        xc, yc = check_pattern(pattern, 0)
        # print(yc, xc)
        total += xc
        total += yc * 100

    print(total)
    total = 0
    for pattern in patterns:
        xc, yc = check_pattern(pattern, 1)
        # print(yc, xc)
        total += xc
        total += yc * 100
    return total


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))
