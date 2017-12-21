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

    def follow_path(self):
        node = self._find_start()
        self.visited = set()
        seen = []
        direction = 1
        steps = 1
        self.end = None
        iterations = 0
        while True:
            self.visited.add(node)
            for node, direction in self._neighbors(node, direction):
                if direction is None:
                    self.end = node
                    return ''.join(seen), steps
                if self[node].isalpha():
                    seen.append(self[node])
                steps += 1
                break


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
    chars, length = n.follow_path()
    if part2:
        return length
    return chars


if __name__ == '__main__':
    day = int(os.path.basename(__file__).split('.')[0].split('y')[1])
    inputs = get_instructions(day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
