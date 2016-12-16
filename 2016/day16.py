from time import time

def timeit(function):
    def timed(*args, **kwargs):
        s_t = time()
        result = function(*args, **kwargs)
        e_t = time()
        out = '{} {} took {:.2f} sec'
        print out.format(function.__name__, kwargs, e_t - s_t)
        return result
    return timed


def dragon_curve(data):
    b = data[::-1].replace('1', '2').replace('0', '1').replace('2', '0')
    return '{}0{}'.format(data, b)


def checksum(data):
    output = ''
    for index in range(1, len(data), 2):
        if data[index] == data[index - 1]:
            output += '1'
        else:
            output += '0'
    return output


@timeit
def get_results(instructions, part2=False):
    string = instructions
    if part2:
        length = 35651584
    else:
        length = 272
    while len(string) < length:
        string = dragon_curve(string)
    check = checksum(string[:length])
    while len(check) % 2 == 0:
        check = checksum(check)
    return check


if __name__ == '__main__':
    with open('instructions_day16.txt', 'r') as f:
        instructions = f.read().strip()
    print get_results(instructions, part2=False)
    print get_results(instructions, part2=True)



