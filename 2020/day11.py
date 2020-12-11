from aoc_utilities import get_instructions
from pathlib import Path


DIRECTIONS = ((0, 1), (0, -1), (1, 0), (-1, 0),
              (1, 1), (-1, -1), (1, -1), (-1, 1))


def parse_input(data):
    grid = {}
    for j, row in enumerate(data):
        for i, val in enumerate(row):
            grid[i, j] = val
    return grid


def get_neighbors1(grid, i, j):
    for x, y in DIRECTIONS:
        nx = i + x
        ny = j + y
        if (nx, ny) in grid:
            yield grid[nx, ny]


def get_neighbors2(grid, i, j):
    num_occupied = 0
    for x, y in DIRECTIONS:
        spot = '.'
        v = 1
        while spot == '.':
            nx = v * x + i
            ny = v * y + j
            if (nx, ny) not in grid:
                break
            spot = grid[nx, ny]
            v += 1
        yield spot


def rules(grid, i, j, func=get_neighbors1, count=4):
    if grid[i, j] == '.':
        return '.'

    num_occupied = 0
    for state in func(grid, i, j):
        if state == '#':
            num_occupied += 1

    if grid[i, j] == 'L' and num_occupied == 0:
        return '#'
    if grid[i, j] == '#' and num_occupied >= count:
        return 'L'
    return grid[i, j]


def run_game(grid, func=get_neighbors1, count=4):
    new_grid = {}
    for i, j in grid:
        new_grid[i, j] = rules(grid, i, j, func, count)
    return new_grid


def show_grid(grid):
    c = 0
    row = ''
    for i, j in sorted(grid, key=lambda x: x[1]):
        if j == c:
            row += grid[i, j]
        else:
            c +=1
            print(row)
            row = grid[i, j]
    print()


def get_answer(data, part2=False):
    grid = parse_input(data)
    rounds = 0

    which = {True: get_neighbors2, False: get_neighbors1}
    val = {True: 5, False: 4}

    verbose = False

    while True:
        rounds += 1
        if verbose:
            show_grid(grid)
        next_grid = run_game(grid, which[part2], val[part2])
        if next_grid == grid:
            print(rounds)
            return sum([1 if v == '#' else 0 for v in grid.values()])
        grid = next_grid


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''L.LL.LL.LL
# LLLLLLL.LL
# L.L.L..L..
# LLLL.LL.LL
# L.LL.LL.LL
# L.LLLLL.LL
# ..L.L.....
# LLLLLLLLLL
# L.LLLLLL.L
# L.LLLLL.LL'''.split('\n')
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
