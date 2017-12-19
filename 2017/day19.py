from aoc_utilities import get_instructions
import os
from collections import deque


class Network:

    def __init__(self, grid):
        self.grid = grid

    def _get(self, postion):
        x, y = int(postion.real), int(postion.imag)
        if not (0 <= x < len(self.grid)):
            return None
        if not (0 <= y < len(self.grid[0])):
            return None
        return self.grid[x][y]

    def __getitem__(self, key):
        if isinstance(key, complex):
            return self._get(key)
        elif isinstance(key, tuple):
            return self._get(complex(*key))
        else:
            msg = 'only keys that are complex or tuple allowed'
            raise NotImplementedError(msg)

    def _neighbors(self, node, direction):
        if self[node + direction]:
            yield node + direction, direction
        for turn in [1j, -1j]:
            if self[node + turn * direction]:
                yield node + turn * direction, turn * direction

        yield node, None

    def _find_start(self):
        for i, char in enumerate(self.grid[0]):
            if char:
                return complex(0, i)

    def follow_path(self, animate=False):
        node = self._find_start()
        self.visited = set()
        seen = []
        direction = 1
        steps = 1
        self.end = None
        iterations = 0
        while True:
            self.visited.add(node)
            if animate:
                f_name = '../images/animate_map_{:0>5}.html'.format(steps)
                with open(f_name, 'w') as f:
                    to_write = self.print_map()
                    f.write(to_write)
                print('finished file {}'.format(f_name))
            for node, direction in self._neighbors(node, direction):
                if direction is None:
                    self.end = node
                    return ''.join(seen), steps
                if self[node].isalpha():
                    seen.append(self[node])
                steps += 1
                break

    def print_map(self):

        c_pre = '<span style="color:#FF0000">'
        c_end = '</span>'
        c_e_pre = '<span style="color:#00FF00">'
        o_string = '<pre style="word-wrap: break-word; white-space: pre-wrap;"><p>\n'
        for i, row in enumerate(self.grid):
            for j, char in enumerate(row):
                node = complex(i, j)
                if node == self.end:
                    o_string += (c_e_pre + char + c_end)
                elif node in self.visited:
                    o_string += (c_pre + char + c_end)
                elif char == '':
                    o_string += ' '
                else:
                    o_string += char
            o_string += '\n'
        o_string += '</p>'
        return o_string


def make_grid(data):
    max_len = 0
    for i, line in enumerate(data.split('\n')):
        if len(line) > max_len:
            max_len = len(line)
    grid = [['' for _ in range(max_len)] for _ in range(i + 1)]
    i = 0
    j = 0
    for char in data:
        if char == '\n':
            i += 1
            j = 0
            continue
        if char != ' ':
            grid[i][j] = char
        j += 1

    return grid


def get_answer(data, part2=False):
    grid = make_grid(data)
    n = Network(grid)
    chars, length = n.follow_path(animate=True)
    if part2:
        return length
    return chars


if __name__ == '__main__':
    day = int(os.path.basename(__file__).split('.')[0].split('y')[1])
    inputs = get_instructions(day)
    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))
