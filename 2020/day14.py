from aoc_utilities import get_instructions
from pathlib import Path


def dec_to_bin(num):
    return '{0:036b}'.format(num)


def bin_to_dec(num):
    return int(num, 2)


def apply_mask(mask, num):
    num = list(num)
    for loc, val in mask.items():
        num[loc] = val
    return ''.join(num)


def run_init(data):
    mem = {}
    for row in data:
        command, value = row.split(' = ')
        if command == 'mask':
            mask = {}
            for i, entry in enumerate(value):
                if entry == 'X':
                    continue
                mask[i] = entry
        else:
            num_b = dec_to_bin(int(value))
            updated = apply_mask(mask, num_b)
            mem[command] = bin_to_dec(updated)

    return mem


def _extract_num(cmd):
    return int(cmd[4:-1])


def make_split(arr):
    new = []
    for entry in arr:
        new.append(entry + '0')
        new.append(entry + '1')
    return new


def apply_mask_v2(mask, num):
    outs = ['']

    num_b = list(dec_to_bin(num))

    for i, val in enumerate(mask):
        if val == '0':
            outs = [x + num_b[i] for x in outs]
        elif val == '1':
            outs = [x + '1' for x in outs]
        else:
            outs = make_split(outs)

    for entry in outs:
        yield entry


def run_init_v2(data):
    mem = {}
    for row in data:
        command, value = row.split(' = ')
        if command == 'mask':
            mask = value
        else:
            mem_loc = _extract_num(command)
            value = int(value)
            for loc in apply_mask_v2(mask, mem_loc):
                mem[loc] = value
    return mem


def get_answer(data, part2=False):

    if part2:
        mem = run_init_v2(data)
    else:
        mem = run_init(data)
    return sum(mem.values())


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)

    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
