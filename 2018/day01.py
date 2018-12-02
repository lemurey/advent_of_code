from aoc_utilities import get_instructions
from itertools import cycle
import os


def get_answer(data, part2=False):
    data = map(int, data.split())
    seen = set([0])
    total = 0
    count = 0
    for num in cycle(data):
        total += num
        count += 1
        if ((total in seen) and part2) or ((count == len(data)) and not part2):
            break
        seen.add(total)
    return total


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))