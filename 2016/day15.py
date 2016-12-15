from time import time

def parse_instructions(instructions):
    disks = []
    for i, line in enumerate(instructions.split('\n')):
        words = line.split()
        num_positions = int(words[3])
        start_position = int(words[-1][:-1])
        disks.append((num_positions, start_position))
    return disks


def sim_disks(disks):
    end_state = []
    state = []
    sizes = []
    for i, (size, position) in enumerate(disks, 1):
        state.append(position)
        end_val = abs((size - i) % size)
        end_state.append(end_val)
        sizes.append(size)

    possible_states = reduce(lambda x, y: x * y, sizes)
    step = 0
    while True:
        step += 1
        state = [(x + 1) % disks[i][0] for i, x in enumerate(state)]
        if state == end_state:
            return step
        if step > possible_states:
            print 'uh oh'
            return


#stolen from reddit
def alt_sim(disks):
    step = -1
    while True:
        step += 1
        for i, (size, start) in enumerate(disks, 1):
            if (step + start + i) % size != 0:
                break
        else:
            return step


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
    disks = parse_instructions(instructions)
    if part2:
        disks.append((11, 0))
    return sim_disks(disks)
    return alt_sim(disks)


if __name__ == '__main__':
    with open('instructions_day15.txt', 'r') as f:
        instructions = f.read().strip()
    print sim_disks([(5, 4), (2, 1)])
    print get_results(instructions, part2=False)
    print get_results(instructions, part2=True)



