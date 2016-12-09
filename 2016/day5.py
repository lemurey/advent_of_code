import md5

with open('instructions_day5.txt', 'r') as f:
    instructions = f.read().strip()


def compute_hash(string, count):
    return md5.new('{}{}'.format(string, count)).hexdigest()

def get_result(instructions, ordered=False):
    result = ['' for _ in xrange(8)]
    count = 0
    filled = 0
    while filled < 8:
        hashed = compute_hash(instructions, count)
        if hashed[:5] == '00000':
            test = hashed[5]
            if not ordered:
                result[filled] = hashed[5]
                filled += 1
            elif test.isdigit():
                if int(test) <= 7:
                    if result[int(test)] == '':
                        result[int(test)] = hashed[6]
                        filled += 1
        count += 1
    return ''.join(result)


if __name__ == '__main__':
    # print get_result(instructions)
    print get_result(instructions, True)