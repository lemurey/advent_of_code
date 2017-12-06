from aoc_utilities import get_instructions
import os


def run_row(row, mode):
    if mode == 'part1':
        max_val = row[0]
        min_val = row[0]
        for entry in row:
            if entry > max_val:
                max_val = entry
            if entry < min_val:
                min_val = entry
        return max_val - min_val
    for i, entry in enumerate(row):
        for entry2 in row[i + 1:]:
            if entry % entry2 == 0:
                return entry / entry2
            if entry2 % entry == 0:
                return entry2 / entry


def get_answer(data, mode):
    checksum = 0
    for row in data.split('\n'):
        parsed = list(map(int, row.split()))
        value = run_row(parsed, mode)
        checksum += value
    return checksum


if __name__ == '__main__':
    day = int(os.path.basename(__file__).split('.')[0].split('y')[1])
    inputs = get_instructions(day)
    print(get_answer(inputs, mode='part1'))
    print(get_answer(inputs, mode='part2'))
