from time import time
from collections import deque

def elf_cycle(n):
    presents = {i : 1 for i in xrange(1, n + 1)}
    iterations = 1
    index = 0
    while len(presents) != 1:
        to_remove = []
        for key in presents:
            if (index % 2) - 1 == 0:
                presents[prev] += presents[key]
                presents[key] = 0
                to_remove.append(key)
            prev = key
            index += 1
        for key in to_remove:
            del presents[key]
    return presents.keys()[0]


def elf_cycle2_dict(n):
    presents = {i: {'prev' : i - 1, 'next' : i + 1} for i in xrange(1, n + 1)}
    presents[1]['prev'] = n
    presents[n]['next'] = 1
    start = 1
    middle = n/2 + 1
    iterations = 0
    for iteration in xrange(n - 1):
        
        to_remove = middle

        presents[presents[middle]['prev']]['next'] = presents[middle]['next']
        presents[presents[middle]['next']]['prev'] = presents[middle]['prev']
        n_middle = presents[middle]['next']
        start = presents[start]['next']

        if (n - iteration) % 2 == 1:
            n_middle = presents[n_middle]['next']

        middle = n_middle

    return start


def elf_cycle2(n):
    ## initialize two lists (need two because cannot remove from middle of deques)
    first, second = deque(), deque()
    for i in xrange(1, n + 1):
        if i < n/2 + 1:
            first.append(i) # elves 1 to n/2 [1, 2, 3, ...]
        else:
            second.appendleft(i) #elves n/2 to n [n, n-1, n-2, ...]

    while first and second:
        if len(first) > len(second):
            first.pop()
        else:
            second.pop()

        second.appendleft(first.popleft()) # cycle elements
        first.append(second.pop()) # cycle elements
    if first:
        return first[0]
    else:
        return second[0]


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
def get_results(instructions, part2=False, method=None):
    if part2:
        if method == 'dict':
            return elf_cycle2_dict(int(instructions))
        else:
            return elf_cycle2(int(instructions))
        
    else:
        return elf_cycle(int(instructions))


if __name__ == '__main__':
    with open('instructions_day19.txt', 'r') as f:
        instructions = f.read().strip()

    print get_results(instructions, part2=False)
    print get_results(instructions, part2=True, method='linked')
    print get_results(instructions, part2=True, method='dict')

