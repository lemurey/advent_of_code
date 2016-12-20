from utilities import timeit

def parse_instructions(instructions):
    output = []
    for line in instructions.split('\n'):
        start, end = map(int, line.split('-'))
        output.append((start, end))
    return sorted(output, key=lambda x: x[0])


def get_continous_ranges(limits):
    '''limits is sorted by first value'''
    cur_range = [limits[0][0], limits[0][1]]
    ranges = [cur_range]
    for first, second in limits[1:]:
        if first <= (cur_range[1] + 1) and second > cur_range[1]: #extend range
            cur_range[1] = second
        elif first > cur_range[1]: #a separate range
            cur_range = [first, second]
            ranges.append(cur_range)
    return ranges


def get_min_allowed(limits):
    min_val = 0
    for first, second in limits:
        if first == min_val or (first < min_val and second >= min_val):
            min_val = second + 1
    return min_val


def get_number_allowed(ranges):
    collapsed = get_continous_ranges(ranges)
    p_end = collapsed[0][1]
    allowed = 0
    max_val = 4294967295
    for entry in collapsed[1:]:
        allowed += (entry[0] - p_end - 1)
        p_end = entry[1]
    if max_val > p_end:
        allowed += max_val - p_end - 1
    return allowed


@timeit
def get_results(instructions, part2=False):
    ranges = parse_instructions(instructions)
    if part2:
        return get_number_allowed(ranges)
    else:
        return get_min_allowed(ranges)


if __name__ == '__main__':
    with open('instructions_day20.txt', 'r') as f:
        instructions = f.read().strip()
    print get_results(instructions, part2=False)
    print get_results(instructions, part2=True)
