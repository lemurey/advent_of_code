from aoc_utilities import get_instructions
from pathlib import Path

import re
checker = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)|don't\(\)|do\(\)")



def get_answer(data, part2=False):
    total = 0
    do_mult = True
    for entry in data:
        for val in checker.finditer(entry):
            if val[0] in ('do()', "don't()"):
                if part2 and val[0] == "don't()":
                    do_mult = 0
                else:
                    do_mult = 1
            else:
                total += (int(val[1]) * int(val[2])) * do_mult
    return total


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
    # inputs = ['xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))']
    # inputs = ['''xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))''']
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
