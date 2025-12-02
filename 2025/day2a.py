def parse_input(lines):
    ranges = []
    for line in lines:
        opts = line.split(',')
        for entry in opts:
            start, end = map(int, entry.split('-'))
            ranges.append((start, end))
    return ranges


def check_id1(id):
    id = str(id)
    if len(id) % 2 != 0:
        return False
    mid = len(id) // 2
    if (id[:mid] * 2) == id:
        return True
    return False


def _get_factors(length):
    factors = []
    for i in range(1, length // 2 + 1):
        if (length % i == 0):
            factors.append(i)
    return factors


def check_id2(id):
    id = str(id)
    factors = _get_factors(len(id))
    for factor in factors:
        mult = len(id) // factor
        if (id[:factor] * mult) == id:
            return True
    return False


def get_answer(data, part2=False):
    ranges = parse_input(data)
    output = 0

    for start, stop in ranges:
        for val in range(start, stop + 1):
            if part2:
                if check_id2(val):
                    output += val
            else:
                if check_id1(val):
                    output += val
    return output


if __name__ == '__main__':
    # p = Path(__file__).absolute()
    # year = p.parent.stem
    # day = int(p.stem.split('y')[1])
    # inputs = get_instructions(year, day)
    with open('instructions_day_02.txt', 'r') as f:
        inputs = f.read().splitlines()

    # inputs = ['11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124']

    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
