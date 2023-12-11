from aoc_utilities import get_instructions
from pathlib import Path


def parse_grid(data):
    grid = {}
    galaxies = []
    expanders = []

    for j, row in enumerate(data):
        if all(x == '.' for x in row):
            expanders.append(f'r{j}')

    for xv in range(len(row)):
        column = [data[yv][xv] for yv in range(j+1)]
        if all (y == '.' for y in column):
            expanders.append(f'c{xv}')
    nd = []
    for j, row in enumerate(data):
        nr = []
        for i, val in enumerate(row):
            if f'c{i}' in expanders:
                nr.append('.')
            nr.append(val)

        nd.append(nr)
        if f'r{j}' in expanders:
            nd.append(nr)
    for j, row in enumerate(nd):
        for i, val in enumerate(row):
            c = i - 1j*j
            grid[c] = val
            if val == '#':
                galaxies.append(c)

    return grid, galaxies


def get_galaxies(data, expansion=2):
    galaxies = []
    expanders = []

    for j, row in enumerate(data):
        if all(x == '.' for x in row):
            expanders.append(f'r{j}')

    for xv in range(len(row)):
        column = [data[yv][xv] for yv in range(j+1)]
        if all (y == '.' for y in column):
            expanders.append(f'c{xv}')

    xc, yc = 0, 0
    for j, row in enumerate(data):
        for i, val in enumerate(row):
            if f'c{i}' in expanders:
                xc += expansion - 1
            if val == '#':
                galaxies.append(xc -1j*yc)
            xc += 1
        yc += 1
        if f'r{j}' in expanders:
            yc += expansion - 1
        xc = 0
    return galaxies


def md(x, y):
    return abs(x.real - y.real) + abs(x.imag - y.imag)


def get_answer(data, part2=False):
    galaxies = get_galaxies(data)
    if part2:
        galaxies = get_galaxies(data, 1000000)
    total = 0
    for i, g1 in enumerate(galaxies):
        for g2 in galaxies[i:]:
            if g1 == g2:
                continue
            step = md(g1, g2)
            total += step

    return total


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''...#......
# .......#..
# #.........
# ..........
# ......#...
# .#........
# .........#
# ..........
# .......#..
# #...#.....'''.split('\n')
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
