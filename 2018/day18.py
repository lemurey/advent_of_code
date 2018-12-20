from aoc_utilities import get_instructions
import os
from day15 import colors


class Square(object):
    def __init__(self, x, y, t):
        self.location = complex(x, y)
        self.type = t

    def __add__(self, other):
        if isinstance(other, Square):
            return self.location + other.location
        elif isinstance(other, complex):
            return self.location + other
        elif isinstance(other, tuple):
            return self.location + other[0] + other[1] * 1j

    def __radd__(self, other):
        if isinstance(other, (Square, complex, tuple)):
            return self.__add__(other)

    def __str__(self):
        return self.type


class Grid(object):
    def __init__(self, grid):
        self.grid = grid

    def sum_up(self):
        t_sum = 0
        l_sum = 0
        for row in self.grid:
            for entry in row:
                if entry.type == '|':
                    t_sum += 1
                elif entry.type == '#':
                    l_sum += 1
        return t_sum, l_sum

    def __str__(self):
        out = ''
        for row in self.grid:
            for entry in row:
                out += str(entry)
            out += '\n'
        return out


class GameOfTrees(object):
    def __init__(self, grid):
        self.grid = grid

    def get_sub_grid(self, start_y, start_x):
        sub_grid = []
        for y in range(-1, 2):
            sub_row = []
            for x in range(-1, 2):
                yp = start_y + y
                xp = start_x + x
                c = self.grid[start_y][start_x] + (x, y)
                if xp < 0 or yp < 0:
                    continue
                if (xp, yp) == (start_x, start_y):
                    continue
                if yp >= len(self.grid):
                    continue
                elif xp >= len(self.grid[0]):
                    continue
                sub_row.append(self.grid[yp][xp])
            sub_grid.append(sub_row)
        return Grid(sub_grid)

    def find_cycles(self):
        num_stable = 0
        cycles = 0
        self.values = [self.value()]

        while cycles < 50:
            self.run_round()
            cycles += 1
            self.values.append(self.value())

        while True:
            last_50 = self.values[-50:]
            prev = set(last_50)
            self.run_round()
            cycles += 1
            self.values.append(self.value())
            last_50 = self.values[-50:]
            cur = set(last_50)
            if prev == cur:
                num_stable += 1
            else:
                num_stable = 0
            if num_stable > len(cur):
                break

            if cycles % 100 == 0:
                print 'at cycle: {}'.format(cycles)
        print 'found stable cycle in {} iterations'.format(cycles)
        return cur

    def run_game(self, n_rounds, show=False):
        n = len(str(n_rounds))
        d = []
        with open('game_of_trees.log', 'w') as f:
            f.write('{round:0>{n}}: {score}\n'.format(round=0, n=n,
                    score=self.value()))
            for i in range(n_rounds):
                self.run_round()
                if show:
                    print self.draw(wc=True)
                    print i
                v = self.value()
                f.write('{round:0>{n}}: {s}\n'.format(round=i + 1, n=n, s=v))
                d.append(v)
        return d

    def run_round(self, show=False):
        new_grid = []
        if isinstance(show, tuple):
            print_sub = True
        else:
            print_sub = False

        for y, row in enumerate(self.grid):
            new_row = []
            for x, entry in enumerate(row):
                if show:
                    if not print_sub:
                        show = (x, y)

                new = self.update(x, y, show)
                if (x, y) == show:
                    print new
                new_row.append(Square(x, y, new))
            new_grid.append(new_row)
        self.grid = new_grid

    def update(self, x, y, show):
        grid = self.get_sub_grid(y, x)
        if show == (x, y):
            print grid
        t_sum, l_sum = grid.sum_up()
        cur = self.grid[y][x]
        if cur.type == '.':
            if t_sum > 2:
                return '|'
            else:
                return '.'
        if cur.type == '|':
            if l_sum > 2:
                return '#'
            else:
                return '|'
        if cur.type == '#':
            if t_sum > 0 and l_sum > 0:
                return '#'
        return '.'

    def value(self):
        temp = Grid(self.grid)
        t, l = temp.sum_up()
        return t * l

    def draw(self, wc=False):
        out = ''
        cmap = {'|': 'green', '#': 'red', '.': 'white'}
        for row in self.grid:
            for entry in row:
                if wc:
                    c = str(entry)
                    out += colors.color(c, cmap[c])
                else:
                    out += str(entry)
            out += '\n'
        return out.strip('\n')

    def __str__(self):
        return self.draw()


def process_data(data):
    grid = []
    for j, line in enumerate(data):
        row = []
        for i, entry in enumerate(line):
            row.append(Square(i, j, entry))
        grid.append(row)
    return grid



'''
184920 is too low
202648 is too high
'''



def get_answer(data, part2=False):
    grid = process_data(data)
    game = GameOfTrees(grid)
    if part2:
        total_runs = 1000000000
        # test_runs = 800
        # start_checks = 600
        # if 'game_of_trees.log' in os.listdir('.'):
        #     vals = []
        #     with open('game_of_trees.log', 'r') as f:
        #         for line in f:
        #             vals.append(int(line.split(': ')[1]))
        # else:
        #     vals = game.run_game(test_runs, show=False)


        # stationary_set = set(vals[600:test_runs])
        # sl = len(stationary_set)
        # print 'stationary cycle found: {} '.format(sl)
        stationary_set = game.find_cycles()
        start_checks = len(game.values) - 50

        ordered = []
        for val in stationary_set:
            ind = game.values[start_checks:].index(val)
            ordered.append((ind + start_checks, val))

        ordered_stationary = [x[1] for x in sorted(ordered)]

        to_grab = total_runs - start_checks
        index = to_grab  % sl
        return ordered_stationary[index]
    else:
        game.run_game(10)
        return game.value()


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
#     sample = '''.#.#...|#.
# .....#|##|
# .|..|...#.
# ..|#.....#
# #.#|||#|#|
# ...#.||...
# .|....|...
# ||...#|.#|
# |.||||..|.
# ...#.|..|.'''.split('\n')
#     print get_answer(sample)
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))