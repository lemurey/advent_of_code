from aoc_utilities import get_instructions
from utilities import timeit
import os
from collections import deque
import numpy as np

OFFSETS = ((-1, 0), (0, -1), (0, 1), (1, 0))



class colors:
    red = '\x1b[1;31;40m'
    blue = '\x1b[1;34;40m'
    yellow = '\x1b[1;33;40m'
    green = '\x1b[1;32;40m'
    white = '\x1b[1;37;40m'
    end = '\x1b[0m'

    @classmethod
    def color(cls, s, c='red'):
        if c == 'red':
            color = cls.red
        elif c == 'blue':
            color = cls.blue
        elif c == 'yellow':
            color = cls.yellow
        elif c == 'green':
            color = cls.green
        elif c == 'white':
            color = cls.white
        else:
            color = end
        return '{}{}{}'.format(color, s, cls.end)


class Monster(object):
    def __init__(self, x, y, t):
        self.hp = 200
        self.attack = 3
        self.x = x
        self.y = y
        self.type = t

    def move(self, y, x):
        self.y = y
        self.x = x

    def damage(self, n):
        self.hp -= n

    def select_target_loc(self, potentials):
        locations = {(x.y, x.x): x for x in potentials}
        potentials = []
        for y, x in OFFSETS:
            check = (self.y + y, self.x + x)
            if check in locations:
                potentials.append((locations[check].hp, check))
        if len(potentials) == 0:
            return None
        return min(potentials)[1]

    def __lt__(self, other):
        return (self.y, self.x) < (other.y, other.x)

    def __le__(self, other):
        return (self.y, self.x) <= (other.y, other.x)

    def __gt__(self, other):
        return (self.y, self.x) > (other.y, other.x)

    def __ge__(self, other):
        return (self.y, self.x) >= (other.y, other.x)

    def __eq__(self, other):
        if not isinstance(other, Monster):
            return False
        return ((self.y, self.x) == (other.y, other.x) and
                (self.hp == other.hp) and
                (self.type == other.type)
               )

    def __str__(self):
        if self.hp > 0:
            return self.type
        return '#'

    def __repr__(self):
        return '{} @ {},{} -- {}, {}'.format(self.type, self.y, self.x,
                                             self.hp, self.attack)


