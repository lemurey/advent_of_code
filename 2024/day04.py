from aoc_utilities import get_instructions
from pathlib import Path


DIRS = (1+0j, -1+0j, 0+1j, 0-1j, 
        1+1j, 1-1j, -1+1j, -1-1j)


def parse_letters(data):
    grid = {}
    p = 0+0j
    for line in data:
        for letter in line:
            grid[p] = letter
            p += 1
        max_x = p.real
        p = 0 + (p.imag + 1)*1j
    max_y = p.imag
    return grid, int(max_x), int(max_y)


def check(grid, loc, outcomes, d=None, prev='X', history=None):
    checks = {'X': 'M', 'M': 'A', 'A': 'S'}

    if history is None:
        history = []
    # if we are at an S then we found XMAS and return the direction
    if prev == 'S':
        if history[0] not in outcomes:
            outcomes[history[0]] = []
        outcomes[history[0]].append(d)
        return None

    # if the location in the grid is not the current check lettter break out
    if grid[loc] != prev:
        return None

    # if no direction provided, check them all for next letter
    if d is None:
        to_check = []
        for cd in DIRS:
            nl = loc + cd
            if nl not in grid:
                continue
            if grid[nl] == checks[prev]:
                to_check.append(cd)
    else:
        to_check = [d]

    for cd in to_check:
        nl = loc + cd
        if nl not in grid:
            continue
        if grid[nl] == checks[prev]:
            check(grid, loc + cd, outcomes, cd, checks[prev], history + [loc])


def check_grid(grid, max_x, max_y, no_x=False):
    '''
    for part 1:
        check every starting letter, if we can find XMAS in a consistent direction
        log the start point and the direction, then make a set of (start, dir) and
        the length will be the number of XMAS words
    for part2:
        start with part1, but find all instances of MAS instead of XMAS
        then find all the As, and log where their M values are, but only if
        the M is diagonally adjacent to the A. Then find all cases where an A
        has adjacent M values with a distance of 2 from each other, those will
        be a cross. Add that A to a set, and the set's length will be the number
        of crossing MAS words
    '''
    words = set()
    holding = {}
    a_locs = {}
    if no_x:
        start = 'M'
    else:
        start = 'X'

    for y_val in range(max_y):
        for x_val in range(max_x):
            point = x_val + y_val * 1j
            if point not in grid:
                continue
            c = check(grid, point, holding, prev=start)

    for k, v in holding.items():
        for entry in v:
            words.add((k, entry))
            if (entry.real == 0) or (entry.imag == 0):
                continue
            if k+entry not in a_locs:
                a_locs[k+entry] = []
            a_locs[k+entry].append(k)

    if no_x:
        words = set()
        for k, v in a_locs.items():
            if len(v) == 1:
                continue
            for c1 in v:
                for c2 in v:
                    c = c1 - c2
                    if abs(c1.real - c2.real) + abs(c1.imag - c2.imag) == 2:
                        words.add(k)
    return words


def print_grid(grid, max_x, max_y):
    out = ''
    for y_val in range(max_y):
        for x_val in range(max_x):
            point = x_val + y_val * 1j
            if point not in grid:
                continue
            out += grid[point]
        out += '\n'
    print(out)


def get_answer(data, part2=False):
    grid, max_x, max_y = parse_letters(data)
    # print_grid(grid, max_x, max_y)
    words = check_grid(grid, max_x, max_y, part2)

    return len(words)

if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''MMMSXXMASM
# MSAMXMSMSA
# AMXSXMAAMM
# MSAMASMSMX
# XMASAMXAMM
# XXAMMXXAMA
# SMSMSASXSS
# SAXAMASAAA
# MAMMMXMMMM
# MXMXAXMASX'''.split('\n')
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
