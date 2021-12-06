from aoc_utilities import get_instructions
from pathlib import Path


class LanternFish:
    def __init__(self, vals):
        self.state = {i: 0 for i in range(9)}
        for num in vals:
            self.state[int(num)] += 1

    def __call__(self):
        dupe = {i: 0 for i in range(9)}
        dupe[-1] = 0
        for i in self.state:
            dupe[i - 1] = self.state[i]

        dupe[8] += dupe[-1]
        dupe[6] += dupe[-1]

        self.state = {i: x for i, x in dupe.items() if i >= 0}

    def __str__(self):
        out = ''
        for k in sorted(self.state):
            out += f'{k}: {self.state[k]}, '
        return out.strip(', ')


def get_answer(data, part2=False):
    school = LanternFish(data[0].split(','))

    to_run = 80
    if part2:
        to_run = 256
    for i in range(to_run):
        school()
    return sum(school.state.values())


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
