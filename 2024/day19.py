from aoc_utilities import get_instructions
from pathlib import Path
from functools import cache


def get_towels_and_logs(data):
    towels = tuple(sorted(data[0].split(', '), key=lambda x: len(x)))
    logos = []
    for row in data[2:]:
        logos.append(row)
    return towels, logos


@cache
def check_logo(logo, towels):
    valids = []
    for towel in towels:
        if logo == towel:
            valids.append(1)
        elif logo.startswith(towel):
            valids.append(check_logo(logo[len(towel):], towels))
        else:
            valids.append(0)
    return sum(valids)


def get_answer(data, part2=False):
    towels, logos = get_towels_and_logs(data)

    num_logos = []
    for i, logo in enumerate(logos):
        num_logos.append(check_logo(logo, towels))
    if part2:
        return sum(num_logos)
    return sum(1 if x > 0 else 0 for x in num_logos)


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)

#     inputs = '''r, wr, b, g, bwu, rb, gb, br

# brwrr
# bggr
# gbbr
# rrbgbr
# ubwu
# bwurrg
# brgr
# bbrgwb'''.split('\n')

    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
