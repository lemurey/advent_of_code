from aoc_utilities import get_instructions
from pathlib import Path
from collections import deque

RED = '\033[91m'
YELLOW = '\033[97m'
END = '\033[0m'


DIRS = {'|': (-1j, 1j), '-': (-1, 1), 'L': (1j, 1), 'J': (1j, -1),
        '7': (-1, -1j), 'F': (1, -1j)}


def get_connections(p, grid):
    conn = []
    if p not in grid:
        return conn
    for d in (1j, -1j, 1, -1):
        c = p + d
        if c not in grid:
            continue
        if grid[c] not in DIRS:
            continue
        for d1 in DIRS[grid[c]]:
            if (c + d1) == p:
                conn.append(c)
    return conn


def decode_start(start, grid):
    conn = get_connections(start, grid)
    for k, v in DIRS.items():
        if ((start + v[0]) in conn) and ((start + v[1]) in conn):
            return k


def run_path(grid, start):
    Q = deque()
    seen = set()
    Q.append((start, {start: 0}))
    c = 0
    while Q:
        loc, path = Q.popleft()

        cur_length = len(path)

        if loc in seen:
            continue
        seen.add(loc)
        for d in DIRS[grid[loc]]:
            nl = loc + d
            if nl not in path:
                path[nl] = path[loc] + 1
                Q.append((nl, path))

        if len(path) == cur_length:
            return path

        c += 1
        if (c % 1000) == 0:
            print(f'at iter {c}, cur_length: {len(path)}')


def parse_grid(data):
    grid = {}
    for j, row in enumerate(data):
        for i, val in enumerate(row):
            c = i + -1j*j
            if val == 'S':
                start_val = c
            grid[c] = val
    grid[start_val] = decode_start(start_val, grid)
    return grid, start_val


def draw_grid(grid, path=None):
    out = ''
    max_x = max(int(x.real) for x in grid)
    max_y = abs(min([int(x.imag) for x in grid]))
    if path is None:
        path = {}

    for j in range(max_y + 1):
        for i in range(max_x + 1):
            c = i + -1j*j
            if grid[c] in ('O', 'I'):
                out += f'{RED}{grid[c]}{END}'
            elif grid[c] == '*':
                out += f'{YELLOW}{grid[c]}{END}'
            else:
                out += grid[c]
        out += '\n'
    return out


def get_exterior(grid, path, start, flip_labels=False):
    '''
    start at the start point and head down, every step check points on your right
    and your left, if its on your right its outside, if its on your left its inside
    any point we never check is outside by default
    if flip labels is true, reverse whether right/left is inside/outside
    '''
    # right turns are *-1j, left turns are *1j
    turns = {'F': {1j: -1j, -1: 1j},
             'L': {-1j: 1j, -1: -1j},
             '7': {1j: 1j, 1: -1j},
             'J': {1: 1j, -1j: -1j}}
    on_right = {1j: 1, -1j: -1, 1: -1j, -1: 1j}
    if flip_labels:
        labels = {1: 'I', -1: 'O'}
    else:
        labels = {1: 'O', -1: 'I'}
    # initialize with an unused character
    ng = {k: '*' for k in grid}

    cur = None
    count = 0
    while cur != start:
        if cur is None:
            cur = start
            d = -1j # start going down

        # take a step in direction of travel
        new = cur + d
        ng[new] = grid[new]
        if new not in path:
            print('something broke we got off the path')
            return ng
        # label the cells on your left/right
        for mod in (1, -1):
            check = new + mod * on_right[d]
            if check in grid:
                if check not in path:
                    ng[check] = labels[mod]
                else:
                    ng[check] = grid[check]
        # turn if necessary
        s = grid[new]
        if s in turns:
            d = d * turns[s][d]

        # if turning, check new right/left as well
        for mod in (1, -1):
            check = new + mod * on_right[d]
            if check in grid:
                if check not in path:
                    ng[check] = labels[mod]
                else:
                    ng[check] = grid[check]
        # update location for next loop
        cur = new

        count += 1
        if count > len(path):
            print("I didn't loop back properly")
            return ng

    # pass through each row and clean up missed cells
    max_x = max(int(x.real) for x in grid)
    max_y = abs(min([int(x.imag) for x in grid]))

    # hacky method to fill in gaps
    for j in range(max_y + 1):
        for i in range(1, max_x):
            c = i + -1j*j
            if ng[c] != '*':
                continue

            p = (i - 1) + -1j*j
            n = (i + 1) + -1j*j
            # if its next to an I label, continue it
            if ng[p] == 'I' or ng[n] == 'I':
                ng[c] = 'I'

    return ng


def get_answer(data, part2=False):
    grid, start = parse_grid(data)
    path = run_path(grid, start)

    # either right or left labeling is correct, its easy to see when you visualize
    # i used that to determine my grid needs rhs labeling
    ngr = get_exterior(grid, path, start)

    print(draw_grid(ngr, path))
    print()

    num_enclosed_r = sum(x == 'I' for x in ngr.values())

    return max(path.values()), num_enclosed_r


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)

    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))
