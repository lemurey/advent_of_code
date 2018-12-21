from aoc_utilities import get_instructions
import os
from day19 import OPR2, process_codes


def decompiled():
    stops = set()

    D = 0
    E = 0
    D = E | 65536 # command 6
    E = 16098955 # command 7
    while True:
        F = D % 256 # 8
        E += F   # 9
        E = (E % (2 ** 24) * 65899) % (2 ** 24) # 10 - 12

        # program does the following
        if D < 256: # condition is commands 13 - 16
            '''
            if A == E:
                break
            '''
            # so to answer questions:
            if not stops:
                print E
            if E not in stops:
                prev = E
            if E in stops:
                return prev
            stops.add(E)
            D = E | 65536
            E = 16098955
        else:
            # the time consuming loop of commands do the following
            D = D / 256


def get_answer(data, part2=False):
    return decompiled()
    # i got some logs to help figure out what code does
    # but mostly this was an excercise in reading the commands directly
    # ip, program = process_codes(data)
    # r = OPR2(ip)
    # if part2:
        # r.registers = [15823996, 0, 0, 0, 0, 0]
    # # num_iters = 5000
    # r.run_program(program, debug=True, early_stop=num_iters, day=21)


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))