from aoc_utilities import get_instructions
import os
from day15 import colors


class Ground(object):
    def __init__(self, comp):
        self.clay = comp
        self.min_x = min(comp, key=lambda x:x[1])[1]
        self.min_y = min(comp, key=lambda x:x[0])[0]
        self.max_x = max(comp, key=lambda x:x[1])[1]
        self.max_y = max(comp, key=lambda x:x[0])[0]

        self.flowing = set()
        self.settled = set()

    def flow(self, point):
        stack = set()
        stack.add(point)
        while stack:
            # grab point, save original coordinates for later
            p = stack.pop()
            y, x = p

            # drop down to clay or settled water
            while not ((p  in self.clay) or (p in self.settled)):
                if y > self.max_y:
                    break
                self.flowing.add(p)
                y += 1
                p = (y, x)

            # do not keep going forever
            if y > self.max_y:
                continue

            # if we are in clay or settled water jump up a level
            if p in self.clay or p in self.settled:
                y -= 1
                p = (y, x)

            fall = False

            while not fall:
                # spread flowing water
                left, right = self.flow_right_left(p)
                # check for falls
                below_left = (left[0] + 1, left[1])
                if (below_left not in self.clay and left not in self.clay):
                    self.flow_right_left(left)
                    stack.add(left)
                    fall = True

                below_right = (right[0] + 1, right[1])
                if (below_right not in self.clay) and (right not in self.clay):
                    self.flow_right_left(right)
                    stack.add(right)
                    fall = True

                if not fall:
                    self.spread_stable(p)
                    (y, x) = p
                    y -= 1
                    p = (y, x)

    def flow_right_left(self, p):
        left = self.flow_out(p, -1)
        right = self.flow_out(p, 1)
        return left, right

    def flow_out(self, point, d):
        y, x = point
        below_over = (y + 1, x + d)
        over = (y, x + d)
        while self._is_flowable(below_over) and over not in self.clay:
            self.flowing.add(over)
            x += d
            below_over = (y + 1, x + d)
            over = (y, x + d)
        return over

    def stable_over(self, point, d):
        y, x = point
        self.settled.add(point)
        over = (y, x + d)
        while over not in self.clay and over in self.flowing:
            self.settled.add(over)
            over = (y, over[1] + d)

    def spread_stable(self, point):
        self.stable_over(point, -1)
        self.stable_over(point, 1)

    def _is_flowable(self, point):
        return (point in self.clay) or (point in self.settled)

    def draw_highlight(self, highlights=None, color=True):
        if highlights is None:
            highlights = []
        out = ''
        for y in range(0, self.max_y + 1):
            for x in range(self.min_x - 2, self.max_x + 3):
                if (y, x) == (0, 500):
                    val = '+'
                elif (y, x) in self.settled:
                    val = '~'
                elif (y, x) in self.flowing:
                    val = '|'
                elif (y, x) in self.clay:
                    val = '#'
                else:
                    val = '.'

                if (y, x) in highlights:
                    if color:
                        out += colors.color(val)
                    else:
                        out += '*'
                else:
                    out += val
            out += '\n'
        return out.strip('\n')

    def __str__(self):
        return self.draw_highlight([])

    def write_out(self, path, highlights=None, color=True):
        if highlights is None:
            highlights = []
        out = self.draw_highlight(highlights, color=color)
        with open(path, 'w') as f:
            f.write(out)

    def get_sum(self, part2=True):
        total = 0
        grid = self.draw_highlight()
        if part2:
            return len(self.settled)
        for i, line in enumerate(grid.split('\n')):
            if (i < self.min_y) or (i > self.max_y):
                continue
            for entry in line:
                if entry == '|':
                    total += 1
                elif entry == '~':
                    total += 1
        return total


def process_data(data):
    output = set()
    for line in data:
        vals = {}
        for entry in line.split(','):
            entry = entry.strip()
            which, check = entry.split('=')
            if '..' in check:
                start, end = map(int, check.split('..'))
                vals[which] = range(start, end + 1)
            else:
                vals[which] = [int(check)]
        if len(vals['x']) == 1:
            x = vals['x'][0]
            for entry in vals['y']:
                output.add((entry, x))
        else:
            y = vals['y'][0]
            for entry in vals['x']:
                output.add((y, entry))
    return output


def get_answer(data, part2=False):
    scan = process_data(data)
    g = Ground(scan)
    g.flow((1, 500))
    g.write_out('day17_part1.cw')
    return g.get_sum(part2)


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
