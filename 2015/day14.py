from time import time

def parse_reindeer(instructions):
    reindeer = {}
    for line in instructions.split('\n'):
        words = line.split()
        name = words[0]
        speed = int(words[3])
        on_time = int(words[6])
        off_time = int(words[-2])
        reindeer[name] = (speed, on_time, off_time)
    return reindeer

def update(lst, val):
    lst.append(lst[-1] + val)
    return lst


def make_breakpoints(reindeer, race_time):
    breakpoints = {}
    status = {}
    options =['', 'on', 'off']
    cycles = 0
    for deer in reindeer:
        breakpoints[deer] = [0]
        status[deer] = ['off']
        time = reindeer[deer][1] + reindeer[deer][2]
        needed = race_time / time + 1
        if needed > cycles:
            cycles = needed
    for i in xrange(cycles * 2):
        index = i % 2 + 1
        for deer in reindeer:
            if breakpoints[deer][-1] >= race_time:
                continue
            breakpoints[deer] = update(breakpoints[deer], reindeer[deer][index])
            status[deer].append(options[index])
    for deer, lst in breakpoints.iteritems():
        breakpoints[deer] = set(lst)
    return breakpoints, status


def run_race(stats, race_time, part2):
    breakpoints, status = make_breakpoints(stats, race_time)
    positions = {deer : 0 for deer in stats}
    mode = {deer : 'off' for deer in stats}
    indices = {deer : 0 for deer in stats}
    if part2:
        score = {deer : 0 for deer in stats}

    for time in xrange(0, race_time):
        for deer in stats:
            if time in breakpoints[deer]:
                indices[deer] += 1
                if len(status[deer]) > indices[deer]:
                    mode[deer] = status[deer][indices[deer]]
            if mode[deer] == 'on':
                positions[deer] += stats[deer][0]
        if part2:
            lead = max(positions.values())

            for deer, position in positions.iteritems():
                if position == lead:
                    score[deer] += 1

    for deer in stats:
        if part2:
            print '{}: {}, {}'.format(deer, score[deer], positions[deer]) 
            output = score
        else:
            print '{}: {}'.format(deer, positions[deer])
            output = positions

    # print output.items()
    return max(output.items(), key=lambda x: x[1])


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
    race_time = 2503
    reindeer = parse_reindeer(instructions)
    return run_race(reindeer, race_time, part2)


if __name__ == '__main__':
    with open('instructions_day14.txt', 'r') as f:
        instructions = f.read().strip()
    print get_results(instructions, part2=False)
    print get_results(instructions, part2=True)
