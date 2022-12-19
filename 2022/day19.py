from aoc_utilities import get_instructions
from pathlib import Path
from collections import deque

MATERIALS = {'ore', 'clay', 'obsidian', 'geode'}


def parse_instructions(data):
    blueprints = {}
    parser = r'\d+'

    for line in data:
        label, rest = line.split(':')
        key = int(label.split(' ')[-1])
        blueprints[key] = {}
        for robot in rest.split('.'):
            if robot == '':
                continue
            vals = robot.split()
            which = vals[1]
            blueprints[key][which] = {}
            for word in vals[2:]:
                if word in MATERIALS:
                    blueprints[key][which][word] = value
                if word.isdigit():
                    value = int(word)
    return blueprints


def search_robot_space(blueprint, t=24):
    best = 0
    # (ore, clay, obisidian, geode, r_o, r_c, r_ob, r_g, time)
    state = (0, 0, 0, 0, 1, 0, 0, 0, t)

    cost_check = None

    Q = deque([state])
    seen = set()

    r_o_oc = blueprint['ore']['ore']
    r_c_oc = blueprint['clay']['ore']
    r_ob_oc = blueprint['obsidian']['ore']
    r_ob_cc = blueprint['obsidian']['clay']
    r_g_oc = blueprint['geode']['ore']
    r_g_obc = blueprint['geode']['obsidian']

    while Q:
        state = Q.popleft()
        o, c, ob, g, r_o, r_c, r_ob, r_g, t = state

        best = max(best, g)
        if t == 0:
            continue

        # trim values to reduce search space size

        # never makes sense to add robots when you generate more than
        # you can spend in a round
        max_ore = max(r_o_oc, r_c_oc, r_ob_oc, r_g_oc)
        add_ore = r_o < max_ore
        add_clay = r_c < r_ob_cc
        add_obsidian = r_ob < r_g_obc
        # r_o = min(r_o, max_ore)
        # r_c = min(r_c, r_ob_cc)
        # r_ob = min(r_ob, r_g_obc)
        # if you can't spend more of a resource in the remaing time
        # than you can generate then cap the value becuase it doesn't
        # impact the final geode count
        o = min(o, t * max_ore - r_o * (t-1))
        c = min(c, t * r_ob_cc - r_c * (t-1))
        ob = min(ob, t * r_g_obc - r_ob * (t-1))

        if state in seen:
            continue
        seen.add(state)

        if len(seen) % 1000000 == 0:
            print(t,best,len(seen))

        interupt_normal = False
        # if you can make geode robot do so no matter what
        if (o >= r_g_oc) and (ob >= r_g_obc):
            Q.append((o + r_o - r_g_oc, c + r_c,
                      ob + r_ob - r_g_obc, g + r_g,
                      r_o, r_c, r_ob, r_g + 1, t - 1))
            interupt_normal = True


        if interupt_normal:
            continue

        Q.append((o + r_o, c + r_c, ob + r_ob, g + r_g,
                  r_o, r_c, r_ob, r_g, t - 1))
        # make ore robot
        if (o >= r_o_oc) and add_ore:
            Q.append((o + r_o - r_o_oc, c + r_c, ob + r_ob, g + r_g,
                      r_o + 1, r_c, r_ob, r_g, t - 1))
        # make clay robot
        if (o >= r_c_oc) and add_clay:
            Q.append((o + r_o - r_c_oc, c + r_c, ob + r_ob, g + r_g,
                      r_o, r_c + 1, r_ob, r_g, t - 1))
        # make obsidian robot
        if (o >= r_ob_oc) and (c >= r_ob_cc) and add_obsidian:
            Q.append((o + r_o - r_ob_oc, c + r_c - r_ob_cc,
                      ob + r_ob, g + r_g,
                      r_o, r_c, r_ob + 1, r_g, t - 1))

    return best

def get_answer(data, part2=False):
    blueprints = parse_instructions(data)
    total = 0
    part2 = 1
    for num, b in blueprints.items():
        q = search_robot_space(b)
        # print(q)
        total += num * q
        if num <= 3:
            v = search_robot_space(b, 32)
            print(v)
            part2 *= v
    return total, part2


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.

# Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.'''.split('\n\n')
    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))
