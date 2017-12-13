from aoc_utilities import get_instructions
import os
from utilities import timeit


@timeit
def get_answer(data, part2=False):
    periods = {}
    for line in data.split('\n'):
        key, value = line.split(': ')
        periods[int(key)] = 2 * (int(value) - 1)

    if part2:
        delay = 0
        caught = True
        while caught:
            caught = False
            for location, period in periods.items():
                if (location + delay) % period == 0:
                    caught = True
                    delay += 1
                    break
        return delay

    severity = 0
    for location, period in periods.items():
        depth = (period - 2) / 2
        if location % period == 0:
            severity += location * depth
    return severity

    firewall = Firewall(data, part2, visualize=visualize)
    if part2:
        return firewall.run()
    return firewall.check_severity()


if __name__ == '__main__':
    day = int(os.path.basename(__file__).split('.')[0].split('y')[1])
    inputs = get_instructions(day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
