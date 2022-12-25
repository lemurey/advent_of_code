from aoc_utilities import get_instructions
from pathlib import Path


def from_snafu(num):
    total = 0
    for i, char in enumerate(num[::-1]):
        if char == '-':
            val = -1
        elif char == '=':
            val = -2
        else:
            val = int(char)
        total += val * (5 ** i)
    return total


def to_snafu(num):
    s = ''
    while num:
        digit = num % 5
        if digit == 0:
            s = '0' + s
            num //= 5
        elif digit == 1:
            s = '1' + s
            num -= 1
            num  //= 5
        elif digit == 2:
            s = '2' + s
            num -= 2
            num //= 5
        elif digit == 3:
            s  = '=' + s
            num += 2
            num //= 5
        elif digit == 4:
            s = '-' + s
            num += 1
            num //= 5
    return s


def get_answer(data, part2=False):
    total = 0
    for num in data:
        n = from_snafu(num)
        print(n)
        total += n
    print()
    print(to_snafu(total))
    return total

if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))
