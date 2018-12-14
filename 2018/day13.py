from aoc_utilities import get_instructions
import os
import sys

def parse_map(data):
    grid = {}
    carts = {}
    n = 0
    cd = {'<': '-', '>': '-', '^': '|', 'v': '|'}
    for j, line in enumerate(data):
        for i, entry in enumerate(line):
            if entry in '<>^v':
                carts[(i, j)] = (n, entry, 0)
                n += 1
                grid[(i, j)] = cd[entry]
            # elif entry in '/\\':
            #     fixes = {'/': }
            #     grid[(i, j)] =
            else:
                grid[(i, j)] = entry
    return grid, carts


def draw_grid(grid, carts, max_x, max_y, as_file=True):
    if as_file:
        f = open('test.txt', 'w')
    else:
        f = sys.stdout
    for j in range(max_y):
        for i in range(max_x):
            if (i, j) in carts:
                f.write(carts[(i, j)][1])
            elif (i, j) in grid:
                f.write(grid[(i, j)])
        f.write('\n')
    if as_file:
        f.close()
    else:
        f.write('\n')


def turn_cart(cart, index):
    turns = {('<', 0): 'v', ('<', 1): '<', ('<', 2): '^',
             ('>', 0): '^', ('>', 1): '>', ('>', 2): 'v',
             ('v', 0): '>', ('v', 1): 'v', ('v', 2): '<',
             ('^', 0): '<', ('^', 1): '^', ('^', 2): '>',
             ('<', '/'): 'v', ('>', '/'): '^',
             ('v', '/'): '<', ('^', '/'): '>',
             ('<', '\\'): '^', ('>', '\\'): 'v',
             ('v', '\\'): '>', ('^', '\\'): '<',
            }
    return turns[(cart, index)]


def check_collision(x, y, n, carts, new_carts):
    if (x, y) in carts:
        nc = carts[(x, y)][0]


def run_carts(grid, carts, part1):
    outcomes = {'<': (-1, 0), '>': (1, 0), 'v': (0, 1), '^': (0, -1)}
    new_carts = {}
    trail = set()
    to_remove = []
    for (x, y) in sorted(carts, key=lambda x: (x[1], x[0])):
        if (x, y) in to_remove:
            continue
        n, cart, index = carts[(x, y)]
        new_cart = cart
        new_index = index
        if grid[(x, y)] == '+':
            new_cart = turn_cart(cart, index)
            new_index = (index + 1) % 3
        elif grid[(x, y)] in '/\\':
            new_cart = turn_cart(cart, grid[(x, y)])
        dx, dy = outcomes[new_cart]
        new_x = x + dx
        new_y = y + dy
        if ((((new_x, new_y) in carts) and ((new_x, new_y) not in trail)) or
            ((new_x, new_y) in new_carts)):
            if part1:
                return new_x, new_y
            else:
                to_remove.append((new_x, new_y))
        else:
            trail.add((x, y))
        new_carts[(new_x, new_y)] = (n, new_cart, new_index)
        for tr in to_remove:
            if tr in new_carts:
                del new_carts[tr]
    return new_carts


def get_answer(data, part2=False):
    grid, carts = parse_map(data)
    max_x = max(grid, key=lambda x: x[0])[0] + 1
    max_y = max(grid, key=lambda x: x[1])[1] + 1
    c = 0
    while True:
        carts = run_carts(grid, carts, not part2)
        if (len(carts) <= 2) and part2:
            return carts
        elif isinstance(carts, tuple):
            return carts
        c += 1
        if c % 1000 == 0:
            print 'at iteration: {}'.format(c)


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
