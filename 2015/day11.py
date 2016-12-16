import re
from time import time

CHECK = re.compile(r'i|o|l')
CHECK2 = re.compile(r'(.)\1.+(.)\2')

def check_password(password):
    if CHECK.search(password):
        return False
    if not CHECK2.search(password):
        return False
    values = map(ord, password)
    for index, letter in enumerate(values[1:-1], 1):
        prev = values[index - 1]
        next = values[index + 1]
        if letter == prev + 1 and letter == next - 1:
            return True
    return False


def increment_password(password):
    values = map(ord, password)
    change = True
    output = ''
    for val in values[::-1]:
        if change:
            val = ((val - 97) + 1) % 26 + 97
            if val != 97:
                change = False
        output += chr(val)
    return output[::-1]


def timeit(function):
    def timed(*args, **kwargs):
        s_t = time()
        result = function(*args, **kwargs)
        e_t = time()
        out = '{} {} took {:.2f} sec'
        print out.format(function.__name__, kwargs, e_t - s_t)
        return result
    return timed
    

@timeit
def get_results(instructions, part2=False):
    password = instructions
    iterations = 0
    while True:
        iterations += 1
        password = increment_password(password)
        if check_password(password):
            if part2:
                return get_results(password)
            return password
        if iterations > 10000000:
            print 'uh oh'
            print password
            return
    return


if __name__ == '__main__':
    with open('instructions_day11.txt', 'r') as f:
        instructions = f.read().strip()
    print get_results(instructions, part2=False)
    print get_results(instructions, part2=True)