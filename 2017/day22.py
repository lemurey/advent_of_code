from aoc_utilities import get_instructions
from utilities import timeit
import os


'''
wake up:
    - if current node is infected:
        - turns right
    - else:
        - turns left
    - if current node is clean:
        - infect node
    else:
        - clean node
    - move forward one step


'''


class Worm:
    def __init__(self, nodes, part2=False):
        self.direction = 1j
        self.node = complex(0, 0)
        self.infected = set()
        self.weakend = set()
        self.flagged = set()
        self.cause_infection = 0
        self.evolved = part2
        self._set_infection_status(nodes)

    def _set_infection_status(self, nodes):
        grid = []
        for i, line in enumerate(nodes.split('\n')):
            row = []
            for j, char in enumerate(line):
                if char == '#':
                    row.append(1)
                else:
                    row.append(0)
            grid.append(row)
        width = j + 1
        hieght = i + 1
        center_x, center_y = width // 2, hieght // 2
        for i, row in enumerate(grid):
            for j, entry in enumerate(row):
                x_pos = j - center_x
                y_pos = center_y - i
                if entry:
                    self.infected.add(complex(x_pos, y_pos))

    def verion1(self):
        if self.node in self.infected:
            self.direction *= -1j
            self.infected.remove(self.node)
        else:
            self.direction *= 1j
            self.infected.add(self.node)
            self.cause_infection += 1

    def version2(self):
        if self.node in self.infected:
            self.direction *= -1j  # turn right
            self.infected.remove(self.node)  # remove infection
            self.flagged.add(self.node)  # add to flagged
        elif self.node in self.weakend:
            # no turn
            self.weakend.remove(self.node)  # remove from weakend
            self.infected.add(self.node)  # become infected
            self.cause_infection += 1
        elif self.node in self.flagged:
            self.direction *= -1  # turn around
            self.flagged.remove(self.node)
        else:  # clean
            self.direction *= 1j  # turn left
            self.weakend.add(self.node)  # add to weakend

    def activity(self):
        if self.evolved:
            self.version2()
        else:
            self.verion1()
        self.move_one()

    def move_one(self):
        self.node += self.direction

    def run(self, n):
        for _ in range(n):
            self.activity()


@timeit
def get_answer(data, part2=False):
    w = Worm(data, part2)
    if part2:
        runs = 10000000
    else:
        runs = 10000
    w.run(runs)
    return w.cause_infection


if __name__ == '__main__':
    day = int(os.path.basename(__file__).split('.')[0].split('y')[1])
    inputs = get_instructions(day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
