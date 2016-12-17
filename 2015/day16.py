from time import time

MATCH = {'children': 3,
         'cats': 7,
         'samoyeds': 2,
         'pomeranians': 3,
         'akitas': 0,
         'vizslas': 0,
         'goldfish': 5,
         'trees': 3,
         'cars': 2,
         'perfumes': 1}


def get_sues(data):
    sues = []
    for line in data.split('\n'):
        info = ':'.join(line.split(': ')[1:])
        cur_sue = {}
        for temp in info.split(', '):
            feature, value = temp.split(':')
            cur_sue[feature] = int(value)
        sues.append(cur_sue)
    return tuple(sues)

def score_sue(sue, part2):
    score = 0
    for category, value in sue.iteritems():
        t_val = MATCH[category]
        if part2 and category in ['cats', 'trees']:
            score += abs(t_val - min(value, t_val))
        elif part2 and category in ['pomeranians', 'goldfish']:
            score += abs(t_val - max(value, t_val))
        else:
            score += abs(t_val - value)
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
    sues = get_sues(instructions)
    min_score = 10000000
    best_matches = []
    for index, sue in enumerate(sues):
        if sue == MATCH and not part2:
            return index + 1
        score = score_sue(sue, part2)
        if score <= min_score:
            min_score = score
            best_matches.append(index + 1)
    return best_matches[-1]


if __name__ == '__main__':
    with open('instructions_day16.txt', 'r') as f:
        instructions = f.read().strip()
    print get_results(instructions, part2=False)
    print get_results(instructions, part2=True)