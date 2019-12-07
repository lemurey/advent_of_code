from aoc_utilities import get_instructions
import os


def path_to_com(orbits, start):
    path = set()
    current = start
    while current != 'COM':
        current = orbits[current]
        path.add(current)
    return path


def parse_inputs(data):
    orbits = {}
    for line in data:
        base, orbit = line.split(')')
        orbits[orbit] = base
    return orbits


def get_answer(data):
    orbits = parse_inputs(data)
    total = 0
    for obj in orbits:
        path = path_to_com(orbits, obj)
        total += len(path)
    print('part1: {}'.format(total))

    def sort_func(x):
        return len(path_to_com(orbits, x))

    you = orbits['YOU']
    san = orbits['SAN']

    you_path = path_to_com(orbits, you)
    san_path = path_to_com(orbits, san)

    common_nodes = you_path.intersection(san_path)
    furthest_common = sorted(common_nodes, key=sort_func)[-1]
    distance_common = sort_func(furthest_common)

    you_to_common = len(you_path) - distance_common
    san_to_common = len(san_path) - distance_common

    print('part2: {}'.format(you_to_common + san_to_common))


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    sample = '''COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN'''.split('\n')
    # get_answer(sample)
    day = int(day.split('.')[0].split('y')[1])
    inputs = get_instructions(year, day)
    get_answer(inputs)
