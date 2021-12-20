from aoc_utilities import get_instructions
from pathlib import Path


def get_grid(data):
    grid = {}
    enhancer = data[0]
    lookup = {'.': 0, '#': 1}
    for j, row in enumerate(data[2:]):
        for i, val in enumerate(row):
            grid[(i, j)] = lookup[val]
    return grid, enhancer


def get_neighbors(grid, i, j, flip):
    for index in ((i - 1, j - 1), (i, j - 1), (i + 1, j - 1),
                  (i - 1, j), (i, j), (i + 1, j),
                  (i - 1, j + 1), (i, j + 1), (i + 1, j + 1)):
        if index in grid:
            yield grid[index]
        else:
            if flip:
                yield 1
            else:
                yield 0


def get_max_min(grid):
    max_x = 0
    max_y = 0
    min_x = 0
    min_y = 0
    for (i, j) in grid:
        if i < min_x:
            min_x = i
        if j < min_y:
            min_y = j
        if i > max_x:
            max_x = i
        if j > max_y:
            max_y = j
    return min_x, max_x, min_y, max_y



def enhance(grid, enhancer, num_iters=0):
    new_grid = {}
    lookup = {'.': 0, '#': 1}
    min_x, max_x, min_y, max_y = get_max_min(grid)

    if (enhancer[0] == '#') and (num_iters % 2 == 1):
        flip = True
    else:
        flip = False

    for j in range(min_y - 3, max_y + 4):
        for i in range(min_x - 3, max_x + 4):
            b = ''
            for neighbor in get_neighbors(grid, i, j, flip):
                b += str(neighbor)
            val = int(b, 2)
            new_val = lookup[enhancer[val]]
            new_grid[(i, j)] = new_val
    return new_grid


def print_grid(grid, to_file=False):
    min_x, max_x, min_y, max_y = get_max_min(grid)

    lookup = {0: '.', 1: '#'}
    out = ''
    for j in range(min_y - 3, max_y + 4):
        for i in range(min_x - 3, max_x + 4):
            if (i, j) not in grid:
                out += '.'
            else:
                out += lookup[grid[(i, j)]]
        out += '\n'
    if to_file:
        with open(to_file, 'a') as f:
            f.write(out)
            f.write('\n')
    else:
        print(out)

def get_answer(data, part2=False):
    grid, enhancer = get_grid(data)

    with open('check_20.txt', 'w') as f:
        pass

    to_iterate = 2
    if part2:
        to_iterate = 50

    for i in range(to_iterate):
        # print_grid(grid, 'check_20.txt')
        grid = enhance(grid, enhancer, i)
        # print_grid(grid, 'check_20.txt')
        # grid = enhance(grid, enhancer, 1)
        # print_grid(grid, 'check_20.txt')

    return sum(grid.values())


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

# #..#.
# #....
# ##..#
# ..#..
# ..###'''.split('\n')
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
