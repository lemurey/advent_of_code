from time import time


def update(groups, item):
    output = []
    for entry in groups:
        output.append(entry + (item,))
    if len(output) == 0:
        output.append((item,))
    return output


def check_volume(volume, containers, part2):
    ways = [1] + [0] * volume
    groups = [[] for _ in range(volume + 1)]
    for capacity in containers: 
    # loop over containers first for enforcing limit on nubmer of containers
        for vol in xrange(volume, capacity - 1, -1): 
            ways[vol] += ways[vol - capacity]
            if ways[vol] and ways[vol - capacity]:
                groups[vol].extend(update(groups[vol  - capacity], capacity))
    if part2:
        check_length = len(min(groups[volume], key=lambda x: len(x)))
        return len(filter(lambda x : len(x) == check_length, groups[volume]))
    return ways[volume]


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
    containers = map(int, instructions.split())
    return check_volume(150, containers, part2)


if __name__ == '__main__':
    with open('instructions_day17.txt', 'r') as f:
        instructions = f.read().strip()
    print get_results(instructions, part2=False)
    print get_results(instructions, part2=True)