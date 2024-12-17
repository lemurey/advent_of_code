from aoc_utilities import get_instructions
from pathlib import Path
from heapq import heappush, heappop

RED = '\033[91m'
END = '\033[0m'


def parse_grid(data):
    grid = {}
    for y, row in enumerate(data):
        for x, val in enumerate(row):
            p = (x, y)
            grid[p] = val
            if val == 'S':
                start = p
            if val == 'E':
                end = p
    return grid, start, end


def get_neighbors(state, grid):
    (cur_x, cur_y), (cur_fx, cur_fy) = state
    left_turn = (cur_fy, -cur_fx)
    right_turn = (-cur_fy, cur_fx)
    next_step = (cur_x + cur_fx, cur_y + cur_fy)
    yield 1000, ((cur_x, cur_y), left_turn)
    yield 1000, ((cur_x, cur_y), right_turn)
    if grid[next_step] != '#':
        yield 1, (next_step, (cur_fx, cur_fy))


def run_search(grid, start, end):
    costs = {}
    Q = []
    paths = {}
    first_state = (start, (1, 0))
    heappush(Q, (0, first_state))

    while Q:
        cost, state = heappop(Q)
        loc = state[0]
        if loc == end:
            break

        for score, next_state in get_neighbors(state, grid):
            # if we have seen this state before get it's cost
            # otherwise cost is infinity
            prev_cost = costs.get(next_state, float('inf'))
            next_cost = cost + score
            # have we found a cheaper way to get to here
            if next_cost < prev_cost:
                costs[next_state] = next_cost
                heappush(Q, (next_cost, next_state))
                # reset the path
                paths[next_state] = {state}
            # if we have found an alternate way to get to here
            elif next_cost == prev_cost:
                paths[next_state].add(state)
            # otherwise it was more expensive to get to here, do nothing

    def get_path(state):
        loc = state[0]
        if loc == start:
            yield [state]
            return
        for prev_state in paths[state]:
            for path in get_path(prev_state):
                yield path + [state]

    return cost, get_path(state)


def print_grid(grid, path=None, start=None, end=None):
    if path is None:
        locs = []
        dirs = []
    else:
        locs = [x[0] for x in path]
        dirs = [x[1] for x in path]
    r = {(1, 0): '>', (-1, 0): '<', (0, 1): 'v', (0, -1): '^'}
    max_x = int(max(x[0] for x in grid))
    max_y = int(max(y[1] for y in grid))
    out = ''
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            p = (x, y)
            if p in locs:
                if p in (start, end):
                    out += f'{RED}{grid[p]}{END}'
                else:
                    out += f'{RED}{r[dirs[locs.index(p)]]}{END}'
            else:
                out += str(grid[p])
        out += '\n'
    print(out)


def get_answer(data, part2=False):
    grid, start, end = parse_grid(data)

    if not part2:
        print_grid(grid)

    score, paths = run_search(grid, start, end)

    if part2:
        seats = set()
        for path in paths:
            for loc, _ in path:
                seats.add(loc)

        return len(seats)

    show_path = [x for x in paths][0]
    print_grid(grid, show_path, start, end)

    return score


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)

#     inputs = '''###############
# #.......#....E#
# #.#.###.#.###.#
# #.....#.#...#.#
# #.###.#####.#.#
# #.#.#.......#.#
# #.#.#####.###.#
# #...........#.#
# ###.#.#####.#.#
# #...#.....#.#.#
# #.#.#.###.#.#.#
# #.....#...#.#.#
# #.###.#.#.#.#.#
# #S..#.....#...#
# ###############'''.split('\n')

#     inputs = '''#################
# #...#...#...#..E#
# #.#.#.#.#.#.#.#.#
# #.#.#.#...#...#.#
# #.#.#.#.###.#.#.#
# #...#.#.#.....#.#
# #.#.#.#.#.#####.#
# #.#...#.#.#.....#
# #.#.#####.#.###.#
# #.#.#.......#...#
# #.#.###.#####.###
# #.#.#...#.....#.#
# #.#.#.#####.###.#
# #.#.#.........#.#
# #.#.#.#########.#
# #S#.............#
# #################'''.split('\n')

    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
