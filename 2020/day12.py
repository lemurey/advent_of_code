from aoc_utilities import get_instructions
from pathlib import Path
import re
from math import sin, cos, pi


class Ship:
    def __init__(self):
        self.heading = 1j
        self.location = 0 + 0j
        self.headings = {'N': 1, 'E': 1j, 'S': -1, 'W': -1j}
        self.turn_directions = {'R': 1j, 'L': -1j}
        self.turn_values = {90: 1, 180: 2, 270: 3}

    def turn(self, direction, value):
        a = self.turn_directions[direction]
        b = self.turn_values[value]
        for _ in range(b):
            self.heading *= a

    def move(self, direction, value):
        self.location += self.headings[direction] * value

    def forward(self, value):
        self.location += self.heading * value

    def calc_location(self):
        return abs(int(self.location.imag)) + abs(int(self.location.real))


class Waypoint(Ship):
    def __init__(self):
        self.location = 1 + 10j
        self.headings = {'N': 1, 'E': 1j, 'S': -1, 'W': -1j}
        self.turn_directions = {'R': 1j, 'L': -1j}
        self.turn_values = {90: 1, 180: 2, 270: 3}
        self.ship = 0 + 0j

    def rotation(self, value):
        x = self.location.real
        y = self.location.imag
        value = value * pi / 180
        a = round(x * cos(value) - y * sin(value))
        b = round(x * sin(value) + y * cos(value))
        self.location = int(a) + int(b) * 1j

    def turn(self, direction, value):
        if direction == 'L':
            value = -1 * value
        self.rotation(value)

    def forward(self, value):
        for _ in range(value):
            self.ship += self.location

    def calc_location(self):
        return abs(int(self.ship.imag)) + abs(int(self.ship.real))


def process_data(data):
    checker = re.compile(r'([NSEWLRF])(\d+)')
    instructions = []
    for row in data:
        action, value = checker.match(row).groups()
        value = int(value)
        instructions.append((action, value))
    return instructions


def get_answer(data, part2=False):

    instructions = process_data(data)
    if part2:
        actor = Waypoint()
    else:
        actor = Ship()
    for action, value in instructions:
        if action == 'F':
            actor.forward(value)
        elif action in ('L', 'R'):
            actor.turn(action, value)
        else:
            actor.move(action, value)
    if part2:
        print(actor.ship)
    else:
        print(actor.location)
    return actor.calc_location()

if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)

#     inputs = '''F10
# N3
# F7
# R90
# F11'''.split('\n')

    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
