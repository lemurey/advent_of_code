from utilities import timeit
import numpy as np
'''
initially did this really slowly with an inefficient extra factoring calculation
this method is much better, iterate over elves first then the houses inside
I switched to numpy for faster iteration on the inner loop, speeds up the code
by ~ a factor of 5
'''

def elves(check, part2):
    houses = np.ones(check / 10)

    for elf in xrange(2, check / 10):
        if part2:
            houses[elf:(elf + 1) * 50:elf] += 11 * elf
        else:
            houses[elf::elf] += 10 * elf
        if houses[elf] >= check:
            return elf


@timeit
def get_results(instructions, part2=False):
    value = int(instructions)
    return elves(value, part2)


if __name__ == '__main__':
    with open('instructions_day20.txt', 'r') as f:
        instructions = f.read().strip()
    print get_results(instructions, part2=False)
    print get_results(instructions, part2=True)
