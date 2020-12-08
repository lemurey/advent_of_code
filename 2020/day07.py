from aoc_utilities import get_instructions
from pathlib import Path

from collections import deque


def process_rules(data):
    bags = {}
    for row in data:
        preface, bag_list = row.split(' contain ')
        bag_color = ' '.join(preface.split(' ')[:-1])
        if bag_color in bags:
            print('duplicate entry found')
        else:
            bags[bag_color] = {}

        for entry in bag_list.strip().split(', '):
            contents = entry.split(' ')
            if contents[0] == 'no':
                continue
            num = int(contents[0])
            color = ' '.join(contents[1:-1])
            bags[bag_color][color] = num

    return bags


def find_gold(bags):
    can_hold = set()
    to_check = set()

    for k, v in bags.items():
        if 'shiny gold' in v:
            can_hold.add(k)
        elif len(v) > 0:
            to_check.add(k)

    c = 0
    while True:
        c += 1

        no_new_found = True
        for bag in to_check:
            for sub_bag in bags[bag]:
                if sub_bag in can_hold and bag not in can_hold:
                    can_hold.add(bag)
                    no_new_found = False

        if no_new_found:
            break

        if c > 25:
            print('high iteration break')
            break

    return can_hold


def num_inside(bags, start='shiny gold'):
    contains = 0
    Q = deque([start])
    seen = set()

    while Q:
        next_bag = Q.popleft()
        if next_bag in seen:
            continue

        for k, v in bags[next_bag].items():
            Q.append(k)
            seen.add(k)

            contains += v * (1 + num_inside(bags, k))

    return contains


def get_answer(data, part2=False):
    bags = process_rules(data)

    can_hold = find_gold(bags)

    print(len(can_hold))

    return num_inside(bags)


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)

#     inputs = '''light red bags contain 1 bright white bag, 2 muted yellow bags.
# dark orange bags contain 3 bright white bags, 4 muted yellow bags.
# bright white bags contain 1 shiny gold bag.
# muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
# shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
# dark olive bags contain 3 faded blue bags, 4 dotted black bags.
# vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
# faded blue bags contain no other bags.
# dotted black bags contain no other bags.'''.split('\n')

#     inputs = '''shiny gold bags contain 2 dark red bags.
# dark red bags contain 2 dark orange bags.
# dark orange bags contain 2 dark yellow bags.
# dark yellow bags contain 2 dark green bags.
# dark green bags contain 2 dark blue bags.
# dark blue bags contain 2 dark violet bags.
# dark violet bags contain no other bags.'''.split('\n')

    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))
