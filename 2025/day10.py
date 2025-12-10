from aoc_utilities import get_instructions
from pathlib import Path
from collections import deque
from scipy.optimize import linprog

class Machine:
    def __init__(self, indicator, wiring):
        self.light_start = ['.' for _ in indicator]
        self.indicator = indicator
        self.wiring = wiring

    def push(self, which, lights):
        new = [x for x in lights]
        switch = {'#': '.', '.': '#'}
        for idx in self.wiring[which]:
            new[idx] = switch[new[idx]]
        return new

    def next(self):
        for k in self.wiring:
            yield k


def search(machine):
    start = machine.light_start
    Q = deque([(0, start)])
    c = 0
    while Q:
        num_preses, state = Q.popleft()

        # c += 1

        # if c % 10000 == 0:
        #     print(c, len(Q))

        for which in machine.next():
            new_state = machine.push(which, state)
            if new_state == machine.indicator:
                return num_preses + 1
            Q.append((num_preses + 1, new_state))
    print('this broke')
    return 0


def parse_input(lines):
    machines = []
    joltages = []
    for line in lines:
        wiring = {}
        indicator, *rest = line.split()
        indicator = list(indicator.strip('[]'))
        for entry in rest:
            if entry.startswith('('):
                wiring[entry] = list(map(int, entry.strip('()').split(',')))
            elif entry.startswith('{'):
                joltage = list(map(int, entry.strip('{}').split(',')))
                joltages.append(joltage)
            else:
                print('this should not happen')
        machines.append(Machine(indicator, wiring))
    return machines, joltages

## I don't like doing this for part2, but I don't know enough about
## linear programming to create my own, and the scipy solver works for this

def get_answer(data, part2=False):
    machines, joltages = parse_input(data)
    total_presses = 0
    if part2:
        for machine, joltage in zip(machines, joltages):
            buttons = [x for x in machine.wiring.values()]
            steps = [1 for _ in buttons]
            matrix = []
            for i, _ in enumerate(joltage):
                inner = []
                for b in buttons:
                    inner.append((i in b))
                matrix.append(inner)
            total_presses += linprog(steps, A_eq=matrix, b_eq=joltage, integrality=1).fun
    else:
        for i, machine in enumerate(machines):
            total_presses += search(machine)
    return total_presses


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)

#     inputs = '''[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
# [...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
# [.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}'''.split('\n')

    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
