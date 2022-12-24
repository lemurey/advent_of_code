from aoc_utilities import get_instructions
from pathlib import Path
from collections import deque


BD = {'>': (1, 0), 'v': (0, 1), '<': (-1, 0), '^': (0, -1)}
R = {(1, 0): '>', (0, 1): 'v', (-1, 0): '<', (0, -1): '^', (0, 0): 'w'}

class Blizzard:
    def __init__(self, loc, move, max_size=None):
        self.loc = loc
        self.icon = move
        self.move = BD[move]
        self.max_size = max_size

    def set_max_size(self, max_size):
        self.max_size = max_size

    def __call__(self):
        x = self.loc[0] + self.move[0]
        y = self.loc[1] + self.move[1]
        if x == 0: # send x position to max - 1
            x = self.max_size[0] - 1
        if y == 0: # send y position to max - 1
            y = self.max_size[1] - 1
        if x == self.max_size[0]:
            x = 1
        if y == self.max_size[1]:
            y =  1
        self.loc = (x, y)

    def __hash__(self):
        return hash(self.loc)

    def __eq__(self, other):
        if isinstance(other, Blizzard):
            return (self.loc == self.loc)
        elif isinstance(other, (tuple, list)):
            return self.loc[0] == other[0] and self.loc[1] ==  other[1]
        return False


def parse_instructions(data):
    blizzards = []
    max_x, max_y  = 0, 0
    for j, row in enumerate(data):
        if j > max_y:
            max_y = j
        for i, val in enumerate(row):
            if val not in '#.':
                b = Blizzard((i, j), val)
                blizzards.append(b)
            if i > max_x:
                max_x = i

    for b in blizzards:
        b.set_max_size((max_x, max_y))

    return blizzards, max_x, max_y


def get_blizzard_states(blizzards, n=30):
    blizzard_set = [blizzards]
    for _ in range(n):
        b = [Blizzard(bb.loc, bb.icon, bb.max_size) for bb in blizzard_set[-1]]
        for blizzard in b:
            blizzard()
        blizzard_set.append(b)

    output = []
    for b in blizzard_set:
        output.append(set([bb.loc for bb in b]))
    return output


def get_neighbors(loc, t, end, start=(0, 1)):
    max_x = max(end[0] + 1, start[0] + 1)
    max_y = max(end[1], start[1])
    for dx, dy in BD.values():
        nx, ny = loc[0] + dx, loc[1] + dy
        if (nx, ny) == end:
            yield (nx, ny)
        if (nx, ny) == start:
            yield (nx, ny)
        if (nx >= max_x) or (ny >= max_y):
            continue
        if (nx <= 0) or (ny <= 0):
            continue
        yield (nx, ny)
    # forgot about the wait state
    yield loc


def get_path(blizzards, end, start=(1, 0), reverse=False,
             start_time=0, n=30, blizzard_set=None):

    if reverse:
        start, end  = end, start
    locations = {start}
    time = start_time
    seen = set()

    # generate blizzards up to time n
    if blizzard_set is None:
        blizzard_set = get_blizzard_states(blizzards, n)
    else:
        n = len(blizzard_set)
    while True:
        # double size of pre-computed blizzard locs if we get to that time
        if time >= len(blizzard_set) - 1:
            n += n
            blizzard_set = get_blizzard_states(blizzards, n)
            print(len(blizzard_set), time)

        new_locs = set()
        for loc in locations:

            for nl in get_neighbors(loc, time, end, start=start):
                new_locs.add(nl)

        valid_locs = set()
        for loc in new_locs:
            if loc not in blizzard_set[time + 1]:
                valid_locs.add(loc)

        time += 1
        if end in new_locs:
            return time

        locations = valid_locs

        if not time % 50:
            print('at iteration: ', time, len(locations))


def show_blizzards(blizzards, p=None, f=None):
    grid = {}
    for b in blizzards:
        if b.loc not in grid:
            grid[b.loc] = b.icon
        elif isinstance(grid[b.loc], str):
            grid[b.loc] = 2
        else:
            grid[b.loc] += 1
    x, y = b.max_size

    out = ''
    for j in range(y):
        for i in range(x):
            if j == 0:
                if i == 1:
                    char = '.'
                else:
                    char = '#'
            elif i == 0:
                char = '#'
            elif (i, j) in grid:
                char = str(grid[(i, j)])
            else:
                char = '.'
            if (i, j) == p:
                char = 'E'
            out += char
        out += '#\n'

    out += '#' * (x - 1) + '.#'
    if f is not None:
        f.write(out)
    else:
        print(out)


def get_answer(data, part2=False):
    blizzards, max_x, max_y = parse_instructions(data)
    bsets = get_blizzard_states(blizzards, 1000)
    end = (max_x - 1, max_y)
    start = (1, 0)
    time = get_path(blizzards, end, blizzard_set=bsets)
    print(time)
    time_back = get_path(blizzards, end=end, start=start, start_time=time,
                         reverse=True, blizzard_set=bsets)
    time_again = get_path(blizzards, end=end, start=start,
                          start_time=time_back, blizzard_set=bsets)

    return time_again


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''#.######
# #>>.<^<#
# #.<..<<#
# #>v.><>#
# #<^v^^>#
# ######.#'''.split('\n')
    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))
