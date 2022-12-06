from aoc_utilities import get_instructions
from pathlib import Path
from collections import Counter


def get_start(seq, check_length):
    for idx in range(check_length, len(seq) - check_length + 1):
        group = seq[idx-check_length:idx]
        if Counter(group).most_common()[0][1] == 1:
            return idx


def get_answer(data, part2=False):
    if part2:
        return get_start(data[0], 14)
    return get_start(data[0], 4)


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
