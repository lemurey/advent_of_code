from aoc_utilities import get_instructions
import os
from collections import deque


STEPS = {'n': (0, 1, -1), 'ne': (1, 0, -1), 'se': (1, -1, 0),
         's': (0, -1, 1), 'sw': (-1, 0, 1), 'nw': (-1, 1, 0)}


def hex_distance(start, stop):
    x1, y1, z1 = start
    x2, y2, z2 = stop
    return (abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)) / 2


def travel_path(steps):
    location = (0, 0, 0)
    max_distance = 0
    for step in steps.split(','):
        location = update(location, STEPS[step])
        distance = hex_distance((0, 0, 0), location)
        if distance > max_distance:
            max_distance = distance

    return location, max_distance


def update(current, step):
    x, y, z = current
    dx, dy, dz = step
    return x + dx, y + dy, z + dz


def get_answer(data, part2=False):
    end_node, max_distance = travel_path(data)
    if part2:
        return max_distance
    return hex_distance((0, 0, 0), end_node)


if __name__ == '__main__':
    day = int(os.path.basename(__file__).split('.')[0].split('y')[1])
    inputs = get_instructions(day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
