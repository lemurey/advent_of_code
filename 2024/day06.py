from aoc_utilities import get_instructions
from pathlib import Path
from day04 import print_grid


def make_grid(data):
    grid = {}
    for y, row in enumerate(data):
        for x, val in enumerate(row):
            p = x + y*1j
            if val == '^':
                guard = p
            grid[p] = val
            max_x = x + 1
        max_y = y + 1
    return grid, guard, max_x, max_y


def run_part1(grid, guard):
    facing = -1j
    path = set()
    while True:
        # if the same position and facing have already happened we are in a loop
        if (guard, facing) in path:
            return path, True
        path.add((guard, facing))
        next_point = guard + facing
        # if the guard moves off the grid we are done
        if next_point not in grid:
            return path, False
        if grid[next_point] == '#':
            facing = facing * 1j
            continue
        guard = next_point


def run_part2(grid, guard, max_x, max_y):
    paths = []
    for y in range(max_y):
        print(f'at row {y}')
        for x in range(max_x):
            O = x + y * 1j
            if O == guard: # this is important
                continue
            new_grid = {k:v for k, v in grid.items()}
            new_grid[O] = '#'
            path, is_loop = run_part1(new_grid, guard)
            if is_loop:
                paths.append((path, O))
    return paths


def get_answer(data, part2=False):
    grid, guard, max_x, max_y = make_grid(data)
    if part2:
        paths = run_part2(grid, guard, max_x, max_y)

        # for path, obst in paths:
        #     new_grid = {k:v for k, v in grid.items()}
        #     new_grid[obst] = 'O'
        #     lines = {-1j: '|', 1j: '|', 1: '-', -1: '-'}
        #     for point, facing in path:
        #         if point == guard:
        #             continue
        #         if new_grid[point] in '|-':
        #             new_grid[point] = '+'
        #         else:
        #             new_grid[point] = lines[facing]
        #     print_grid(new_grid, max_x, max_y)
        #     print()

        return len(paths)
    else:
        path, _ = run_part1(grid, guard)

    # for point, dir in path:
    #     grid[point] = 'X'
    # print_grid(grid, max_x, max_y)

    return len(set(x for x, y in path))


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''....#.....
# .........#
# ..........
# ..#.......
# .......#..
# ..........
# .#..^.....
# ........#.
# #.........
# ......#...'''.split('\n')
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