class Battle(object):
    def __init__(self, grid, e_start=3):
        self.grid = grid
        (self.max_d, self.points, self.max_x, self.max_y, self.combatants,
         self.invalids) = self.analyse_grid()

        if e_start > 3:
            for c in self.combatants:
                if c.type == 'E':
                    c.attack = e_start

        self.elves = [c for c in self.combatants if c.type == 'E']

        self.distances = {}

        self.end = False
        self.count = 0
        self.current = None

        self.show_hp = False
        self.show_count = False

    def analyse_grid(self):
        points = []
        combatants = []
        invalids = set()
        max_x = 0
        max_y = 0
        for (y, x), v in self.grid.items():
            if v != '#':
                points.append((y, x))
            else:
                invalids.add((y, x))
            if isinstance(v, Monster):
                combatants.append(v)
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y
        max_d = np.inf
        points = sorted(points)
        combatants = sorted(combatants)
        return max_d, points, max_x + 1, max_y + 1, combatants, invalids

    def run_full(self, early_stop=False):
        while not self.end:
            self.run_round()
            if early_stop:
                check = [c.hp <= 0 for c in self.elves]
                if any(check):
                    return
        if early_stop:
            check = [c.hp <= 0 for c in self.elves]
            if any(check):
                self.end = False
                return
        return self.close()

    def close(self):
        final_combatants = [c for c in self.combatants if c.hp > 0]
        print self.count, final_combatants
        return self.count * sum([c.hp for c in final_combatants])

    def run_round(self):
        for c in self.combatants:
            if c.hp <= 0:
                continue

            self.current = c

            targets = self.get_available_targets(c)
            if len(targets) == 0:
                # print self
                self.end = True
                self.current = None
                return

            locations = self.find_possible_locs(targets)
            do_move = self.run_combat(c, targets)

            if (len(locations) == 0) or (not do_move):
                continue

            y, x = self.find_movement(c, locations)
            self.do_move(c, y, x)
            self.run_combat(c, targets)
        self.current = None
        self.count += 1
        self.combatants = sorted([c for c in self.combatants if c.hp > 0])

    def run_combat(self, c, targets):
        loc = c.select_target_loc(targets)
        if loc is not None:
            target = self.grid[loc]
        else:
            return True

        target.damage(c.attack)
        if target.hp <= 0:
            target_loc = (target.y, target.x)
            # target.y = self.max_y + 5
            # target.x = self.max_x + 5
            self.grid[target_loc] = '.'
            self.distances = {}

        return False

    def get_available_targets(self, m):
        targets = []
        for c in self.combatants:
            if c.hp <= 0:
                continue
            if c.type != m.type:
                targets.append(c)
        return targets

    def find_possible_locs(self, targets):
        options = set()
        for c in targets:
            for (x, y) in OFFSETS:
                check = (c.y + y, c.x + x)
                if check not in self.grid:
                    continue
                if self.grid[check] == '.':
                    options.add(check)
        return options

    def find_movement(self, m, locations):
        start = (m.y, m.x)

        checks = []
        for end in locations:
            if (start, end) in self.distances:
                d = self.distances
            else:
                d = self._search(start, end)
            self.distances[(start, end)] = d
            self.distances[(end, start)] = d
            if d == np.inf:
                continue
            checks.append((d, end))

        if len(checks) == 0:
            return start
        loc = min(checks)[1]

        checks = []
        for (y, x) in OFFSETS:
            current = (start[0] + y, start[1] + x)
            if current not in self.grid:
                continue
            if self.grid[current] != '.':
                continue
            if (current, loc) in self.distances:
                d = self.distances[(current, loc)]
            else:
                d = self._search(current, loc)
            self.distances[(current, loc)] = d
            self.distances[(loc, current)] = d
            if d == np.inf:
                continue
            checks.append((d, current))

        if len(checks) == 0:
            return start
        return min(checks)[1]

    def _search(self, start, end):
        stack = deque()
        stack.append((start, 0))
        visited = set()
        while stack:
            cur, d = stack.popleft()
            if cur == end:
                return d
            for (x, y) in OFFSETS:
                neighbor = (cur[0] + y, cur[1] + x)
                if neighbor in visited:
                    continue
                visited.add(neighbor)
                if neighbor not in self.grid: # if location out of map
                    continue
                elif self.grid[neighbor] != '.':
                    continue
                elif neighbor == end: # if its the end of the path
                    return d + 1
                else:
                    stack.append((neighbor, d + 1))
        return np.inf

    def do_move(self, m, y, x):
        cur_spot = (m.y, m.x)
        self.grid[(cur_spot)] = '.'
        self.grid[(y, x)] = m
        m.move(y, x)
        if (y, x) != cur_spot:
            self.distances = {}

    def draw_path(self, path):
        out = ''
        if self.show_count:
            out += 'After {} rounds:\n'.format(self.count)
        for y in range(self.max_y):
            for x in range(self.max_x):
                if (y, x) not in self.grid:
                    continue
                val = self.grid[(y, x)]
                if ((y, x) in path) or (val == self.current):
                    color = 'red'
                elif isinstance(val, Monster):
                    color = 'blue'
                else:
                    color = 'white'
                if val == '#':
                    color = 'green'
                out += colors.color(val, color)
            if self.show_hp:
                out += '   '
                for c in self.combatants:
                    if c.hp <= 0:
                        continue
                    if c.y == y:
                        out += '{}({}), '.format(c.type, c.hp)
                out = out.rstrip(', ')
            out += '\n'

        return out

    def draw_distances(self, start, d=None):
        out = ''

        if d is None:
            d = self.monster_distances

        for y in range(self.max_y):
            for x in range(self.max_x):
                val = self.grid[(y, x)]
                if val == '#':
                    out += colors.color('  #  ', 'green')
                    continue
                if (y, x) == start:
                    out += colors.color('  {}  '.format(val), 'red')
                    continue
                dist = d[(start, (y, x))]
                val = ' {:0>3} '.format(dist)
                out += colors.color(val, 'white')
            out += '\n'
        return out

    def __str__(self):
        return self.draw_path(set())


def process_grid(data):
    grid = {}
    for y, line in enumerate(data):
        for x, entry in enumerate(line):
            if entry == 'E':
                grid[(y, x)] = Monster(x, y, 'E')
            elif entry == 'G':
                grid[(y, x)] = Monster(x, y, 'G')
            else:
                grid[(y, x)] = entry
    return grid


def get_answer(data, part2=False):

    if part2:
        e_start = 3
        while True:
            grid = process_grid(data)
            e_start += 1
            print 'trying combat power {}'.format(e_start)
            fight = Battle(grid, e_start)
            check = fight.run_full(early_stop=True)
            if all([c.hp > 0 for c in fight.elves]):
                # fight.show_hp = True
                # fight.show_count = True
                # print fight
                return fight.close()
    else:
        grid = process_grid(data)
        fight = Battle(grid)
        return fight.run_full()



if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))