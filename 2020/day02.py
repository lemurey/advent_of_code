from aoc_utilities import get_instructions
from pathlib import Path


def process_inputs(inputs):
    output = []
    for row in inputs:
        left, password = row.split(': ')
        low, right = left.split('-')
        high, letter = right.split(' ')
        low = int(low)
        high = int(high)
        output.append(((low, high, letter), password))
    return output


def is_valid(policy, password):
    low, high, letter = policy

    if (password.count(letter) >= low) and (password.count(letter) <= high):
        return True
    return False


def is_valid_2(policy, password):
    low, high, letter = policy
    c1 = password[low - 1]
    c2 = password[high - 1]

    if (c1 == letter) ^ (c2 == letter):
        return True
    return False


def get_answer(data, part2=False):
    inputs = process_inputs(data)

    count = 0
    for policy, password in inputs:
        if part2:
            if is_valid_2(policy, password):
                count += 1
        else:
            if is_valid(policy, password):
                count += 1

    return count


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
