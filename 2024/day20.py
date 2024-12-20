from aoc_utilities import get_instructions
from pathlib import Path
from heapq import heappush, heappop


def get_grid(data):
    grid = {}
    for y, row in enumerate(data):
        for x, val in enumerate(row):
            grid[(x, y)] = val
            if val == 'S':
                start = (x, y)
            elif val == 'E':
                end = (x, y)

    return grid, start, end


def neighbors(loc, grid):
    for dx,dy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
        nx, ny = loc[0] + dx, loc[1] + dy
        if (nx, ny) in grid:
            yield 1, (nx, ny)


def find_distances(grid, start, end):
    max_x = int(max(x[0] for x in grid))
    max_y = int(max(y[1] for y in grid))
    scores = {}
    for x in range(max_x + 1):
        for y in range(max_y + 1):
            p = (x, y)
            if grid[p] == '#':
                continue
            scores[p] = get_path(grid, p, end)
            if p == start:
                base_score = scores[p]
    return scores, base_score


def get_path(grid, start, end):
    costs = {}
    Q = []
    heappush(Q, (0, start))
    while Q:
        cost, loc = heappop(Q)
        if loc == end:
            return cost

        for score, next_loc in neighbors(loc, grid):
            if grid[next_loc] == '#': # no going through walls
                continue
            # if we have seen this loc before get it's cost
            # otherwise cost is infinity
            prev_cost = costs.get(next_loc, float('inf'))
            next_cost = cost + score

            # have we found a cheaper way to get to here
            if next_cost < prev_cost:
                costs[next_loc] = next_cost
                heappush(Q, (next_cost, next_loc))


def get_cheat_scores(scores, r):
    shortcut_scores = {}
    # iterate over all points on the path
    for (px, py), score in scores.items():
        # iterate over all points reachable in r steps
        for dx in range(-r, r + 1):
            for dy in range(-r, r + 1) :
                if abs(dx) + abs(dy) > r:
                    continue
                # get the score with the teleport standing in for shortcut
                # if it isn't in our dict of scores, then teleport is in
                # a wall, so call score 0 (should be infinite, but if you
                # use 0 instead, it makes the check easier)
                d_to_end = scores.get((px + dx, py + dy), 0)
                # how much did we save
                saved = d_to_end - abs(dx) - abs(dy) - score
                if saved not in shortcut_scores:
                    shortcut_scores[saved] = 0
                shortcut_scores[saved] += 1
    return shortcut_scores


def get_answer(data, part2=False):
    grid, start, end = get_grid(data)

    from time import time
    s_t = time()
    # calculate scores from all points on the path to the end
    scores, base_score = find_distances(grid, start, end)
    print(f'getting all scores took {time() - s_t:.2f}s')

    shortcut_scores = get_cheat_scores(scores, 2)

    # for k, v in sorted(shortcut_scores.items(), key=lambda x: x[0]):
    #     if k >= 50:
    #         print(f'there are {v} shortcuts that save {k} picoseconds')
    print(sum(v for k, v in shortcut_scores.items() if k >= 100))

    shortcut_scores = get_cheat_scores(scores, 20)

    # for k, v in sorted(shortcut_scores.items(), key=lambda x: x[0]):
    #     if k >= 50:
    #         print(f'there are {v} shortcuts that save {k} picoseconds')
    return sum(v for k, v in shortcut_scores.items() if k >= 100)

                



if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)

#     inputs = '''###############
# #...#...#.....#
# #.#.#.#.#.###.#
# #S#...#.#.#...#
# #######.#.#.###
# #######.#.#...#
# #######.#.###.#
# ###..E#...#...#
# ###.#######.###
# #...###...#...#
# #.#####.#.###.#
# #.#...#.#.#...#
# #.#.#.#.#.#.###
# #...#...#...###
# ###############'''.split('\n')

    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))



    # def cheat_check(loc, grid):
    #     for nx, ny in _neighbors(loc, grid):
    #         if grid[(nx, ny)] == '.':
    #             continue
    #         for nx2, ny2 in _neighbors((nx, ny), grid):
    #             if (nx2, ny2) == loc:
    #                 continue
    #             if grid[(nx2, ny2)] == '.':
    #                 yield (nx, ny), (nx2, ny2)


    # def find_cheats(grid):
    #     max_x = int(max(x[0] for x in grid))
    #     max_y = int(max(y[1] for y in grid))
    #     cheats = {}
    #     for x in range(max_x + 1):
    #         for y in range(max_y + 1):
    #             p = (x, y)
    #             if grid[p] == '#':
    #                 continue
    #             for cp, p2 in cheat_check(p, grid):
    #                 cheats[(p, p2)]= cp
    #     return cheats


    # def get_cheats(grid, start, end):
    #     cheats = find_cheats(grid)

    #     checks = {}
    #     for s, e in cheats:
    #         cheat = cheats[s, e]
    #         ordered = tuple(sorted((s, cheat, e)))
    #         if ordered not in checks:
    #             checks[ordered] = []
    #         checks[ordered].append((s, cheat, e))
    #     filtered = {}
    #     for v in checks.values():
    #         s, cheat, e = v[0]
    #         filtered[(s, e)] = cheat
    #     return filtered

    # def score_cheat(grid, cheat, start, end):
    #     ng = {k: v for k, v in grid.items()} 
    #     ng[cheat] = '.'
    #     return get_path(ng, start, end)

    # print(len(cheats))
    # base_score = get_path(grid, start, end)
    # print(base_score)
    # scores = {}
    # for i, (s, e) in enumerate(cheats):
    #     if i % 1000 == 0:
    #         print(f'at cheat {i}')
    #     cheat = cheats[s, e]
    #     score = score_cheat(grid, cheat, start, end)
    #     if score == base_score:
    #         continue
    #     saved = base_score - score
    #     if saved not in scores:
    #         scores[saved] = 0
    #     scores[saved] += 1

    # for k, v in sorted(scores.items(), reverse=True):
    #     print(base_score - k, v)

    # return sum(v for k, v in scores.items() if k >= 100  )