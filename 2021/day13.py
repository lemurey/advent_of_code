from aoc_utilities import get_instructions
from pathlib import Path


def make_grid(data):
    grid = {}
    folds = []
    for line in data:
        if line.startswith('fold'):
            pre, val = line.split('=')
            val = int(val)
            if 'x' in pre:
                folds.append((fold_x, val))
            else:
                folds.append((fold_y, val))
        elif line == '':
            pass
        else:
            (i, j) = map(int, line.split(','))
            grid[i, j] = 1
    return grid, folds


def fold_y(grid, val):
    new_grid = {}
    for k, v in grid.items():
        (i, j) = k
        if j < val:
            new_grid[k] = v
        elif j > val:
            new_grid[i, (val - (j - val))] = 1
        else:
            print('THIS SHOULD NOT HAPPEN')
    return new_grid


def fold_x(grid, val):
    new_grid = {}
    for k, v in grid.items():
        (i, j) = k
        if i < val:
            new_grid[k] = v
        elif i > val:
            new_grid[(val - (i - val), j)] = 1
        else:
            print('THIS SHOULD NOT HAPPEN')
    return new_grid


def print_grid(grid):
    x_max = max([x for (x, y) in grid.keys()])
    y_max = max([y for (x, y) in grid.keys()])
    out = ''
    for y in range(y_max + 1):
        # out = ''
        for x in range(x_max + 1):
            if (x, y) in grid:
                out += '#'
            else:
                out += '.'
        out += '\n'
    print(out)


def get_answer(data, part2=False):
    grid, folds = make_grid(data)

    if part2:
        for fold, val in folds:
            grid = fold(grid, val)
        print_grid(grid)
    else:
        grid = folds[0][0](grid, folds[0][1])
        return sum(grid.values())


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''6,10
# 0,14
# 9,10
# 0,3
# 10,4
# 4,11
# 6,0
# 6,12
# 4,1
# 0,13
# 10,12
# 3,4
# 3,0
# 8,4
# 1,10
# 2,14
# 8,10
# 9,0

# fold along y=7
# fold along x=5'''.split('\n')
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
