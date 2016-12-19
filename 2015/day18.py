from time import time

class Lights(object):
    def __init__(self, data, height=100, width=100, part2=False):
        self.grid = [[0 for _ in range(width + 2)] for __ in range(height + 2)]
        self.part2 = part2
        self._populate_grid(data)

    def _populate_grid(self, data):
        for i, row in enumerate(data.split('\n'), 1):
            for j, val in enumerate(row, 1):
                self.grid[i][j] = 1 if val == '#' else 0
        if self.part2:
            self._set_corners()

    def _set_corners(self):
        self.grid[1][1]   = 1
        self.grid[-2][-2] = 1
        self.grid[1][-2]  = 1
        self.grid[-2][1]  = 1

    def _get_neighbors(self, i, j):
        value = 0
        for row in self.grid[i - 1:i + 2]:
            value += sum(row[j - 1:j + 2])
        return value

    def __call__(self):
        replace = self.grid[:]
        for i, row in enumerate(self.grid[1:-1], 1):
            new_row = row[:]
            for j, val in enumerate(row[1:-1], 1):
                neighbors = self._get_neighbors(i, j)
                if neighbors == 3 or (neighbors == 4 and val):
                    new_row[j] = 1
                else:
                    new_row[j] = 0
            replace[i] = new_row
        self.grid = replace
        if self.part2:
            self._set_corners()

    def sum(self):
        output = 0
        for row in self.grid:
            output += sum(row)
        return output

    def print_grid(self):
        for row in self.grid[1:-1]:
            print ''.join('#' if x else '.' for x in row[1:-1])


def timeit(function):
    def timed(*args, **kwargs):
        s_t = time()
        result = function(*args, **kwargs)
        e_t = time()
        out = '{} {} took {:.2f} sec'
        print out.format(function.__name__, kwargs, e_t - s_t)
        return result
    return timed


@timeit
def get_results(instructions, part2=False):
    grid = Lights(instructions, part2=part2)
    for _ in xrange(100):
        grid()
    return grid.sum()


if __name__ == '__main__':
    with open('instructions_day18.txt', 'r') as f:
        instructions = f.read().strip()
    print get_results(instructions, part2=False)
    print get_results(instructions, part2=True)