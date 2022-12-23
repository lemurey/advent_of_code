from aoc_utilities import get_instructions
from pathlib import Path
from operator import lt, gt

OFFSETS = [(0, 1), (0, -1), (1, 0), (-1, 0),
           (1, 1), (1, -1), (-1, 1), (-1, -1)]

D_TO_L = {(0, -1): 'N', (1, 0): 'E', (0, 1): 'S', (-1, 0): 'W',
          (1, -1): 'NE', (-1, -1): 'NW', (-1, 1): 'SW', (1, 1): 'SE'}

LABELS = {'N': (0, -1), 'E': (1, 0), 'S': (0, 1), 'W': (-1, 0),
          'NE': (1, -1), 'NW': (-1, -1), 'SW': (-1, 1), 'SE': (1, 1)}

BASE_DIRS = 'NSWE'

DIR_OPTIONS = {'N': {LABELS['N'], LABELS['NE'], LABELS['NW']},
               'S': {LABELS['S'], LABELS['SE'], LABELS['SW']},
               'W': {LABELS['W'], LABELS['NW'], LABELS['SW']},
               'E': {LABELS['E'], LABELS['NE'], LABELS['SE']}}

F = open('log_day23.txt', 'w')

def parse_instructions(data):
    elves = set()
    for y, row in enumerate(data):
        for x, val in enumerate(row):
            if val == '#':
                elves.add((x, y))
    return elves


def get_neighbors(x, y, checks=OFFSETS):
    for dx, dy in checks:
        yield x + dx, y + dy


def run_one_sim(elves, dirs):
    can_move = set()
    for elf in elves:
        if any(n in elves for n in get_neighbors(*elf)):
            can_move.add(elf)
    proposals = {}
    # part 1
    for elf in can_move:
        for d in dirs:
            if all(n not in elves for n in get_neighbors(*elf, DIR_OPTIONS[d])):
                nx, ny = elf[0] + LABELS[d][0], elf[1] + LABELS[d][1]
                if (nx, ny) not in proposals:
                    proposals[(nx, ny)] = []
                proposals[(nx, ny)].append(elf)
                break

    # part 2
    to_move = set()
    new_locs = set()
    for new_loc, elf_list in proposals.items():
        if len(elf_list) > 1:
            continue
        new_locs.add(new_loc)
        to_move.add(elf_list[0])
    # remove existing elves that will move
    elves -= to_move
    # add moved elves back in
    elves |= new_locs

    return elves, len(to_move)


def _get_extreme(grid, op):
    mx, my = 0, 0
    for (x, y) in grid:
        if op(x, mx):
            mx = x
        if op(y, my):
            my = y
    return mx, my


def show_grid(grid, f=None):
    lx, ly = _get_extreme(grid, lt)
    hx, hy = _get_extreme(grid, gt)
    out = ''
    for y in range(ly, hy + 1):
        for x in range(lx, hx + 1):
            if (x,y) not in grid:
                out += '.'
            else:
                out += '#'
        out += '\n'
    if f is not None:
        f.write(f'{out}\n')
        f.write('\n')
    else:
        print(out)


def score_grid(grid):
    lx, ly = _get_extreme(grid, lt)
    hx, hy = _get_extreme(grid, gt)
    return (hx - lx + 1) * (hy - ly + 1) - len(grid)


def get_answer(data, part2=False):
    elves = parse_instructions(data)

    show_grid(elves, F)
    ds = BASE_DIRS
    c = 0
    num_moved = 1
    while num_moved != 0:
        elves, num_moved = run_one_sim(elves, ds)
        c += 1
        if c == 10:
            print(f'score at round 10: {score_grid(elves)}')
        if not c % 100:
            print(f'at round: {c}')
        ds = ds[1:] + ds[0]
    show_grid(elves, f=F)
    return c


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''.....
# ..##.
# ..#..
# .....
# ..##.
# .....'''.split('\n')
#     inputs = '''....#..
# ..###.#
# #...#.#
# .#...##
# #.###..
# ##.#.##
# .#..#..'''.split('\n')
    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))
    F.close()
