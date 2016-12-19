from time import time

IT = {'^' : {'^' : {'^' : '.', '.' : '^'}, '.' : {'^' : '.', '.' : '^'}}, 
      '.' : {'^' : {'^' : '^', '.' : '.'}, '.' : {'^' : '^', '.' : '.'}}}

def next_line(line):
    line = '.' + line + '.'
    output = ''
    for i, center in enumerate(line[1:-1], 1):
        left = line[i - 1]
        right = line[i + 1]
        output += IT[left][center][right]
    return output


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
    if part2: 
        repeats = 400000
    else:
        repeats = 40
    line = instructions
    count = line.count('.')
    for _ in xrange(repeats - 1):
        line = next_line(line)
        count += line.count('.')
    return count



if __name__ == '__main__':
    with open('instructions_day18.txt', 'r') as f:
        instructions = f.read().strip()
    print get_results(instructions, part2=False)
    print get_results(instructions, part2=True)