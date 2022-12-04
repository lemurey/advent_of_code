from aoc_utilities import get_instructions
from pathlib import Path

def parse_instructions(data):
    output = []
    for line in data:
        a, b = line.split(',')
        a = list(map(int, a.split('-')))
        b = list(map(int, b.split('-')))
        output.append((min(a), max(a), min(b), max(b)))
    return output


def part1(pairs):
    count = 0
    for first_low, first_high, second_low, second_high in pairs:
        left = set(range(first_low, first_high+1))
        right = set(range(second_low, second_high+1))
        if left.issuperset(right) or right.issuperset(left):
           count += 1
    return count


def run_part2(pairs):
    count = 0
    for first_low, first_high, second_low, second_high in pairs:
        left = set(range(first_low, first_high+1))
        right = set(range(second_low, second_high+1))
        if len(left.intersection(right)) > 0:
            count += 1
    return count


def get_answer(data, part2=False):
    lines = parse_instructions(data)
    if part2:
        return run_part2(lines)
    return part1(lines)


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''2-4,6-8
# 2-3,4-5
# 5-7,7-9
# 2-8,3-7
# 6-6,4-6
# 2-6,4-8'''.split('\n')
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
