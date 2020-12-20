from aoc_utilities import get_instructions
from pathlib import Path
import re

from collections import defaultdict


def chunker(line, step_size=8):
    prev = 0

    for n in range(8, len(line) + step_size, step_size):
        chunk = line[prev:n]
        yield chunk
        prev = n


def parse_input(data):
    rules = {}
    base_rules = set()
    messages = []
    for row in data:
        if ':' in row:
            num, rule = row.split(': ')
            num = int(num)
            if '"' in rule:
                rules[num] = [rule.strip('"')]
                base_rules.add(num)
            elif '|' in rule:
                left, right = rule.split(' | ')
                rules[num] = (list(map(int, left.split())),
                              list(map(int, right.split())))
            else:
                rules[num] = (list(map(int, rule.split())), )
        elif row == '':
            continue
        else:
            messages.append(row)

    return messages, rules, base_rules


def process_sub(sub, rules, verbose=False):
    out = ''
    for n in sub:
        if verbose:
            print(n, rules[n])
        s = rules[n][0]
        if len(s) == 1:
            out += s
        else:
            out += f'({s})'
    return out


def process_contained_rules(rules, base_rules, verbose=False):
    new_rules = {}
    for n, rule in rules.items():
        if n in base_rules:
            new_rules[n] = rule
        new_rule = []
        for sub in rule:
            check = [x in base_rules for x in sub]
            if all(check):
                new_sub = process_sub(sub, rules, verbose)
                new_rule.append(new_sub)
            else:
                new_rule.append(sub)
        new_rules[n] = new_rule
    return new_rules


def colapse_subs(rules):
    new_rules = {}
    for n, rule in rules.items():
        if len(rule) == 1:
            new_rules[n] = rule
        else:
            c = 0
            for sub in rule:
                if isinstance(sub, str):
                    c += 1

            if c == len(rule):
                new_rules[n] = ['|'.join(rule)]
            else:
                new_rules[n] = rule

    return new_rules


def check_for_new_base_rules(rules):
    base_rules = set()
    for n, rule in rules.items():
        if len(rule) == 1 and isinstance(rule[0], str):
            base_rules.add(n)
    return base_rules


def full_process(messages, rules, base_rules):
    while not isinstance(rules[0][0], str):
        rules = process_contained_rules(rules, base_rules)
        rules = colapse_subs(rules)
        base_rules = check_for_new_base_rules(rules)

    return rules




'''
if add_loops and n == '8':
    return '(?P<eight>{0}|{0}(?&eight))'.format(dfs("42"))
if add_loops and n == '11':
    return '(?P<eleven>{0}{1}|{0}(?&eleven){1})'.format(dfs("42"), dfs("31"))
'''


def get_answer(data, part2=False):
    messages, rules, base_rules = parse_input(data)

    rules = full_process(messages, rules, base_rules)


    if not part2:
        regex = re.compile(f'^{rules[0][0]}$')
        return sum([1 if regex.match(x) else 0 for x in messages])
    else:

        r42 = re.compile(f'{rules[42][0]}')
        r31 = re.compile(f'{rules[31][0]}')

        '''
        the way the updated rules work is similar to the regex below

        (I wrote the regex below based on example in the problem, it works for
        that example, but fails on my actual input)

        you have rule 42 any number of times (thats rule 8)
        followed by the same thing rule 42+, and then ending with rule 31+

        However, the regex below misses an important point, there has to be
        more 42 matches than 31 matches, because the updated rule 11 will have
        matched groups of 42 and 31, and then you needed at least one 8 match
        at the beginning

        i checked, and both 42 and 31 always match 8 character long groupings.
        so first I check the regex below (if a line doesn't match it is invalid)
        then i go over those lines in chunks of 8 characters, and I see which of
        42 or 31 it matches, then I only count matches where there are more
        42 matches in the line than 31. I am reasonably confident I could write
        a regex that does this, but I am too tired to try and think of it now
        '''
        regex = re.compile(f'(?P<r8>{rules[42][0]})+'
                           f'(?P<r42>{rules[42][0]})+'
                           f'(?P<r31>{rules[31][0]})+$')

        c = 0
        for line in messages:
            if not regex.match(line):
                continue

            count_42 = 0
            count_31 = 0

            for chunk in chunker(line):
                if r42.match(chunk):
                    count_42 += 1
                if r31.match(chunk):
                    count_31 += 1

            if count_42 > count_31:
                c += 1

        return c


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)

#     inputs = '''0: 4 1 5
# 1: 2 3 | 3 2
# 2: 4 4 | 5 5
# 3: 4 5 | 5 4
# 4: "a"
# 5: "b"

# ababbb
# bababa
# abbbab
# aaabbb
# aaaabbb'''.split('\n')

#     inputs = '''42: 9 14 | 10 1
# 9: 14 27 | 1 26
# 10: 23 14 | 28 1
# 1: "a"
# 11: 42 31
# 5: 1 14 | 15 1
# 19: 14 1 | 14 14
# 12: 24 14 | 19 1
# 16: 15 1 | 14 14
# 31: 14 17 | 1 13
# 6: 14 14 | 1 14
# 2: 1 24 | 14 4
# 0: 8 11
# 13: 14 3 | 1 12
# 15: 1 | 14
# 17: 14 2 | 1 7
# 23: 25 1 | 22 14
# 28: 16 1
# 4: 1 1
# 20: 14 14 | 1 15
# 3: 5 14 | 16 1
# 27: 1 6 | 14 18
# 14: "b"
# 21: 14 1 | 1 14
# 25: 1 1 | 1 14
# 22: 14 14
# 8: 42
# 26: 14 22 | 1 20
# 18: 15 15
# 7: 14 5 | 1 21
# 24: 14 1

# abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
# bbabbbbaabaabba
# babbbbaabbbbbabbbbbbaabaaabaaa
# aaabbbbbbaaaabaababaabababbabaaabbababababaaa
# bbbbbbbaaaabbbbaaabbabaaa
# bbbababbbbaaaaaaaabbababaaababaabab
# ababaaaaaabaaab
# ababaaaaabbbaba
# baabbaaaabbaaaababbaababb
# abbbbabbbbaaaababbbbbbaaaababb
# aaaaabbaabaaaaababaa
# aaaabbaaaabbaaa
# aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
# babaaabbbaaabaababbaabababaaab
# aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba'''.split('\n')

    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
