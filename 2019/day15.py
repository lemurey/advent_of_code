from aoc_utilities import get_instructions
import os
from intcode import Intcode
from collections import deque


class Robot:
    def __init__(self, program):
        self.core = Intcode([x for x in program], input=0, mode='robot')
        self.position = 0
        self.directions = {1: 1j,
                           2: -1j,
                           3: -1,
                           4: 1}

    def single_step(self, direction):
        self.core.secondary = direction
        self.core.waiting = False
        val_1 = self.core.run()
        if val_1 == -1:
            raise Exception('core halted')

        location = self.position + self.directions[direction]
        if val_1 != 0:
            self.position = location

        return location, val_1

    def step(self, direction, grid):
        location, val_1 = self.single_step(direction)
        if val_1 == 2:
            grid[location] = 'O'
        elif val_1 == 1:
            grid[location] = '.'
        else:
            grid[location] = '#'

        return location, grid


def get_grid_bounds(grid):
    min_y = int(min(grid, key=lambda x: x.imag).imag)
    max_y = int(max(grid, key=lambda x: x.imag).imag)
    min_x = int(min(grid, key=lambda x: x.real).real)
    max_x = int(max(grid, key=lambda x: x.real).real)
    return min_y, max_y, min_x, max_x


def grid_iterator(grid):
    min_y, max_y, min_x, max_x = get_grid_bounds(grid)
    for y in reversed(range(min_y, max_y + 1)):
        for x in range(min_x, max_x + 1):
            yield x, y


def check_grid(grid):
    for x, y in grid_iterator(grid):
        position = x + y*1j
        if position not in grid:
            breaking = False
            for direction in (1j, -1j, -1, 1):
                if position + direction not in grid:
                    continue
                if grid[position + direction] == '#':
                    continue
                breaking = True
            if breaking:
                return False
    return True


def get_complete_map(program):
    robot = Robot(program)
    grid = {0: '.'}
    cur_d = 1j
    dirs = {1j: 1, -1j: 2, -1: 3, 1: 4}
    iters = 0
    while True:
        for _ in range(50):
            iters += 1
            new_loc, grid = robot.step(dirs[cur_d], grid)
            if grid[new_loc] == '#':
                cur_d *= -1j
            else:
                cur_d *= 1j
        if check_grid(grid):
            show_grid(grid)
            print(iters)
            return grid


def find_end_point(grid):
    for x, y in grid_iterator(grid):
        position = x + y*1j
        if position not in grid:
            continue
        if grid[position] == 'O':
            return position


def backtrack(full_grid, check=0, start=None):
    if start is None:
        end_point = find_end_point(full_grid)
    else:
        end_point = start
    paths = {end_point: []}
    Q = deque([end_point])
    while Q:
        loc = Q.popleft()
        if loc == check:
            return paths[loc]

        for d in (1j, -1j, -1, 1):
            new_loc = loc + d
            if (new_loc in paths) or (full_grid[new_loc] == '#'):
                continue
            paths[new_loc] = paths[loc] + [d]
            Q.append(new_loc)
    return


def show_grid(grid):
    min_y, max_y, min_x, max_x = get_grid_bounds(grid)
    for y in reversed(range(min_y, max_y + 1)):
        row = ''
        for x in range(min_x, max_x + 1):
            position = x + y*1j
            if position in grid:
                row += grid[position]
            else:
                row += ' '
        print(row)
    return


def fill_with_o(grid, end_point):
    new = {k: v for k, v in grid.items()}

    to_remove = [end_point]

    minutes = 0
    iters = 0
    while len(to_remove) != 0:
        iters += 1
        if iters % 10000 == 0:
            show_grid(new)
            return
        tc = to_remove[:]
        add_minute = False
        for cur_point in tc:
            to_remove.remove(cur_point)
            for d in (1j, -1j, -1, 1):
                new_loc = cur_point + d
                if new_loc not in new:
                    continue
                if new[new_loc] == '.':
                    add_minute = True
                    new[new_loc] = 'O'
                    to_remove.append(new_loc)
        if add_minute:
            minutes += 1
    return minutes, new


def get_answer(data):
    program = list(map(int, data[0].split(',')))
    grid = get_complete_map(program)
    end_point = find_end_point(grid)
    path = backtrack(grid, start=end_point)
    print(len(path))
    t, ng = fill_with_o(grid, end_point)
    print(t)


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
    inputs = get_instructions(year, day)
    get_answer(inputs)
