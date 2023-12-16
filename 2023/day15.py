from aoc_utilities import get_instructions
from pathlib import Path


def hhash(ch, cur=0):
    return ((cur + ord(ch)) * 17) % 256


def run_hhash(chars):
    value = 0
    for char in chars:
        if char == '\n':
            continue
        value = hhash(char, value)
    return value


def prep_instructions(instructions):
    new =[]
    for step in instructions:
        if '-' in step:
            label, _ = step.split('-')
            new.append((label, run_hhash(label), None))
        elif '=' in step:
            label, f = step.split('=')
            new.append((label, run_hhash(label), int(f)))
    return new


def hashmap(instructions, verbose=False):
    the_map = [{} for _ in range(256)]
    for label, box, lens in instructions:
        if lens is None:
            if label in the_map[box]:
                del the_map[box][label]
        if lens is not None:
            the_map[box][label] = lens
        if verbose:
            print(label, lens)
            for i, box in enumerate(the_map):
                if len(box) > 0:
                    print(f'Box {i}: {box.items()}')
    return the_map


def get_answer(data, part2=False):
    output = 0
    for sub in data[0].split(','):
        value = run_hhash(sub)
        output += value
    print(output)
    instructions = prep_instructions(data[0].split(','))

    the_map = hashmap(instructions)
    power = 0
    for i, box in enumerate(the_map):
        c = i + 1
        if len(box) > 0:
            # print(f'Box {i}: {box.items()}')
            for j, (label, lens) in enumerate(box.items(), start=1):
                val = j * lens
                power += c * val
    return power


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
    # inputs = 'rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'.split('\n')
    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))
