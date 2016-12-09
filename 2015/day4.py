import md5


def compute_hash(string, count):
    return md5.new('{}{}'.format(string, count)).hexdigest()


def get_results(instructions, part2=False):
    count = 0
    while True:
        count += 1
        hashed = compute_hash(instructions, count)
        if part2:
            if hashed[:6] == '000000':
                return count
        elif hashed[:5] == '00000':
            return count


if __name__ == '__main__':
    with open('instructions_day4.txt', 'r') as f:
        instructions = f.read().strip()
    print get_results(instructions)
    print get_results(instructions, True)