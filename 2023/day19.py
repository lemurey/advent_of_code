from aoc_utilities import get_instructions
from pathlib import Path
from functools import reduce


class Rule:
    def __init__(self, values):
        if isinstance(values, str):
            self.terminal = True
            self.loc = values
        else:
            self.terminal = False
            self.which = values[0]
            self.comp = values[1]
            self.value = int(values[2])
            self.loc = values[3]
    def __repr__(self):
        if self.terminal:
            return self.loc
        return f'{self.which}{self.comp}{self.value}:{self.loc}'
    def __str__(self):
        return self.__repr__()


def get_rules(data):
    rules = {}
    for line in data:
        if line == '':
            return rules
        name, rest = line.split('{')
        rest = rest.strip('}')
        rules[name] = []
        for entry in rest.split(','):
            if ':' not in entry:
                rules[name].append(Rule(entry))
            else:
                comp, loc = entry.split(':')
                rules[name].append(Rule((comp[0], comp[1], comp[2:], loc)))


def get_count(current_rule, rules, ranges=None):
    if ranges is None:
        ranges = dict(zip(('xmas'), ((1, 4000) for _ in range(4))))

    # ignore rejects
    if current_rule == 'R':
        return 0
    # multiply ranges
    if current_rule == 'A':
        return reduce(lambda x, y: x * ((y[1] - y[0]) + 1), ranges.values(), 1)

    cur_rules = rules[current_rule]

    total = 0
    for rule in cur_rules:
        if rule.terminal:
            total += get_count(rule.loc, rules, ranges)
        else:
            new_range = dict(ranges)
            check_range = ranges[rule.which]

            # is the new value in the current range
            if check_range[0] < rule.value < check_range[1]:
                # create the split groups
                if rule.comp == '<':
                    new_range[rule.which] = (check_range[0], rule.value - 1)
                    ranges[rule.which] = (rule.value, check_range[1])
                else:
                    new_range[rule.which] = (rule.value + 1, check_range[1])
                    ranges[rule.which] = (check_range[0], rule.value)

            total += get_count(rule.loc, rules, new_range)
    return total


def get_answer(data, part2=False):
    rules = get_rules(data)
    # for k, v in rules.items():
        # print(k, v)
    return get_count('in', rules)



if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''px{a<2006:qkq,m>2090:A,rfg}
# pv{a>1716:R,A}
# lnx{m>1548:A,A}
# rfg{s<537:gd,x>2440:R,A}
# qs{s>3448:A,lnx}
# qkq{x<1416:A,crn}
# crn{x>2662:A,R}
# in{s<1351:px,qqz}
# qqz{s>2770:qs,m<1801:hdj,R}
# gd{a>3333:R,R}
# hdj{m>838:A,pv}

# {x=787,m=2655,a=1222,s=2876}
# {x=1679,m=44,a=2067,s=496}
# {x=2036,m=264,a=79,s=2244}
# {x=2461,m=1339,a=466,s=291}
# {x=2127,m=1623,a=2188,s=1013}'''.split('\n')
    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))