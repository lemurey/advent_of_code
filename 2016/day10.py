import re
from collections import defaultdict

NUMS = re.compile(r'-?\d+')
WHO = re.compile(r' (bot|output)')

def parse_instructions(instructions):
    bots = defaultdict(list)
    pipeline = {}
    for line in instructions.split('\n'):
        if 'value' in line:
            value, bot = map(int, NUMS.findall(line))
            bots[bot].append(value)
        else:
            bot, num1, num2 = map(int, NUMS.findall(line))
            which1, which2 = WHO.findall(line)
            pipeline[bot] = (which1, num1), (which2, num2)
    return bots, pipeline


def get_results(instructions):
    bots, pipeline = parse_instructions(instructions)
    output = {}
    while bots:
        bots, output = run_bots(bots, pipeline, output)
    return output[0] * output[1] * output[2]


def run_bots(bots, pipeline, output):
    to_delete = []
    to_add = []
    for bot, values in bots.iteritems():
        if len(values) == 2:
            to_delete.append(bot)
            value1, value2 = sorted(values)
            if (value1, value2) == (17, 61):
                print bot
            (which1, n1), (which2, n2) = pipeline[bot]
            if which1 == 'bot':
                to_add.append((n1, value1))
            else:
                output[n1] = value1
            if which2 == 'bot':
                to_add.append((n2, value2))
            else:
                output[n2] = value2
    update_bots(bots, to_delete, to_add)
    return bots, output


def update_bots(bots, del_list, add_list):
    for bot in del_list:
        del bots[bot]
    for bot, value in add_list:
        bots[bot].append(value)
    return bots


if __name__ == '__main__':
    with open('instructions_day10.txt', 'r') as f:
        instructions = f.read().strip()
    print get_results(instructions)