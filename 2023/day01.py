from aoc_utilities import get_instructions
from pathlib import Path


def process_line(line):
    replacements = {"zero": "0", "one": "1", "two": "2", "three": "3",
                    "four": "4", "five": "5", "six": "6", "seven": "7",
                    "eight": "8", "nine": "9"}
    nl = ''
    for i, char in enumerate(line):
        if char.isdigit():
            nl += char
            continue
        for key in replacements.keys():
            if line[i:i+len(key)] == key:
                nl += replacements[key]
    return nl


def get_answer(data, part2=False):
    values = []
    for line in data:
        store = []
        if part2:
            nl = process_line(line)
        else:
            nl = ''.join(x for x in line if x.isdigit())
        values.append(int(nl[0] + nl[-1]))
    return sum(values)


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
