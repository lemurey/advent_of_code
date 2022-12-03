from aoc_utilities import get_instructions
from pathlib import Path


class Grid:
    def __init__(self, data):
        self.grid = {}
        for j, line in enumerate(data):
            for i, val in enumerate(line):
                self.grid[i, j] = val

        self.max_y = max(x[1] for x in self.grid)
        self.max_x = max(x[0] for x in self.grid)

    def get_neighbors(self, i, j, which):

        if which == 'east':
            if i == self.max_x:
                return 0, j
            else:
                return i+1, j
        if which == 'south':
            if j == self.max_y:
                return i, 0
            else:
                return i, j+1

    def run_step(self):
        east_movers = []
        south_movers = []

        for i, j in self.grid:
            if self.grid[i, j] == '>':
                ni, nj = self.get_neighbors(i, j, 'east')
                if self.grid[ni, nj] == '.':
                    east_movers.append((i, j))


        for i, j in east_movers:
            self.grid[i, j] = '.'
            ni, nj = self.get_neighbors(i, j, 'east')
            self.grid[ni, nj] = '>'


        for i, j in self.grid:
            if self.grid[i, j] == 'v':
                ni, nj = self.get_neighbors(i, j, 'south')
                if self.grid[ni, nj] == '.':
                    south_movers.append((i, j))

        for i, j in south_movers:
            self.grid[i, j] = '.'
            ni, nj = self.get_neighbors(i, j, 'south')
            self.grid[ni, nj] = 'v'

        return len(east_movers) + len(south_movers)

    def __str__(self):
        out = ''
        for j in range(self.max_y + 1):
            for i in range(self.max_x + 1):
                out += str(self.grid[i, j])
            out += '\n'
        return out

def get_answer(data, part2=False):
    grid = Grid(data)

    num_movers = 1
    c = 0
    # print(grid)
    while num_movers > 0:
        c += 1
        num_movers = grid.run_step()
        # print(grid)
        # print(num_movers)
        # if c > 60:
        #     break

    return c



if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs='''v...>>.vv>
# .vv>>.vv..
# >>.>v>...v
# >>v>>.>.v.
# v>v.vv.v..
# >.>>..v...
# .vv..>.>v.
# v.v..>>v.v
# ....v..v.>'''.split('\n')
    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))
