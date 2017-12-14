from aoc_utilities import get_instructions
from collections import deque
from day10 import knothash
import os


class Defrag:
    def __init__(self, data, max_ind=127):
        self.grid = make_grid(data, max_ind + 1)
        self.max_ind = max_ind
        self.regions = {}
        self.q = deque()
        self.cur_region = 1
        self.regionized = False

    def _neighbors(self, row, col):
        if col < self.max_ind:
            yield row, col + 1
        if col > 0:
            yield row, col - 1
        if row > 0:
            yield row - 1, col
        if row < self.max_ind:
            yield row + 1, col

    def _zero_process(self, row, col):
        for neighbor in self._neighbors(row, col):
            if neighbor not in self.regions:
                self.q.append(neighbor)

    def _one_process(self, row, col):
        for n_row, n_col in self._neighbors(row, col):
            if (n_row, n_col) in self.regions:
                continue
            if self.grid[n_row][n_col] == 0:
                self.regions[(n_row, n_col)] = -1
                self._zero_process(n_row, n_col)
                continue
            self.regions[(n_row, n_col)] = self.cur_region
            self._one_process(n_row, n_col)

    def regionize(self):
        if self.regionized:
            return self.cur_region
        self.q.append((0, 0))
        while self.q:
            row, col = self.q.popleft()
            if (row, col) in self.regions:
                continue
            if self.grid[row][col] == 0:
                self.regions[(row, col)] = -1
                self._zero_process(row, col)
                continue
            self.regions[(row, col)] = self.cur_region
            self._one_process(row, col)
            self.cur_region += 1
        self.cur_region -= 1
        self.regionized = True
        return self.cur_region


def process_row(seed, row, max_size):
    hex_val = knothash('{}-{}'.format(seed, row))
    bin_string = '{value:0>{size}}'.format(size=max_size,
                                           value=bin(int(hex_val, 16))[2:])
    return list(map(int, bin_string))


def make_grid(data, max_size=128):
    grid = []
    for row_num in range(max_size):
        grid.append(process_row(data, row_num, max_size))
    return grid


def get_answer(data, part2=False):
    d = Defrag(data)
    print(sum([sum(x) for x in d.grid]))
    return d.regionize()


if __name__ == '__main__':
    day = int(os.path.basename(__file__).split('.')[0].split('y')[1])
    inputs = get_instructions(day)
    # print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
