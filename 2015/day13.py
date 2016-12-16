from time import time
from itertools import permutations

def parse_instructions(instructions, part2):
    persons = set([])
    d = {}
    for line in instructions.split('\n'):
        words = line.split()
        person1, person2 = words[0], words[-1].strip('.')
        value = int(words[3])
        mod = -1 if words[2] == 'lose' else 1
        d[(person1, person2)] = mod * value
        if part2:
            d[(person1, 'me')] = 0
            d[('me', person1)] = 0
            persons.add('me')
        persons.add(person1)
    return list(persons), d


def find_guests(guests, scores):
    highest = 0
    for guest_list in permutations(guests, len(guests)):
        happiness = 0
        for i, guest in enumerate(guest_list[:-1]):
            happiness += scores[(guest, guest_list[i + 1])]
            happiness += scores[(guest_list[i + 1], guest)]
        happiness += scores[(guest_list[-1], guest_list[0])]
        happiness += scores[(guest_list[0], guest_list[-1])]
        if happiness > highest:
            highest = happiness
    return highest


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
    all_guests, scores = parse_instructions(instructions, part2)
    return find_guests(all_guests, scores)


if __name__ == '__main__':
    with open('instructions_day13.txt', 'r') as f:
        instructions = f.read().strip()
    print get_results(instructions, part2=False)
    print get_results(instructions, part2=True)
