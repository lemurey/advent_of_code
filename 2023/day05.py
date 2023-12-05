from aoc_utilities import get_instructions
from pathlib import Path

'''
the transformations are piecewise linear, so there exists a series of ranges
[a, b) such that b - a = t(b) - t(a). Becuase of this the minimum across all
such edges will be one of the extrema.
so what I do for part 2 is search the seed ranges to find edges
(values of a and b above) and then I only need to run the transformation on those
edges to get the minimum

I started trying to get the above to work, but couldn't. While I was doing it
I had the thought that you could just pass the seed ranges in, get the possible
overlaps between the seed range and the transformation range (left, middle, right)
and then build up a set of all possible output ranges. then you need to grab
the minimum such output. This didn't work for me and I'm not sure why, I have
checked the reddit and this is the approach many others took, so I'm not sure
what I did wrong with it.

Eventually I realized how to make my edge finding work properly and I got the
searching edges process to give the correct answer
'''


def step(cmap, value):
    for destination, source, length in cmap:
        if source <= value < (source + length):
            return destination + (value - source)
    return value


def process_data(data):
    maps = {}
    cur_map = None

    for line in data:
        if line.startswith('seeds'):
            _, seeds = line.split(': ')
            seeds = list(map(int, seeds.split()))
        elif line == '':
            continue
        elif line.endswith('map:'):
            cur_map = line.strip(' map:')
            maps[cur_map] = []
        else:
            dest, source, length = map(int, line.split())
            maps[cur_map].append((dest, source, length))
    return seeds, maps


def run_process(seeds, maps, ret_all=False, debug=False):
    process = ('seed-to-soil', 'soil-to-fertilizer', 'fertilizer-to-water',
               'water-to-light', 'light-to-temperature', 'temperature-to-humidity',
               'humidity-to-location')
    current = [x for x in seeds]
    for which in process:
        for i, seed in enumerate(seeds):
            current[i] = step(maps[which], seed)
        seeds = current[:]
        if debug:
            print(seeds)
    if ret_all:
        return seeds
    return min(seeds)

## not sure why this didn't work
# def run_range(ranges, maps):
    # '''
    # explaining to myself to make sure I get what I'm trying to do:
    # for every seed range, modify the minimum possible value by the offset for
    # that maps delta.
    # so if the seed, transformation have ranges
    # [a, b), [c, d)
    # we modify the range [max(a, c), min(b, d)) to be
    # [max(a, c) - offset, min(b, d) - offset)
    # where offset is the value (destination - source) for that transformation step

    # we also store the ranges above/below the overlap of seed/transformation so
    # we keep track of possiblities where intermediate ranges are not transformed
    # but end up in the lowest final output
    # '''
#     process = ('seed-to-soil', 'soil-to-fertilizer', 'fertilizer-to-water',
#                'water-to-light', 'light-to-temperature', 'temperature-to-humidity',
#                'humidity-to-location')
#     all_ranges = []
#     ff = open('mine_log.txt', 'w')
#     for which in process:
#         for (destination, source, length) in maps[which]:
#             new_ranges = []
#             source_end = source + length
#             for (start, end) in ranges:
#                 # get everything before the start of transformation
#                 if start < source:
#                     left = (start, min(end, source))
#                     new_ranges.append(left)
#                 # get everything after the end of transformation
#                 if end > source_end:
#                     right = (max(start, source_end), end)
#                     new_ranges.append(right)

#                 # check for overlaps (I think these 4 cover everything)
#                 # source is in between start/end
#                 c1 = start <= source <= end
#                 # source end is in between start/end
#                 c2 = start <= source_end <= end
#                 # start is in between source and source_end
#                 c3 = source <= start <= source_end
#                 # end is in between source and source_end
#                 c4 = source <= end <= source_end

#                 # apply the transformation before appending this
#                 if c1 or c2 or c3 or c4:
#                     middle = (max(start, source), min(end, source_end))
#                     new_middle = tuple(destination + (x - source) for x in middle)
#                     # new_ranges.append(new_middle)
#             ranges = new_ranges[:]
#             all_ranges.extend(ranges)
#         # new_ranges.extend(ranges)
#         # ranges = new_ranges

#     for e in ranges:
#         ff.write(f'{e}\n')

#     return ranges


def edge_check(val, maps):
    l, h = run_process([val - 1, val + 1], maps, ret_all=True)
    if (h - l) == 2:
        return False
    return True


def search(l, r, maps):
    if l >= r:
        return
    vl = run_process([l], maps)
    vr = run_process([r], maps)
    ## if the range from left/right is same as outputs, no edges in between left/right
    ## and we can stop
    if (vr - vl) == (r - l):
        return

    ## get the center of range and process that
    c = int((r + l) / 2)
    vc = run_process([c], maps)

    # check for edges in (l, c, r)
    for val in (l-1, l):
        if edge_check(val, maps):
            yield val
    for val in (c-1, c, c+1):
        if edge_check(val, maps):
            yield val
    for val in (r, r+1):
        if edge_check(val, maps):
            yield val

    # if there is in edge in the left/right side, search that side
    if (vc - vl) != (c - l):
        yield from search(l+1, c-2, maps)
    if (vr - vl) != (r - c):
        yield from search(c+2, r-1, maps)


def get_answer(data, part2=False):
    seeds, maps = process_data(data)

    if part2:
        cands = set()
        for start, stop in zip(seeds[::2], seeds[1::2]):
            for cand in search(start, start + stop, maps):
                if edge_check(cand, maps):
                    cands.add(cand)
        seeds = sorted(cands)
    return run_process(seeds, maps)


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''seeds: 79 14 55 13

# seed-to-soil map:
# 50 98 2
# 52 50 48

# soil-to-fertilizer map:
# 0 15 37
# 37 52 2
# 39 0 15

# fertilizer-to-water map:
# 49 53 8
# 0 11 42
# 42 0 7
# 57 7 4

# water-to-light map:
# 88 18 7
# 18 25 70

# light-to-temperature map:
# 45 77 23
# 81 45 19
# 68 64 13

# temperature-to-humidity map:
# 0 69 1
# 1 0 69

# humidity-to-location map:
# 60 56 37
# 56 93 4'''.split('\n')
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
