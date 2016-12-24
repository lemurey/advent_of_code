from utilities import timeit
import md5, sys
from string import printable
from random import choice


CHARS = printable[:-6]

def compute_hash(string, count):
    return md5.new('{}{}'.format(string, count)).hexdigest()


def decrypting(password):
    out = ''
    finished = '\033[37m{}\033[0m'
    for char in password:
        if char == '':
            out += choice(CHARS)
        else:
            out += finished.format(char)
    sys.stdout.write('\r')
    sys.stdout.write(out)
    sys.stdout.flush()


@timeit
def get_result(instructions, part2=False):
    result = ['' for _ in xrange(8)]
    count = 0
    filled = 0
    while filled < 8:
        count += 1
        hashed = compute_hash(instructions, count)
        if hashed[:5] == '00000':
            test = hashed[5]
            if not part2:
                result[filled] = hashed[5]
                filled += 1
            elif test.isdigit():
                if int(test) <= 7:
                    if result[int(test)] == '':
                        result[int(test)] = hashed[6]
                        filled += 1
        if count % 5000 == 0 or filled == 8:
            decrypting(result)

    return ''.join(result)


if __name__ == '__main__':
    with open('instructions_day5.txt', 'r') as f:
        instructions = f.read().strip()
    # print get_result(instructions, part2=False)
    print get_result(instructions, part2=True)