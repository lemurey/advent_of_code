from aoc_utilities import get_instructions
from pathlib import Path


def get_joltage(bank, size=2):
    fbank = str(bank)
    values = []
    for i in range(1, size+1):
        if i == size:
            value = max(fbank)
        else:
            value = max(fbank[:-size+i])
        index = fbank.index(value)
        fbank = fbank[index+1:]
        values.append(value)
    return int(''.join(values))


def get_answer(data, part2=False):
    output = 0
    size = 2
    if part2:
        size = 12
    for bank in data:
        joltage = get_joltage(bank, size)
        output += joltage
    return output


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
