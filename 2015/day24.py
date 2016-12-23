from utilities import timeit
from itertools import combinations


#this was unneccesary to solving the problem, but I had fun writing it
#generate all possible subsequences that sum to a specified number
def checker(items, W, smallest=set()):
    N = len(items)
    results = {0 : []}
    for entry in items:
        for i in xrange(W , 0, -1):
            if i - entry in results:
                cur = (entry, )
                for prev in results[i - entry]:
                    if i not in results:
                        results[i] = []
                    if prev + cur in smallest:
                        continue
                    results[i].append( prev + cur )
                if not results[i - entry]:
                    if i not in results:
                        results[i] = []
                    results[i].append( cur )

    return results[W]


def get_pacakages(lines):
    packages = []
    for item in lines.split():
        packages.append(int(item))
    return set(packages)


def get_smallest(packages, check_val=512):
    smallest = []
    for i, _ in enumerate(packages, 1):
        for combo in combinations(packages, i):
            if sum(combo) == check_val:
                smallest.append(combo)
        if smallest:
            return sorted(smallest, key=lambda x: prod(x))
    return []


def prod(x):
    o = 1
    for i in x:
        o *= i
    return o


def find_qe(packages, check_val, part2):

    smallest = get_smallest(packages, check_val)
    for entry in smallest:
        remainder = packages - set(entry)
        next_smallest = get_smallest(remainder, check_val)
        for entry2 in next_smallest:
            remainder2 = remainder - set(entry2)
            next_next_smallest = get_smallest(remainder2, check_val)
            for entry3 in next_next_smallest:
                if not part2:
                    return prod(entry)
                remainder3 = remainder2 - set(entry3)
                next_next_next_smallest = get_smallest(remainder3, check_val)
                for entry4 in next_next_next_smallest:
                    return prod(entry)


@timeit
def get_results(instructions, part2=False):
    packages = get_pacakages(instructions)
    if part2:
        check_val = sum(packages)/4
    else:
        check_val = sum(packages)/3
    return find_qe(packages, check_val, part2)
    

if __name__ == '__main__':
    with open('instructions_day24.txt', 'r') as f:
        instructions = f.read().strip()
    print get_results(instructions, part2=False)
    print get_results(instructions, part2=True)
