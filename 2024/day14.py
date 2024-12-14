from aoc_utilities import get_instructions
from pathlib import Path


def get_robots(data):
    robots = []
    for line in data:
        _, p, v = line.split('=')
        x, y = map(int, p.strip(' v').split(','))
        vx, vy = map(int, v.strip().split(','))
        robots.append([(x, y), (vx, vy)])
    return robots


def sim_robot(robot, max_x, max_y, steps, return_quadrant=True, verbose=False):
    (x, y), (vx, vy) = robot
    nx, ny = x, y
    for _ in range(steps):
        nx = (nx + vx) % max_x
        ny = (ny + vy) % max_y
        if verbose:
            print(nx, ny)
    if return_quadrant:
        return get_quadrant(nx, ny, max_x, max_y)
    return (nx, ny)


def get_quadrant(x, y, max_x, max_y):
    half_x = max_x // 2
    half_y = max_y // 2
    q1x = range(half_x)
    q2x = range(half_x + 1, max_x)
    q1y = range(half_y)
    q2y = range(half_y + 1, max_y)

    if x in q1x and y in q1y:
        return 1
    if x in q1x and y in q2y:
        return 3
    if x in q2x and y in q1y:
        return 2
    if x in q2x and y in q2y:
        return 4
    return None


def run_part2(robots, max_x, max_y):
    cur_bots = [p for p,v in robots]

    for s in range(10000):
        bot_pos = set()
        for i, robot in enumerate(robots):
            (_, _), (vx, vy) = robot
            x, y = cur_bots[i]
            nx = (x + vx) % max_x
            ny = (y + vy) % max_y
            bot_pos.add((nx, ny))
            cur_bots[i] = (nx, ny)

        if len(bot_pos) == len(cur_bots):
            write_bots(cur_bots, max_x, max_y, s+1)


def write_bots(cur_bots, max_x, max_y, s):
    cb = set(cur_bots)
    with open(f'bots/bots_{s}', 'w') as f:
        for y in range(max_y):
            line = ''
            for x in range(max_x):
                if (x, y) in cb:
                    line += '*'
                else:
                    line += '.'
            f.write(line + '\n')


def get_answer(data, part2=False):
    max_x, max_y = (101, 103)

    robots = get_robots(data)

    if part2:
        run_part2(robots, max_x, max_y)
        return

    quadrants = {1: 0, 2: 0, 3: 0, 4: 0, None: 0}
    for robot in robots:
        quad = sim_robot(robot, max_x, max_y, 100)
        quadrants[quad] += 1

    out = 1
    for k, v in quadrants.items():
        if k is None:
            continue
        out *= v
    return out


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
