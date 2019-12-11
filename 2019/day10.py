from aoc_utilities import get_instructions
import os
from math import atan, pi


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'{self.x, self.y}'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __sub__(self, other):
        return (self.x - other.x, self.y - other.y)

    def __hash__(self):
        return hash((self.x, self.y))


def parse_grid(data):
    asteroids = []
    for j, row in enumerate(data):
        for i, val in enumerate(row):
            if val == '#':
                asteroids.append(Point(i, j))
    return asteroids


def adj_angle(y, x):
    if x == 0:
        if y > 0:
            result = pi / 2
        else:
            result = -pi / 2
    else:
        result = atan(y / x)
    if x < 0:
        return result + pi
    else:
        return result


def angle_and_distance(p1, points):
    output = {}
    for p2 in points:
        if p1 == p2:
            continue
        d_x, d_y = p2 - p1

        angle = adj_angle(d_y, d_x)
        angle = angle * (180 / pi)
        distance = (d_x ** 2 + d_y ** 2) ** 0.5
        output[p2] = (angle, distance)
    return output


def get_answer(data, part2=False):
    asteroids = parse_grid(data)

    num_in_view = {}
    max_in_view = 0
    best_point = None
    for a in asteroids:
        d_a = angle_and_distance(a, asteroids)
        v = len(set([x[0] for x in d_a.values()]))
        if v > max_in_view:
            max_in_view = v
            best_point = a

    if part2:
        d = angle_and_distance(best_point, asteroids)
        s = {}
        for key, (angle, distance) in d.items():
            if angle not in s:
                s[angle] = []
            s[angle].append((distance, key))
        ordered_angles = sorted(s, reverse=False)

        print(ordered_angles[0])

        for angle in ordered_angles:
            s[angle] = sorted(s[angle], key=lambda x: x[0])
        num_destroyed = 0
        i = 0
        while True:
            for angle in ordered_angles:
                if len(s[angle]) <= i:
                    continue
                num_destroyed += 1
                if num_destroyed == 200:
                    winner = s[angle][i][1]
                    return 100 * winner.x + winner.y
            i += 1

    return max_in_view


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
    inputs = get_instructions(year, day)
    sample = '''.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
'''.split('\n')
    # print(get_answer(sample, part2=True))
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
