from aoc_utilities import get_instructions
from pathlib import Path


def parse_signal(code, signal):
    two_three_five = []
    zero_six_nine = []
    # identify length groupings
    for entry in code:
        if len(entry) == 2:
            one = entry
        elif len(entry) == 4:
            four = entry
        elif len(entry) == 3:
            seven = entry
        elif len(entry) == 7:
            eight = entry
        elif len(entry) == 5:
            two_three_five.append(entry)
        elif len(entry) == 6:
            zero_six_nine.append(entry)
    # find top segment
    top = seven.difference(one).pop()
    # identify which is three
    for entry in two_three_five:
        if one.intersection(entry) == one:
            three = entry
    two_three_five.remove(three)
    # find top left
    top_left = four.difference(three).pop()
    # identify 5
    for entry in two_three_five:
        if top_left in entry:
            five = entry
    two_three_five.remove(five)
    # identify 2
    two = two_three_five[0]
    # find top right
    top_right = two.intersection(one).pop()
    # find bottom right
    bottom_right = one.difference(set(top_right)).pop()
    # identify 9
    nine = three.copy()
    nine.add(top_left)
    zero_six_nine.remove(nine)
    # identify 6
    for entry in zero_six_nine:
        if top_right not in entry:
            six = entry
    zero_six_nine.remove(six)
    # identify zero
    zero = zero_six_nine[0]

    decoder = {}
    for entry in signal:
        if set(entry) == zero:
            decoder[entry] = '0'
        elif set(entry) == one:
            decoder[entry] = '1'
        elif set(entry) == two:
            decoder[entry] = '2'
        elif set(entry) == three:
            decoder[entry] = '3'
        elif set(entry) == four:
            decoder[entry] = '4'
        elif set(entry) == five:
            decoder[entry] = '5'
        elif set(entry) == six:
            decoder[entry] = '6'
        elif set(entry) == seven:
            decoder[entry] = '7'
        elif set(entry) == eight:
            decoder[entry] = '8'
        elif set(entry) == nine:
            decoder[entry] = '9'

    return decoder


def parse_inputs(data):
    codes = []
    signals = []
    numbers = []
    for line in data:
        s, n = line.split('|')
        base = s.strip().split(' ')
        codes.append([set(x) for x in base])
        signals.append([''.join(sorted(x)) for x in base])
        numbers.append([''.join(sorted(x)) for x in n.strip().split(' ')])
    return codes, signals, numbers


def part_1(numbers):
    counts = {2: 0, 4: 0, 3: 0, 7: 0}
    for entry in numbers:
        for num in entry:
            if len(num) in counts:
                counts[len(num)] += 1
    return sum(counts.values())


def get_decoder(codes, signals):
    decoder = []
    for c, s in zip(codes, signals):
        decoder.append(parse_signal(c, s))
    return decoder


def get_answer(data, part2=False):
    codes, signals, numbers = parse_inputs(data)
    if part2:
        total = 0
        decoder = get_decoder(codes, signals)
        for entry, rosetta in zip(numbers, decoder):
            num = ''.join(rosetta[digit] for digit in entry)
            total += int(num)
        return total
    return part_1(numbers)


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
