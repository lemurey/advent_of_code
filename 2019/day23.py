from aoc_utilities import get_instructions
import os
from intcode import Intcode
from time import time


def run_part1(network):
    backup = 0
    to_run = []
    while True:
        if len(to_run) == 0:
            comp = network[backup]
            backup = (backup + 1) % 50
        else:
            cnum = to_run.pop(0)
            comp = network[cnum]

        comp.waiting = False
        loc = comp.run()
        if loc is None:
            continue
        comp.waiting = False
        x = comp.run()
        comp.waiting = False
        y = comp.run()
        if loc == 255:
            return y
        else:
            to_run.append(loc)
        network[loc].secondary.extend([x, y])


def check_idle(network):
    for i, comp in enumerate(network):
        comp.waiting = False
        val = comp.run()
        if val is not None:
            return comp, val
    return True, None


def run_part2(network):
    nat = []
    seen = set()
    idle_status =[False for _ in network]

    backup = 0
    to_run = []
    current = 0
    prev = -1

    while True:
        comp, loc = check_idle(network)
        if comp == True:
            if nat == []:
                pass
            else:
                if nat[1] == prev:
                    return prev

                network[0].secondary = nat
                prev = nat[1]
            continue

        comp.waiting = False
        x = comp.run()
        comp.waiting = False
        y = comp.run()
        if loc == 255:
            nat = [x, y]
        else:
            network[loc].secondary.extend([x, y])


def get_answer(data, part2=False):
    program = list(map(int, data[0].split(',')))
    network = []
    for i in range(50):
        comp = Intcode([x for x in program], input=i, mode='network')
        network.append(comp)


    if part2:
        return run_part2(network)

    return run_part1(network)


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
