from aoc_utilities import get_instructions
from pathlib import Path

from itertools import count


def parse_inputs(data):
    timestamp = int(data[0])
    buses = []
    for i, entry in enumerate(data[1].split(',')):
        if entry == 'x':
            continue
        buses.append((i, int(entry)))
    return timestamp, buses


def part1(timestamp, buses):
    min_val = timestamp
    min_bus = None
    for _, bus in buses:
        r = timestamp % bus
        check = bus - r
        if check < min_val:
            min_val = check
            min_bus = bus
    return min_val, min_bus


'''
after a lot of googling realized this is related to chinese remainer theorem
I'm still not 100% sure how to do the conversion, but for a set of buses at
various indices (the inputs) it seems clear to me that you have the following:
t mod b0 = (b0 - 0)
t mod b1 = (b1 - 1)
.
.
.
t mod bn = (bn - n)

now, the formulation for chinese remainder would be
x = (b0 - 0) mod b0
x = (bo - 1) mod b1
.
.
.
x = (bn - n) mod bn

this is essentially flipping t and (bi - i) in my original formulation. I think
this is always valid (because equality isn't really what I'm using, this is all
congruence, which I'm not great with)

assuming that, then I need a chinese remainder solver, i'm pulling from a few
places to write one based on reading algorithm descriptions
'''


## based on wikipedia extended euclidiean algorithm page
def mul_inv(a, n):
    t, t1 = 0, 1
    r, r1 = n, a

    # if n is 1 the loop will hang, but if n is 1 the answer is 1
    if n == 1:
        return 1

    while r1 != 0:
        q = r // r1
        (t, t1) = (t1, t - q * t1)
        (r, r1) = (r1, r - q * r1)

    if t < 0:
        t += n
    return t


## pulled from various sources, i eventually figured it out, based on the
## constructed solution to chinese remainder theorem
def chinese_remainders(lefts, rights):
    prod = 1
    for val in rights:
        prod *= val

    result = 0
    for l, r in zip(lefts, rights):
        b = prod // r

        result += l * b * mul_inv(b, r)

    return result % prod



def get_answer(data, part2=False):
    timestamp, buses = parse_inputs(data)

    if not part2:
        min_val, min_bus = part1(timestamp, buses)
        return min_val * min_bus

    lefts = []
    rights = []
    for mod, bus in buses:
        lefts.append(bus - mod)
        rights.append(bus)

    return chinese_remainders(lefts, rights)



if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)

#     inputs = '''2
# 3,x,4,5'''.split('\n')

#     inputs = '''939
# 7,13,x,x,59,x,31,19'''.split('\n')

#     inputs = '''1
# 67,7,x,59,61'''.split('\n')

    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
