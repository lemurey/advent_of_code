from time import time
from itertools import permutations, ifilter

def parse_instructions(instructions):
    properties = {}
    for line in instructions.split('\n'):
        ingredient, rest = line.split(':')
        for proper in rest.split(', '):
            label, value = proper.split()
            if label.strip() not in properties:
                properties[label.strip()] = {}
            properties[label.strip()][ingredient] = int(value)
    return properties


def is_100(lst):
    return sum(lst) == 100


def process_ingredients(properties, part2):
    score = 0
    indices = {ing : i for i, ing in enumerate(properties['calories'])}
    for combo in ifilter(is_100, permutations(range(1, 101), 4)):
        cur_score = 1
        if part2:
            test_val = sum(a * x for a, x in zip(combo, properties['calories'].values()))
            if test_val != 500:
                continue
        for prop in properties:
            total = 0
            if prop == 'calories':
                continue
            for ing in properties[prop]:
                total += combo[indices[ing]] * properties[prop][ing]
            if total < 0:
                break
            else:
                cur_score *= total
        if cur_score > score:
            score = cur_score
    return score


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
    properties = parse_instructions(instructions)
    return process_ingredients(properties, part2)


if __name__ == '__main__':
    with open('instructions_day15.txt', 'r') as f:
        instructions = f.read().strip()
    print get_results(instructions, part2=False)
    print get_results(instructions, part2=True)
