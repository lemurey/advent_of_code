from aoc_utilities import get_instructions
from pathlib import Path
from operator import add, mul
from itertools import product


def parse_tests(data):
    outputs = []
    for line in data:
        value, rest = line.split(':')
        inputs = list(map(int, rest.split()))
        outputs.append((int(value), inputs))
    return outputs


def run_ops(sequence, values, debug=False):
    out = values[0]
    for index, op in enumerate(sequence, start=1):
        out = op(out, values[index])
        if debug:
            print(out)
    return out


def cat(v1, v2):
    return int(str(v1) + str(v2))


def get_answer(data, part2=False):
    tests = parse_tests(data)
    valid = []

    if part2:
        ops = (add, mul, cat)
    else:
        ops = (add, mul)

    for value, inputs in tests:
        for op_sequence in product(ops, repeat=len(inputs)-1):
            to_test = run_ops(op_sequence, inputs)
            # print(value, inputs, to_test)
            if value == to_test:
                valid.append(value)
                break
    # print(valid)
    return sum(valid)


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''190: 10 19
# 3267: 81 40 27
# 83: 17 5
# 156: 15 6
# 7290: 6 8 6 15
# 161011: 16 10 13
# 192: 17 8 14
# 21037: 9 7 18 13
# 292: 11 6 16 20'''.split('\n')
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
