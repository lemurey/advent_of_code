from aoc_utilities import get_instructions
from pathlib import Path
import re

CHECK = re.compile(r'^(\d+)\1$')
CHECK2 = re.compile(r'^(\d+)\1+$')


def parse_input(lines):
    ranges = []
    for line in lines:
        opts = line.split(',')
        for entry in opts:
            start, end = map(int, entry.split('-'))
            ranges.append((start, end))
    return ranges


def check_id(id, part2):
    if part2:
        c = CHECK2
    else:
        c = CHECK
    if c.match(str(id)):
        return True
    return False


def get_answer(data, part2=False):
    ranges = parse_input(data)
    output = 0
    for start, stop in ranges:
        for val in range(start, stop + 1):
            if check_id(val, part2):
                output += val
    return output


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)

    # inputs = ['11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124']

    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
