from aoc_utilities import get_instructions
from pathlib import Path

from collections import defaultdict

'''
The commented code below is what I initially ran, it essentially brute forces
the result, but it only searches ~200million numbers rather than the full
10^14 numbers

I had been trying to do something like what is done in the uncommented code, but
couldn't get the proper space to search working out. I found code similar to
below on the reddit and re-wrote for my purposes.
'''


def process_data(data):
    program = []
    for line in data:
        if 'inp' in line:
            program.append(('inp', 'w', None))
            continue
        inst, reg, val = line.split()
        if val in 'wxyz':
            program.append((inst, reg, val))
        else:
            program.append((inst, reg, int(val)))
    return program


def simplify_program(program):
    simplified = []
    count = 1
    for inst, reg, val in program[1:]:
        if inst == 'inp':
            count = 0
            simplified.append((x_add, z_div, y_add))
        if inst == 'div' and reg == 'z':
            z_div = val
        if inst == 'add' and reg == 'x' and val != 'z':
            x_add = val
        if count == 15:
            y_add = val
        count += 1

    simplified.append((x_add, z_div, y_add))
    return simplified


def reverse_solve(z_in, levels, i, finals):
    B, A, C = levels[i]

    solns = defaultdict(list)
    for d in range(1, 10):
        for z in z_in:
            for sa in range(A):
                pz = z * A + sa
                if (pz % 26) + B == d:
                    if pz // A == z:
                        solns[pz].append((d, z))
                pz = int(((z - d - C) / 26) * A + sa)
                if pz % 26 + B != d:
                    if pz // A * 26 + d + C == z:
                        solns[pz].append((d, z))

    finals[i] = solns
    if i > 0:
        reverse_solve(solns.keys(), levels, i-1, finals)


def construct_solution(z, index, space, vals, largest):
    # print(index, z, space.get(index, {}).get(z, None), vals)

    if index == 14:
        print(''.join(str(x) for x in vals))
        return True

    if z not in space[index]:
        return False

    for d, next_z in sorted(space[index][z], reverse=largest):
        digits = vals[:] + [d]
        ni = index + 1
        # print(ni)
        if construct_solution(next_z, ni, space, digits, largest):
            return True




def get_answer(data, part2):
    program = process_data(data)
    simplified = simplify_program(program)

    finals = {}
    reverse_solve([0], simplified, 13, finals)

    construct_solution(0, 0, finals, [], True)
    construct_solution(0, 0, finals, [], False)


# def loop(z_init, d, x_add, z_div, y_add):

#     x = int(z_init) % 26
#     z = int(int(z_init) / z_div)
#     x += x_add
#     if x != d:
#         y = 26
#         z = z * y
#         y = d + y_add
#         z = z + y
#     return z


# def run_loop(current, zis):
#     outs = []
#     for zi in zis:
#         for d in range(1, 10):
#             outs.append(loop(zi, d, *current))
#     return set(outs)


# def run_loop_reverse(current, zins, valids):
#     possibles = []
#     for zi in zins:
#         for d in range(1, 10):
#             val = loop(zi, d, *current)
#             if val in valids:
#                 possibles.append(d)
#     return possibles


# def get_answer(data, part2=False):

#     program = process_data(data)
#     simplified = simplify_program(program)

#     ## uncomment to brute force valid inputs
#     # z_in = set([0])
#     # with open('all_zs.txt', 'w') as f:
#     #     for level in simplified:
#     #         f.write(','.join(str(x) for x in z_in) + '\n')
#     #         new_zs = set()
#     #         for z in z_in:
#     #             for d in range(1, 10):
#     #                 new_zs.add(loop(z, d, *level))
#     #         print(len(new_zs))
#     #         z_in = new_zs

#     input_vals = []
#     with open('all_zs.txt', 'r') as f:
#         for line in f.readlines():
#             input_vals.append(list(map(int, line.split(','))))


#     valid_outs = set([0])
#     potential_digits = []
#     for inputs, level in zip(input_vals[::-1], simplified[::-1]):
#         print(len(inputs))
#         potential_digits.append(set())
#         next_ins = set()
#         for z_in in inputs:
#             for d in range(1, 10):
#                 out = loop(z_in, d, *level)
#                 if out in valid_outs:
#                     potential_digits[-1].add(d)
#                     next_ins.add(z_in)
#         valid_outs = next_ins

#     for entry in potential_digits:
#         print(sorted(entry))


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))
