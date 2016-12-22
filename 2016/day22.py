from utilities import timeit
from collections import deque
import os, sys, time

def parse_instructions(instructions):
    output = {}
    for line in instructions.split('\n'):
        if line[0] != '/':
            continue
        name, size, used, avail, _ = line.split()
        x, y = name.split('-')[1:]
        x = int(x[1:])
        y = int(y[1:])
        size = int(size[:-1])
        used = int(used[:-1])
        avail = int(avail[:-1])
        output[(x, y)] = {'size': size, 'used': used, 'avail' : avail}
    return output


def find_available_pairs(data):
    s = sorted(data.items(), key=lambda x: -x[1]['avail'])
    b = s[0][1]['avail']
    m = s[0][1]['avail']
    count = 0
    for entry in s:
        if entry[1]['used'] <= b and entry[1]['used'] != 0:
            count += 1
    return count, m


class DataGrid(object):
    def __init__(self, data, empty, goal, max_val, animate=False):
        self.data = data
        self.empty = empty
        self.goal = goal
        self.max_val = max_val
        self.moves = 0
        self.animate = animate
        self.argmin = lambda x, y: x if x[1] < y[1] else y
        self.dirs = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        self.wall_dir = None
        self.pass_wall_dir = None

    def _add_nodes(self, n1, n2):
        return n1[0] + n2[0], n1[1] + n2[1]

    def _single_move(self, step, sleep=0.1):
        start = self.empty
        swap = self._add_nodes(start, step)
        if self.max_val < self.data[swap]['used']:
            return 'invalid move'
        if swap == self.goal:
            self.goal = self.empty
        self.data[swap], self.data[start] = self.data[start], self.data[swap]
        self.empty = swap
        self.moves += 1
        if self.animate:
            self.print_grid(sleep)

    def _run_rotation(self):
        while self.empty != (0, 0):
            for step in [(1, 0), (0, 1), (-1, 0), (-1, 0), (0, -1)]:
                self._single_move(step, sleep=0.03)
        self._single_move((1, 0))
        return self.moves

    def _navigate_wall(self):
        self._find_wall()
        wall = self._add_nodes(self.empty, self.wall_dir)
        while self.data[wall]['used'] > self.max_val:
            self._single_move(self.pass_wall_dir)
            wall = self._add_nodes(self.empty, self.wall_dir)
        return self.navigate_path()

    def _find_wall(self):
        for step in self.dirs:
            test = self._add_nodes(self.empty, step)
            if self.data[test]['used'] > self.max_val:
                self.dirs.remove(step)
                self.wall_dir = step
                if step[0]:
                    self.dirs.remove((-step[0], 0))
                else:
                    self.dirs.remove((0, -step[1]))
                break
        self._find_wall_end()

    def _find_wall_end(self):
        start = self._add_nodes(self.empty, self.wall_dir)
        prev = [start, start]
        distances = [0, 0]
        while True:
            stop_searching = 0
            for i, s in enumerate(self.dirs):
                last_step = prev[i]
                dist = distances[i]
                next_step = self._add_nodes(last_step, s)
                if next_step in self.data:
                    if self.data[next_step]['used'] > self.max_val:
                        prev[i] = next_step
                        distances[i] = dist + 1
                    else:
                        stop_searching += 1
                elif dist != 100:
                    distances[i] = 100
                else:
                    stop_searching += 1

            if stop_searching == 2:
                index = reduce(self.argmin, enumerate(distances))[0]
                self.pass_wall_dir = self.dirs[index]
                return

    def navigate_path(self):
        while True:
            if self.empty[1] > self.goal[1]:
                r = self._single_move((0, -1))
            elif self.empty[0] < self.goal[0] - 1:
                r = self._single_move((1, 0))
            else:
                return self._run_rotation()
            if r:
                return self._navigate_wall()

    def print_grid(self, sleep):
        f_line = ('{}  ' * 28).strip() + '\n'
        f = sorted(self.data.items(), key=lambda x: (x[0][0], x[0][1]))
        output = ''
        if self.animate:
            os.system('clear')
        prev_index = -1
        for entry, contents in f:
            index, _ = entry
            if index > prev_index:
                prev_index = index
                row = []
            if contents['used'] == 0:
                row.append('_')
            elif contents['used'] > 85:
                row.append('#')
            elif index == self.goal[0] and len(row) == self.goal[1]:
                row.append('G')
            else:
                row.append('.')
            if len(row) == 28:
                output += f_line.format(*row)
        sys.stdout.write(output)
        sys.stdout.flush()
        time.sleep(sleep)


@timeit
def get_results(instructions, part2=False):
    data = parse_instructions(instructions)
    count, max_val = find_available_pairs(data)
    
    if part2:
        grid = DataGrid(data, (22, 25), (36, 0), max_val, animate=True)
        return grid.navigate_path()
    else:
        return count


if __name__ == '__main__':
    with open('instructions_day22.txt', 'r') as f:
        instructions = f.read().strip()
    print get_results(instructions, part2=False)
    print get_results(instructions, part2=True)
