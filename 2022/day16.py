from aoc_utilities import get_instructions
from pathlib import Path
import functools


def parse_instructions(data):
    tunnels = {}
    for row in data:
        v, c = row.split(';')
        rate = int(v.split('=')[-1])
        valve = v.split()[1]
        exits = ''.join(x for x in c if (x.isupper() or x == ',')).split(',')
        tunnels[valve] = (rate, exits)
    return tunnels


def calc_path(tunnels, start, end, path=None):
    if path is None:
        path = []
    path = path + [start]
    if start == end:
        return path
    shortest = None
    for o in tunnels[start][1]:
        if o not in path:
            newpath = calc_path(tunnels, o, end, path)
            if newpath:
                if not shortest or len(newpath) < len(shortest):
                    shortest = newpath
    return shortest


def calc_travel_times(tunnels):
    times = {}

    for s in tunnels:
        for e in tunnels:
            path = calc_path(tunnels, s, e)
            times[(s, e)] = len(path) - 1
    return times


@functools.lru_cache(maxsize=None)
def calc_flow(cur, opened, min_left):
    if min_left <= 0:
        return 0
    max_flow = 0
    if cur not in opened:
        val = (min_left - 1) * tunnels[cur][0]
        cur_opened = tuple(sorted(opened + (cur,)))
        for neighbor in tunnels[cur][1]:
            if val != 0:
                max_flow = max(max_flow,
                    val + calc_flow(neighbor, cur_opened, min_left - 2))
            max_flow = max(max_flow, calc_flow(neighbor, opened, min_left - 1))
    return max_flow


def get_paths(loc, budget, exclude=None):
    if exclude is None:
        exclude = set()
    if budget >= 1:
        yield (loc,)
    for cost, neighbor in times2[loc]:
        if neighbor in exclude:
            continue
        if budget >= cost + 2:
            for path in get_paths(neighbor, budget - cost - 1, exclude | {loc}):
                yield (loc,) + path


@functools.lru_cache(maxsize=None)
def get_flow(path, time):
    total_flow = 0
    for cur, dest in zip(path, path[1:]):
        # walk to destination and open valve
        time -= (times[cur, dest] + 1)
        total_flow += time * tunnels[dest][0]
    return total_flow


@functools.lru_cache(maxsize=None)
def part_2(cur, opened, min_left):
    if min_left <= 0:
        return calc_flow('AA', opened, 26)
    max_flow = 0
    if cur not in opened:
        val = (min_left - 1) * tunnels[cur][0]
        cur_opened = tuple(sorted(opened + (cur,)))
        for neighbor in tunnels[cur][1]:
            if val != 0:
                max_flow = max(max_flow,
                    val + part_2(neighbor, cur_opened, min_left - 2))
            max_flow = max(max_flow, part_2(neighbor, opened, min_left - 1))
    return max_flow



def get_answer(data, part2=False):
    global tunnels
    tunnels = parse_instructions(data)
    # global times
    # times = calc_travel_times(tunnels)

    print(calc_flow('AA', (), 30))

    return part_2('AA', (), 26)

    # keep = [x for x in tunnels if tunnels[x][0] > 0]
    # if 'AA' not in keep:
    #     keep = ['AA'] + keep
    # global times2
    # times2 = {}
    # for x in keep:
    #     if x not in times2:
    #         times2[x] = []
    #     for y in keep:
    #         if x == y:
    #             continue
    #         times2[x].append((times[x, y], y))

    # max_flow = 0
    # num_iters = 0
    # # get all of my paths
    # for path1 in get_paths('AA', 26, set()):
    #     # get flow of this path
    #     my_flow = get_flow(path1, 26)
    #     # get all elephant paths that are different than my current path
    #     for path2 in get_paths('AA', 26, exclude=set(path1)):
    #         num_iters += 1
    #         # get flow of this path
    #         ele_flow = get_flow(path2, 26)
    #         max_flow = max(max_flow, my_flow + ele_flow)
    #         if num_iters % 20000 == 0:
    #             print(num_iters)
    # print(num_iters)
    # return max_flow


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
    inputs = '''Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II'''.split('\n')
    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))
