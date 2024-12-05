from aoc_utilities import get_instructions
from pathlib import Path


def process_rules(data):
    before = {}
    after = {}
    second = False
    rules = []
    for line in data:
        if line == '':
            second = True
            continue
        if second:
            rules.append(list(map(int, line.split(','))))
        else:
            b, a = map(int, line.split('|'))
            if b not in before:
                before[b] = []
            if a not in after:
                after[a] = []
            before[b].append(a)
            after[a].append(b)

    return before, after, rules


def _c(others, value, checks):
    if value not in checks:
        to_check = []
    else:
        to_check = checks[value]
    for val in others:
        if val not in to_check:
            return val
    return None


def check(rule, before, after):
    for i, val in enumerate(rule):
        b = rule[:i]
        a = rule[i+1:]
        # there are pages before the value being checked, so we check them
        # against the after ruleset
        if b != []:
            check_val = _c(b, val, after)
            if check_val is not None:
                return i, check_val
        # there are pages after the value being checked, so we check them
        # agains the before ruleset
        if a != []:
            check_val = _c(a, val, before)
            if check_val is not None:
                return i, check_val
    return None


def fix(rule, before, after, count=0):
    # if it passes then return the rule
    check_val = check(rule, before, after)
    if check_val is None:
        return rule
    # if it didn't pass, then we need to flip a value
    # take the index that failed and flip it with the value it failed against

    new_rule = rule[:]
    cur_val = rule[check_val[0]]
    cur_index = rule.index(check_val[1])

    new_rule[check_val[0]] = check_val[1]
    new_rule[cur_index] = cur_val

    # make it break if it's stuck in a loop
    if count > 500:
        return
    return fix(new_rule, before, after, count+1)


def get_answer(data, part2=False):
    before, after, rules = process_rules(data)
    total = 0
    total2 = 0
    for rule in rules:
        index = len(rule) // 2
        check_val = check(rule, before, after)
        if check_val is None:
            total += rule[index:index+1][0]
        else:
            new = fix(rule, before, after)
            total2 += new[index:index+1][0]
    return total, total2


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''47|53
# 97|13
# 97|61
# 97|47
# 75|29
# 61|13
# 75|53
# 29|13
# 97|29
# 53|29
# 61|53
# 97|53
# 61|29
# 47|13
# 75|47
# 97|75
# 47|61
# 75|61
# 47|29
# 75|13
# 53|13

# 75,47,61,53,29
# 97,61,53,29,13
# 75,29,13
# 75,97,47,61,53
# 61,13,29
# 97,13,75,29,47'''.split('\n')
    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))
