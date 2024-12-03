from aoc_utilities import get_instructions
from pathlib import Path


def sign(x):
    if x < 0:
        return -1
    if x > 0:
        return 1
    if x == 0:
        return 0


def check_data(data):
    is_safe = []
    dampener = []
    for report in data:
        base = list(map(int, report.split()))
        
        checks = []
        values = [base] + [base[:i] + base[i+1:] for i in range(len(base))]
        
        for entry in values:
            which = None
            for l, r in zip(entry[:-1], entry[1:]):
                d = l - r
                c = sign(d)
                if which is None:
                    which = c
                if ((c == 0) or 
                    (c == 1 and which == -1) or 
                    (c == -1 and which == 1) or
                    (abs(d) > 3)):
                    checks.append(False)
                    break
            else:
                checks.append(True)
        is_safe.append(checks[0])
        if any(checks):
            dampener.append(True)
        else:
            dampener.append(False)

    return is_safe, dampener


def get_answer(data, part2=False):
    p1, p2 = check_data(data)
    if part2:
        return sum(p2)
    return sum(p1)


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''7 6 4 2 1
# 1 2 7 8 9
# 9 7 6 2 1
# 1 3 2 4 5
# 8 6 4 4 1
# 1 3 6 7 9'''.split('\n')
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
