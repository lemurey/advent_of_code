from aoc_utilities import get_instructions
from pathlib import Path


def run_process(data):
    all_histories = []
    for row in data:
        check = list(map(int, row.split()))
        history = [check]
        while not all(x == 0 for x in check):
            diffs = [y - x for x, y in zip(check[:-1], check[1:])]
            history.append(diffs)
            check = diffs
        all_histories.append(history)
    return all_histories


def get_answer(data, part2=False):
    histories = run_process(data)
    total = 0
    t2 = 0
    for group in histories:
        total += sum(x[-1] for x in group)
        prev = 0
        for entry in group[::-1]:
            cur = entry[0]
            new = cur - prev
            prev = new
        t2 += new
    return total, t2


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''0 3 6 9 12 15
# 1 3 6 10 15 21
# 10 13 16 21 30 45'''.split('\n')
    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))
