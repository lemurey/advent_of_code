from aoc_utilities import get_instructions
import os
from collections import defaultdict


class Mapper(object):
    def __init__(self, directions):
        self.directions = directions
        self.location = complex(0)
        self.dirs = {'W': complex(-1), 'N': complex(0, -1),
                     'E': complex(1), 'S': complex(0, 1)}
        self.locations = []
        self.distances = defaultdict(int)

    def move(self, d):
        direction = self.dirs[d]
        prev = self.location
        self.location += direction
        cur = self.location

        if self.distances[cur] != 0:
            a = self.distances[cur]
            b = self.distances[prev] + 1
            self.distances[cur] = min(a, b)
        else:
            self.distances[cur] = self.distances[prev] + 1

    def map_out(self):
        for c in self.directions[:-1]:
            if c == '(':
                self.locations.append(self.location)
            elif c == '|':
                self.location = self.locations[-1]
            elif c == ')':
                self.location = self.locations.pop()
            else:
                self.move(c)


def get_answer(data, part2=False):
    reg = data[0].strip('^')
    m = Mapper(reg)
    m.map_out()
    if part2:
        return len([x for x in m.distances.values() if x >= 1000])
    return max(m.distances.values())




if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
    # sample = ['^WNE$']
    # print get_answer(sample)
    # sample = ['^ENWWW(NEEE|SSE(EE|N))$']
    # print get_answer(sample)
    # sample = ['^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$']
    # print get_answer(sample)
    # sample = ['^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$']
    # print get_answer(sample)
    # sample = ['^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$']
    # print get_answer(sample)
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
