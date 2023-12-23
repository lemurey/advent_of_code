from aoc_utilities import get_instructions
from pathlib import Path


def brick_id():
    id_num = 1
    while True:
        yield id_num
        id_num += 1


class Brick():
    def __init__(self, x1, y1, z1, x2, y2, z2, id_num):
        self.x1 = min(x1, x2)
        self.x2 = max(x1, x2)
        self.y1 = min(y1, y2)
        self.y2 = max(y1, y2)
        self.z1 = min(z1, z2)
        self.z2 = max(z1, z2)
        self.locked = False
        self.id_num = id_num

    def drop(self):
        self.z1 -= 1
        self.z2 -= 1

    def footprint(self):
        for x in range(self.x1, self.x2 + 1):
            for y in range(self.y1, self.y2 + 1):
                yield x, y

    def full_brick(self):
        for z in range(self.z1, self.z2 + 1):
            for (x, y) in self.footprint():
                yield x, y, z

    def check_support(self, prev):
        for x, y in self.footprint():
            if (x, y) in prev:
                yield prev[x, y]
        return False

    def __repr__(self):
        return str(self.id_num)

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if not isinstance(other, Brick):
            return False
        return self.id_num == other.id_num

    def __hash__(self):
        return hash(self.id_num)

class Board():
    def __init__(self, bricks):
        self.bricks = bricks
        self._get_zrange()
        self._init_grid()

    def _init_grid(self):
        base_grid = {z: {} for z in self.z_range}
        max_x, max_y = 0, 0
        for b in self.bricks:
            for x, y in b.footprint():
                if x > max_x:
                    max_x = x
                if y > max_y:
                    max_y = y
                for z in range(b.z1, b.z2+1):
                    base_grid[z][x, y] = b
        self.grid = base_grid
        self.max_x = max_x
        self.max_y = max_y
        for brick in self.grid[1].values():
            brick.locked = True

    def _get_zrange(self):
        min_z = 100000000
        max_z = 0
        for b in self.bricks:
            if b.z1 < min_z:
                min_z = b.z1
            if b.z1 > max_z:
                max_z = b.z2
        self.z_range = list(range(min_z, max_z + 1))

    def drop(self):
        any_drops = False
        seen = set()
        for z in self.z_range:
            if z == 1: # don't check bricks on ground level
                continue
            grid = self.grid[z]
            prev_grid = self.grid[z - 1]
            dropped_bricks = set()
            for brick in grid.values():
                if brick.z1 == 1: # if brick is at ground level, lock it
                    brick.locked = True
                if brick.locked: # if brick is locked, don't check
                    continue
                if brick in seen: # no brick can drop more than once per iteration
                    continue
                seen.add(brick)
                drop_brick = True
                for s in brick.check_support(prev_grid):
                    if s.locked:
                        brick.locked = True
                    drop_brick = False
                if drop_brick:
                    any_drops = True
                    dropped_bricks.add(brick)
            for brick in dropped_bricks:
                # remove the brick from every grid spot it is in and add it to the one below
                for x, y, z1 in brick.full_brick():
                    if (x, y) in self.grid[z1]:
                        del self.grid[z1][x, y]
                        self.grid[z1-1][x, y] = brick
                brick.drop()
        return any_drops

    def __getitem__(self, key):
        return self.grid[key]


def get_bricks(data):
    bricks = []
    id_gen = brick_id()
    for line in data:
        p = [int(y) for x in line.split('~') for y in x.split(',')]
        bricks.append(Brick(*p, next(id_gen)))
    return bricks


def show_grid(board, view):
    if view == 'x':
        r1 = list(range(board.max_x + 1))
        r2 = list(range(board.max_y + 1))
    else:
        r1 = list(range(board.max_y + 1))
        r2 = list(range(board.max_x + 1))
    out = ''
    for k in sorted(board.grid)[::-1]:
        cur = ''
        grid = board.grid[k]
        for c1 in r1:
            for c2 in r2:
                if view == 'x':
                    c = (c1, c2)
                else:
                    c = (c2, c1)
                if c in grid:
                    break
            else:
                cur += '.'
                continue
            cur += 'X'
        if all(c == '.' for c in cur):
            continue
        out += f'{cur} {k}\n'
    return out


def vertical_view(board, z_index):
    grid = board[z_index]
    out = ''
    for y in range(board.max_y + 1):
        row = []
        for x in range(board.max_x + 1):
            if (x, y) in grid:
                row.append(f'{grid[x, y].id_num:04}')
            else:
                row.append('....')

        out += f'{"|".join(x for x in row)}\n'
    return out


def get_answer(data, part2=False):
    bricks = get_bricks(data)
    board = Board(bricks)

    # drop bricks until no more bricks can drop
    to_drop = True
    while to_drop:
        to_drop = board.drop()

    # check every brick, and get the set of bricks it rests on
    cannot_disentigrate = set()
    supported = {}
    for b in board.bricks:
        supported[b] = set()
        if b.z1 == 1:
            continue
        prev = board[b.z1 - 1]
        for s in b.check_support(prev):
            supported[b].add(s)

    # visualize the whole stack layer by layer
    with open('board_slices.txt', 'w') as f:
        for z_val in sorted(board.grid)[::-1]:
            view = vertical_view(board, z_val)
            if all(x in '.|\n' for x in view):
                continue
            f.write(f'{z_val}\n')
            f.write(vertical_view(board, z_val))

    # if any brick rests on only 1 brick, then that brick cannot be deleted
    for v in supported.values():
        if len(v) == 1:
            cannot_disentigrate = cannot_disentigrate.union(v)

    # part 1 answer
    print(len([x for x in bricks if x not in cannot_disentigrate]))

    # invert the supported dictionary to get a bricks direct supports
    supports = {}
    for k, v in supported.items():
        for entry in v:
            if entry not in supports:
                supports[entry] = set()
            supports[entry].add(k)

    # find the chain of falls from removing a brick
    all_falls = 0
    for brick in bricks:
        new_removes = [brick]
        will_fall = set(new_removes)
        prev = -1
        while len(will_fall) > prev:
            prev = len(will_fall)
            next_removes = set()
            for r in new_removes:
                if r not in supports:
                    continue
                for e in supports[r]:
                    if will_fall.intersection(supported[e]) == supported[e]:
                        next_removes.add(e)
            will_fall = will_fall.union(next_removes)
            new_removes = next_removes
        will_fall.remove(brick)
        all_falls += len(will_fall)

    return all_falls


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''1,0,1~1,2,1
# 0,0,2~2,0,2
# 0,2,3~2,2,3
# 0,0,4~0,2,4
# 2,0,5~2,2,5
# 0,1,6~2,1,6
# 1,1,8~1,1,9'''.split('\n')
    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))
