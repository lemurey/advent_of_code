from utilities import timeit


# start at 20151125; multiply by 252533; mod by 33554393
def get_location(instructions):
    output = []
    for word in instructions.split():
        if word.strip('.,').isdigit():
            output.append(int(word.strip('.,')))
    return output

def next_val(num):
    if num == 0:
        return 20151125
    return num * 252533 % 33554393


def get_iter(x, y):
    '''

    (4, 3) -> (5, 3) is +6 (3 from column 3 from row)
    (4, 3) -> (4, 4) is +7 (4 from column 3 from row)
    previous value + (row - 1) + column is rule
    to go from (1, 1) to (x, y) is sum(range(x + y))
    but that would be x from row not x - 1, so subtract off another x - 1
    sum(range(x + y)) - (x - 1)
    '''
    return sum(range(x + y)) - (x - 1)

def brute_force(x, y):
    num = 0
    for _ in xrange(get_iter(x, y)):
        num = next_val(num)
    return num


@timeit
def get_results(instructions, part2=False):
    location = get_location(instructions)
    print get_iter(*location)
    return brute_force(*location)
    # return brute_force(*location)
    

if __name__ == '__main__':
    with open('instructions_day25.txt', 'r') as f:
        instructions = f.read().strip()
    print get_results(instructions, part2=False)
    # print get_results(instructions, part2=True)
