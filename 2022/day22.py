from aoc_utilities import get_instructions
from pathlib import Path

TURNS = {'R': 1j, 'L': -1j}
FACINGS = {1: '>', 1j: 'v', -1: '<', -1j: '^'}
F = open('log_day22.txt', 'w')

def parse_instructions(data):
    grid = {}
    max_x = 0
    for y, row in enumerate(data, start=1):
        if row == '':
            break
        for x, val in enumerate(row, start=1):
            grid[x + 1j * y] = val
            if x > max_x:
                max_x = x

    grid_max = (max_x, y-1)
    distances = []
    turns = []
    val = ''
    for char in data[-1]:
        if not char.isdigit():
            turns.append(char)
            if val != '':
                distances.append(int(val))
                val = ''
        else:
            val += char
    if val != '':
        distances.append(int(val))
    return grid, grid_max, distances, turns


def wrap_around(grid, grid_max, pos, d):
    options = {1: 1 + 1j * pos.imag,
               -1: grid_max[0] + 1j * pos.imag,
               -1j: pos.real + 1j * grid_max[1],
               1j: pos.real + 1j}
    cur = options[d]
    c = 0
    m = max(grid_max)
    while True:
        c += 1
        if c > 2 * m:
            print(f'{options[d]}, ({pos}, {d}), {cur}')
            return
        if (cur not in grid) or (grid[cur] == ' '):
            cur += d
        elif grid[cur] in '.#':
            return cur

def _get_cube_loc(x, y):
    # there are 3 x areas that it is possible to be in
    if (1 <= x <= 50):
        return _get_cube_loc_y(y, '1')
    elif (51 <= x <= 100):
        return _get_cube_loc_y(y, '2')
    elif (101 <= x <= 150):
        return _get_cube_loc_y(y, '3')

def _get_cube_loc_y(y, x):
    # there are 4 y areas, that plus x give the facing
    if (1 <= y <= 50):
        return {'1': None, '2': 2, '3': 4}[x]
    elif (51 <= y <= 100):
        return {'1': None, '2': 1, '3': None}[x]
    elif (101 <= y <= 150):
        return {'1': 3, '2': 5, '3': None}[x]
    elif (151 <= y <= 200):
        return {'1': 6, '2': None, '3': None}[x]


def wrap_around_2(pos, d):
    prev = pos - d
    x, y = int(prev.real), int(prev.imag)
    # I hardcoded the relationships between the cube faces for my data
    # and the way I ordered them. unlike the example, i used standard
    # d6 convention where opposing sides sum to 7
    options = {
        # 1L -> 3T :: [51, 100] -> [1, 50]
        (-1, 1): (y - 50 + 101j, 1j),
        # 6L -> 2T :: [151, 200] -> [51, 100]
        (-1, 6): (y - 100 + 1j, 1j),
        # 1R -> 4B :: [51, 100] -> [101, 150]
        (1, 1): (y + 50 + 50j, -1j),
        # 6R -> 5B :: [151, 200] -> [51, 100]
        (1, 6): (y - 100 + 150j, -1j),
        # 2T -> 6L :: [51, 100] -> [151, 200]
        (-1j, 2): (1 + (x + 100)*1j, 1),
        # 3T -> 1L :: [1, 50] -> [51, 100]
        (-1j, 3): (51 + (x + 50)*1j, 1),
        # 4B -> 1R :: [101, 150] -> [51, 100]
        (1j, 4): (100 + (x - 50)*1j, -1),
        # 5B -> 6R :: [51, 100] -> [151, 200]
        (1j, 5): (50 + (x + 100)*1j, -1),

        # 4T -> 6B :: [101, 150] -> [1, 50]
        (-1j, 4): (x - 100 + 200j, -1j),
        # 6B -> 4T :: [1, 50] -> [101, 150]
        (1j, 6): (x + 100 + 1j, 1j),
        # 2L -> 3L :: [1, 50] -> [150, 101]
        (-1, 2): (1 + (151 - y)*1j, 1),
        # 3L -> 2L :: [101, 150] -> [50, 1]
        (-1, 3): (51 + (151 - y)*1j, 1),
        # 4R -> 5R :: [1, 50] -> [150, 101]
        (1, 4): (100 + (151 - y)*1j, -1),
        # 5R -> 4R :: [101, 150] -> [50, 1]
        (1, 5): (150 + (151 - y)*1j, -1),
    }

    face = _get_cube_loc(x, y)
    new_loc, new_d = options[d, face]
    return new_loc, new_d


def step(grid, grid_max, pos, d, part2=False):
    check = pos + d
    if (check not in grid) or (grid[check] not in '.#'):
        if part2:
            check, d = wrap_around_2(pos, d)
        else:
            check = wrap_around(grid, grid_max, pos, d)
    if grid[check] == '#':
        return False, d
    return check, d


def _get_start(grid, x=1, y=1):
    while True:
        c = (x + 1j * y)
        if c not in grid:
            y += 1
        elif grid[c] == ' ':
            x += 1
        elif grid[c] == '.':
            break
    return x + 1j * y


def run_map(grid, grid_max, distances, turns, part2=False):
    distances = iter(distances[:])
    turns = iter(turns[:])
    path = {}
    cur = _get_start(grid)
    d = 1
    steps = next(distances)
    turn = next(turns)
    c = 0
    last_step = False
    last_turn = False
    while (not last_step) or (not last_turn):
        c += 1
        if not c % 1000:
            print(c)
        if c > 5000:
            return
        for _ in range(steps):
            path[cur] = 'x'
            prev_d = d
            check, d = step(grid, grid_max, cur, d, part2)
            if check:
                path[cur] = FACINGS[prev_d]
                cur += d
                if cur != check:
                    cur = check
            else:
                d = prev_d
                break
        if not last_turn:
            d = d * TURNS[turn]
        try:
            steps = next(distances)
        except:
            last_step = True
            steps = 0
        try:
            turn = next(turns)
        except:
            last_turn = True

    path[cur] = 'X'

    return path, cur, d


def show_path(path, grid, grid_max, f=None, cubes=False,
              cur_step=None, cur_dir=None):
    if cur_step is not None:
        out = f'{(cur_step, cur_dir)}\n'
    else:
        out = ''
    for y in range(1, grid_max[1] + 1):
        if cubes:
            row = ''
        else:
            row = f'{y:3} '
        for x in range(1, grid_max[0] + 1):
            c = x + 1j * y
            if cubes:
                face = _get_cube_loc(x, y)
                if face is None:
                    face = ' '
                row += f'{face}'
                continue
            if c in path:
                row += path[c]
            elif c in grid:
                row += grid[c]
        if row.strip() == '':
            continue
        out += row
        out += '\n'
    if f is not None:
        f.write(out + '\n\n')
    else:
        print(out)



def get_answer(data, part2=False):
    grid, grid_max, distances, turns = parse_instructions(data)
    path, loc, d = run_map(grid, grid_max, distances, turns, part2)
    print(loc, d)
    row = loc.imag
    column = loc.real
    show_path(path, grid, grid_max, F)

    return int(1000 * row + 4 * column + {1: 0, 1j: 1, -1: 2, -1j: 3}[d])

if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''        ...#
#         .#..
#         #...
#         ....
# ...#.......#
# ........#...
# ..#....#....
# ..........#.
#         ...#....
#         .....#..
#         .#......
#         ......#.

# 10R5L5R10L4R5L5'''.split('\n')
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
    F.close()
