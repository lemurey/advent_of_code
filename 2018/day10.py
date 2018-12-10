from aoc_utilities import get_instructions
import os
import re
import numpy as np

SPLITTER=re.compile(r'-?\d+')


class Point(object):
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def update(self):
        self.x += self.vx
        self.y += self.vy

    def backup(self):
        self.x -= self.vx
        self.y -= self.vy

    def __repr__(self):
        return '#'


class Grid(object):
    def __init__(self, positions, velocities):
        points = []
        grid = set()
        min_x = positions[0][0]
        min_y = positions[0][1]
        max_x = positions[0][1]
        max_y = positions[0][1]
        for (x, y), (vx, vy) in zip(positions, velocities):
            p = Point(x, y, vx, vy)
            points.append(p)
            grid.add((p.x, p.y))
            if x < min_x:
                min_x = x
            if x > max_x:
                max_x = x
            if y < min_y:
                min_y = y
            if y > max_y:
                max_y = y
        self.grid = grid
        self.points = points
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.area = self._get_area()
        self.min_area_time = 0
        self.i = 0

    def _get_area(self):
        return ((self.max_x - self.min_x) *
                (self.max_y - self.min_y))

    def backup(self):
        grid = set()
        min_x = self.points[0].x
        min_y = self.points[0].y
        max_x = self.points[0].x
        max_y = self.points[0].y
        for p in self.points:
            p.backup()
            grid.add((p.x, p.y))
            if p.x < min_x:
                min_x = p.x
            if p.x > max_x:
                max_x = p.x
            if p.y < min_y:
                min_y = p.y
            if p.y > max_y:
                max_y = p.y
        self.grid = grid
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y


    def update(self):
        self.i += 1
        grid = set()
        min_x = self.points[0].x
        min_y = self.points[0].y
        max_x = self.points[0].x
        max_y = self.points[0].y

        for p in self.points:
            p.update()
            grid.add((p.x, p.y))
            if p.x < min_x:
                min_x = p.x
            if p.x > max_x:
                max_x = p.x
            if p.y < min_y:
                min_y = p.y
            if p.y > max_y:
                max_y = p.y

        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y

        check = self._get_area()
        if check < self.area:
            self.min_area_time = self.i
        self.area = check
        self.grid = grid

    def __contains__(self, other):
        x, y = other
        if (x, y) in self.grid:
            return True
        else:
            return False

    def show(self):
        for yi in range(self.min_y, self.max_y + 1):
            for xi in range(self.min_x, self.max_x + 1):
                if (xi, yi) in self:
                    print '#',
                else:
                    print '.',
            print


def make_grid(data):
    grid = []
    velocities =[]
    for line in data:
        x, y, vx, vy = map(int, SPLITTER.findall(line))
        grid.append([x, y])
        velocities.append([vx, vy])
    g = Grid(grid, velocities)
    return g


def get_answer(data, part2=False):
    grid = make_grid(data)
    prev = grid.area
    num_grow = 0
    while True:
        grid.update()
        cur = grid.area
        if cur > prev:
            break
        prev = cur
    grid.backup()
    grid.show()
    return grid.min_area_time


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))