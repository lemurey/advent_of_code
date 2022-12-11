from aoc_utilities import get_instructions
from pathlib import Path
from operator import add, mul
from functools import partial

OPS = {'+': add, '*': mul}


def parse_instructions(data):
    monkies = []
    count = 0
    for line in data:
        count += 1
        if line.startswith('Monkey'):
            monkey = {}
            count = 0
            continue
        if line == '':
            monkies.append(monkey)
            continue
        _, rest = line.split(':')
        if count == 1:
            key = 'items'
            val = list(map(int, rest.strip().split(', ')))
        elif count == 2:
            key = 'op'
            ops = rest.strip().split(' = ')[1].split()
            if ops[2] == 'old':
                val = (pow, 2)
            else:
                val = (OPS[ops[1]], int(ops[2]))
        else:
            key = 'test'
            m = int(rest.split()[-1].strip())
            if count == 3:
                check = m
            elif count == 4:
                true_monkey = m
            else:
                val = (check, true_monkey, m)
        if count in (1, 2, 5):
            monkey[key] = val
    monkies.append(monkey)
    return monkies


def turn(monkies, idx, p2, big_mod):
    monkey = monkies[idx]
    inspections = 0
    for _ in range(len(monkey['items'])):
        worry = monkey['items'].pop(0)
        inspections += 1
        f, v = monkey['op']
        worry = f(worry, v)
        if p2:
            worry = worry % big_mod
        else:
            worry = worry // 3
        c, tm, fm = monkey['test']
        if worry % c == 0:
            new_idx = tm
        else:
            new_idx = fm
        monkies[new_idx]['items'].append(worry)
    return inspections


def round(monkies, counts, p2, big_mod):
    for monkey_index in range(len(monkies)):
        inspections = turn(monkies, monkey_index, p2, big_mod)
        counts[monkey_index] += inspections
    return counts


def get_answer(data, part2=False):
    monkies = parse_instructions(data)
    counts = [0 for _ in monkies]
    '''
    for part2 modulo all worry by the product of all tests
    I am bad at modulo math, so I don't quite fully understand why
    this works, but it basically makes it so no matter what check you
    do it will modulo the same way, but still keeps the numbers from
    getting massive
    '''
    big_mod = 1
    for m in monkies:
        big_mod *= m['test'][0]
    if part2:
        num_rounds = 10000
    else:
        num_rounds = 20
    for r in range(num_rounds):
        if r % 100 == 0:
            print(r)
        round(monkies, counts, part2, big_mod)
    m1, m2 = sorted(counts, reverse=True)[:2]
    return m1 * m2


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
