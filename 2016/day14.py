import re
from hashlib import md5
from time import time

def compute_hash(string, count):
    return md5('{}{}'.format(string, count)).hexdigest()


def advanced_hashes(string, count):
    temp_hash = compute_hash(string, count)
    for _ in xrange(2016):
        temp_hash = compute_hash(temp_hash, '')
    return temp_hash


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
    hash_checks = {}
    keys = []
    count = 0
    checker = re.compile(r'(\w)\1\1')
    to_remove = -1
    while len(keys) < 64:

        if part2:
            hashed = advanced_hashes(instructions, count)
        else:
            hashed = compute_hash(instructions, count)

        match = checker.search(hashed)
        if match:
            string = r'({})\1{{4}}'.format(match.group(1))
            hash_checks[count] = re.compile(string)

        for k, regex in hash_checks.iteritems():
            if k < count and count <= k + 1000:
                if regex.search(hashed):
                    keys.append(k)
            elif count > k + 1000:
                to_remove = k

        if to_remove in hash_checks:
            del hash_checks[to_remove]

        count += 1
        
    return len(keys), count, sorted(keys)[63]


if __name__ == '__main__':
    with open('instructions_day14.txt', 'r') as f:
        instructions = f.read().strip()

    print get_results(instructions, part2=False)
    print get_results(instructions, part2=True)
