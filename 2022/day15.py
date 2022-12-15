from aoc_utilities import get_instructions
from pathlib import Path

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __str__(self):
        return f'{self.x}, {self.y}'


def parse_instructions(data):
    sensors = {}
    beacons = set()
    for row in data:
        s, b = row.split(':')
        sx = int(s.split(',')[0].split('=')[1])
        sy = int(s.split(',')[1].split('=')[1])
        bx = int(b.split(',')[0].split('=')[1])
        by = int(b.split(',')[1].split('=')[1])
        sensor = Point(sx, sy)
        beacon = Point(bx, by)
        if sensor in sensors:
            print('duplicate sensor')
        sensors[sensor] = sensor - beacon
        beacons.add(beacon)

    return sensors, beacons


def _single_check(ol, oh, low, high):
     # check for any extensions
    if (((ol <= low <= oh) and (high >= oh)) or
        ((ol <= high <= oh) and (ol >= low)) or
        ((low <= ol) and (high >= oh))):
        nl, nh = min(ol, low), max(oh, high)
        return (nl, nh), False
    # check if subset
    elif ((ol <= low) and (oh >= high)):
        return (ol, oh), False
    else:
        return (ol, oh), True


def get_checks(checks, low, high):
    if len(checks) == 0:
        checks.add((low, high))
        return checks
    copy = set()
    append = True
    for ol, oh in checks:
        r, a = _single_check(ol, oh, low, high)
        append = a and append
        copy.add(r)
    if append:
        copy.add((low, high))
    return copy


def consolidate_checks(checks):
    checks = sorted(checks)
    if len(checks) == 0:
        return checks
    new = set([checks[0]])
    for low, high in checks[1:]:
        new = get_checks(new, low, high)
    return new


def get_row(sensors, beacons, row=2000000, part2=False):
    checks = set()
    for s, max_d in sensors.items():
        x = max_d - abs(s.y - row)
        if x < 0:
            continue
        low = s.x - x
        high = s.x + x
        checks = get_checks(checks, low, high)
    # print(checks)
    checks = consolidate_checks(checks)
    # print(checks)
    if part2:
        return checks
    impossible = 0
    for low, high in checks:
        for c in range(low, high + 1):
            check = Point(c, row)
            if check not in beacons:
                impossible += 1
    return impossible

# def alt_check(sensors, beacons):
#     grid = {}
#     (min_x, max_x, min_y, max_y) = (0,0,0,0)
#     for s, max_d in sensors.items():
#         if (s.x - max_d) < min_x:
#             min_x = s.x - max_d
#         if (s.y - max_d) < min_y:
#             min_y = s.y - max_d
#         if (s.x + max_d) > max_x:
#             max_x = s.x + max_d
#         if (s.y + max_d) > max_y:
#             max_y = s.y + max_d

#         for y_val in range(s.y - max_d, s.y + max_d+1):
#             for x_val in range(s.x - max_d, s.x + max_d+1):
#                 c = Point(x_val, y_val)
#                 if (s - c) > max_d:
#                     continue
#                 if c in beacons:
#                     grid[c] = 'B'
#                 elif c in sensors:
#                     grid[c] = 'S'
#                 else:
#                     grid[c] = '#'

#     show_grid(grid, min_x, max_x, min_y, max_y)
#     print(min_x, max_x, min_y, max_y)

# def show_grid(grid, min_x, max_x, min_y, max_y, part2=False):
#     for y in range(min_y, max_y + 1):
#         row = f'{y: >4} '
#         for x in range(min_x, max_x + 1):
#             if Point(x, y) in grid:
#                 row += grid[Point(x, y)]
#             else:
#                 row += '.'
#         print(row)


def run_part2(sensors, beacons):
    for y in range(4000000):
        checks = get_row(sensors, beacons, y, part2=True)
        if len(checks) > 1:
            print(y, checks)
            checks = list(checks)
            x_low, x_high = sorted((checks[0][1], checks[1][0]))
            x = x_low + 1
            print(x, y)
            return 4000000 * x + y


def get_answer(data, part2=False):
    sensors, beacons = parse_instructions(data)
    if part2:
        return run_part2(sensors, beacons)
    num_impossible = get_row(sensors, beacons)
    # alt_check(sensors, beacons)
    return num_impossible

if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''Sensor at x=2, y=18: closest beacon is at x=-2, y=15
# Sensor at x=9, y=16: closest beacon is at x=10, y=16
# Sensor at x=13, y=2: closest beacon is at x=15, y=3
# Sensor at x=12, y=14: closest beacon is at x=10, y=16
# Sensor at x=10, y=20: closest beacon is at x=10, y=16
# Sensor at x=14, y=17: closest beacon is at x=10, y=16
# Sensor at x=8, y=7: closest beacon is at x=2, y=10
# Sensor at x=2, y=0: closest beacon is at x=2, y=10
# Sensor at x=0, y=11: closest beacon is at x=2, y=10
# Sensor at x=20, y=14: closest beacon is at x=25, y=17
# Sensor at x=17, y=20: closest beacon is at x=21, y=22
# Sensor at x=16, y=7: closest beacon is at x=15, y=3
# Sensor at x=14, y=3: closest beacon is at x=15, y=3
# Sensor at x=20, y=1: closest beacon is at x=15, y=3'''.split('\n')
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
