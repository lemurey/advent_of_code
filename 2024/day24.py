from aoc_utilities import get_instructions
from pathlib import Path
from functools import partial
from itertools import combinations
import re


def _and(a, b):
    return a and b


def _or(a, b):
    return a or b


def _xor(a, b):
    return a ^ b


def _get(mappings, key):
    if mappings[key] in (0, 1):
        return mappings[key]
    a, op, b = mappings[key]
    return op(_get(mappings, a), _get(mappings, b))


def parse_inputs(data):
    is_input = True
    mapping = {}
    ops = {'XOR': _xor, 'OR': _or, 'AND': _and}
    finals = {}
    for line in data:
        if line == '':
            is_input = False
            continue

        if is_input:
            label, value = line.split(': ')
            mapping[label] = int(value)
        else:
            inputs, outputs = line.split(' -> ')
            a, op, b = inputs.split()
            mapping[outputs] = (a, ops[op], b)
            if outputs.startswith('z'):
                finals[outputs] = None

    return mapping


def get_value(mappings, which, is_int=False):
    vals = {}
    for k in mappings:
        if k.startswith(which):
            vals[k] = _get(mappings, k)
    vals = sorted(vals.items(), key=lambda x: x[0], reverse=True)
    if is_int:
        return int(''.join(str(y) for x, y in vals), base=2)
    return ''.join(str(y) for x, y in vals)


def check_map(mappings, verbose=False):
    check_func = partial(get_value, mappings)
    x, y, z = map(check_func, 'xyz')
    x = '0' + x
    y = '0' + y

    if verbose:
        print(x)
        print(y)
        print(z)

    carry = 0
    for i, (xb, yb, zb) in enumerate(zip(x[::-1], y[::-1], z[::-1])):
        v = int(xb) + int(yb) + carry
        if v == 3:
            carry = 1
            v = 1
        elif v == 2:
            carry = 1
            v = 0
        else:
            carry = 0
        if v != int(zb):
            return i, f'issue at z{i:0>2}'
            outs.append()


def swap(mappings, k1, k2):
    c = mappings.copy()
    t1 = c[k1]
    t2 = c[k2]
    c[k1] = t2
    c[k2] = t1
    return c


def new_map(mappings, x, y):
    s = mappings.copy()
    for i, xb in enumerate(x):
        s[f'x{i:0>2}'] = int(xb)
    for i, yb in enumerate(y):
        s[f'y{i:0>2}'] = int(yb)
    return s


def inspect(mappings, key, depth=0):
    if mappings[key] in (0, 1) or depth >= 5:
        return key
    kl = mappings[key][0]
    kr = mappings[key][2]
    l = inspect(mappings, kl, depth + 1)
    r = inspect(mappings, kr, depth + 1)
    if mappings[key][1] == _and:
        return f'{key}: ({l}) & ({r})'
    if mappings[key][1] == _or:
        return f'{key}: ({l}) | ({r})'
    if mappings[key][1] == _xor:
        return f'{key}: ({l}) ^ ({r})'


def get_answer(data, part2=False):
    mappings = parse_inputs(data)
    z = get_value(mappings, 'z')
    # part1 finished
    print(int(z, base=2))

    max_val = len([x for x in mappings.keys() if x.startswith('x')])
    ###########

    with open('check_maps.txt', 'w') as f:
        for k in mappings.keys():
            if k.startswith('x') or k.startswith('y') or k.startswith('z'):
                continue
            f.write((inspect(mappings, k)) + '\n')

    s1 = swap(mappings, 'z05', 'tst')
    s2 = swap(s1, 'z11', 'sps')
    s3 = swap(s2, 'z23', 'frt')
    s4 = swap(s3, 'cgh', 'pmd')

    # to_check = s4
    # print(check_map(to_check))
    # print('-' * 15)

    # for i in range(max_val):
    #     if i < 35:
    #         continue
    #     if i > 40:
    #         continue
    #     print(inspect(to_check, f'z{i:0>2}'))

    # from numpy.random import randint
    # x = ''.join(str(x) for x in randint(0, 2, (45, )))
    # y = ''.join(str(x) for x in randint(0, 2, (45, )))

    # s = new_map(s4, x, y)
    # print(check_map(s))
        
    switches = ('z05', 'tst', 'z11', 'sps', 'z23', 'frt', 'cgh', 'pmd')
    return ','.join(sorted(switches))


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)

#     inputs = '''x00: 1
# x01: 0
# x02: 1
# x03: 1
# x04: 0
# y00: 1
# y01: 1
# y02: 1
# y03: 1
# y04: 1

# ntg XOR fgs -> mjb
# y02 OR x01 -> tnw
# kwq OR kpj -> z05
# x00 OR x03 -> fst
# tgd XOR rvg -> z01
# vdt OR tnw -> bfw
# bfw AND frj -> z10
# ffh OR nrd -> bqk
# y00 AND y03 -> djm
# y03 OR y00 -> psh
# bqk OR frj -> z08
# tnw OR fst -> frj
# gnj AND tgd -> z11
# bfw XOR mjb -> z00
# x03 OR x00 -> vdt
# gnj AND wpb -> z02
# x04 AND y00 -> kjc
# djm OR pbm -> qhw
# nrd AND vdt -> hwm
# kjc AND fst -> rvg
# y04 OR y02 -> fgs
# y01 AND x02 -> pbm
# ntg OR kjc -> kwq
# psh XOR fgs -> tgd
# qhw XOR tgd -> z09
# pbm OR djm -> kpj
# x03 XOR y03 -> ffh
# x00 XOR y04 -> ntg
# bfw OR bqk -> z06
# nrd XOR fgs -> wpb
# frj XOR qhw -> z04
# bqk OR frj -> z07
# y03 OR x01 -> nrd
# hwm AND bqk -> z03
# tgd XOR rvg -> z12
# tnw OR pbm -> gnj'''.split('\n')

    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))
