from aoc_utilities import get_instructions
import os


def check_double(c):
    if len(c) == len(set(c)):
        return False
    prev = c[0]
    for cur in c[1:]:
        if prev == cur:
            return True
        prev = cur
    return False

def check_increase(c):
    prev = c[0]
    for cur in c[1:]:
        if cur < prev:
            return False
        prev = cur
    return True

def check_chains(c):
    for val in set(c):
        if c.count(val) == 2:
            return True
    return False

def get_answer(data):
    low, high = map(int, data[0].split('-'))
    count = 0
    possible = []
    for num in range(low, high):
        c = str(num)
        if not check_double(c):
            continue
        if not check_increase(c):
            continue
        count += 1
        possible.append(num)
    print(count)
    count = 0
    for num in possible:
        if not check_chains(str(num)):
            continue
        count += 1
    print(count)

if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
    inputs = get_instructions(year, day)
    get_answer(inputs)
    # print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))