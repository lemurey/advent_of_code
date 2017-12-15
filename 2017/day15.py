from aoc_utilities import get_instructions
from utilities import timeit
import os


def generator(seed, mult, check):
    prev = seed
    while True:
        prev = (prev * mult) % 2147483647
        if check is None or prev % check == 0:
            yield prev


def get_seed(data):
    A, B = data.split('\n')
    return int(A.split()[-1]), int(B.split()[-1])


def get_answer(data, part2=False):
    seed_a, seed_b = get_seed(data)
    count = 0
    match = 0
    end_val = 1000000
    if part2:
        end_val *= 5
    else:
        end_val *= 40
    if part2:
        a_check = 4
        b_check = 8
    else:
        a_check = None
        b_check = None
    gen_a = generator(seed_a, 16807, a_check)
    gen_b = generator(seed_b, 48271, b_check)

    for (a, b) in zip(gen_a, gen_b):
        count += 1
        if a % 65536 == b % 65536:
            match += 1
        if count == end_val:
            break
    return match


if __name__ == '__main__':
    day = int(os.path.basename(__file__).split('.')[0].split('y')[1])
    inputs = get_instructions(day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
