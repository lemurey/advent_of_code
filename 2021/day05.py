from aoc_utilities import get_instructions
from pathlib import Path
from operator import add, sub


def get_lines(x1, y1, x2, y2):
    if x1 < x2:
        x_op = add
    elif x2 < x1:
        x_op = sub
    else:
        x_op = lambda a, _: a
    if y1 < y2:
        y_op = add
    elif y2 < y1:
        y_op = sub
    else:
        y_op = lambda a, _: a

    x, y = x1, y1
    yield x, y
    while (x, y) != (x2, y2):
        x = x_op(x, 1)
        y = y_op(y, 1)
        yield x, y


def make_grid(data):
    grid = {}
    big_grid = {}
    for row in data:
        (x1, y1), (x2, y2) = [map(int, x.split(',')) for x in row.split(' -> ')]

        for x, y in get_lines(x1, y1, x2, y2):
            if (x, y) not in grid:
                grid[(x, y)] = 0
            if (x, y) not in big_grid:
                big_grid[(x, y)] = 0
            if x1 == x2 or y1 == y2:
                grid[(x, y)] += 1
            big_grid[(x, y)] += 1

    return grid, big_grid


def get_answer(data, part2=False):
    grid, big_grid = make_grid(data)
    if part2:
        grid = big_grid
    count = 0
    for val in grid.values():
        if val > 1:
            count += 1
    return count


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
