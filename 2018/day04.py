from aoc_utilities import get_instructions
import os
import re
from collections import Counter


def parse_line(line):
    return map(int, re.findall(r'\d+', line))


def parse_file(data):
    times = []
    for line in data:
        temp = parse_line(line)
        if len(temp) == 5:
            _, month, day, hour, minute = temp
            guard = 'unknown'
        else:
            _, month, day, hour, minute, guard = temp
        action = line.split()[-1]
        times.append((month, day, hour, minute, guard, action))
    sorted_times = sorted(times, key=lambda x: (x[0], x[1], x[2], x[3]))
    prev_guard = None
    final = []
    for month, day, hour, minute, guard, action in sorted_times:
        if guard == 'unknown' and prev_guard is not None:
            update = (month, day, hour, minute, prev_guard, action)
        elif action == 'shift':
            prev_guard = guard
        final.append((month, day, hour, minute, prev_guard, action))
    return final


def follow_guards(sorted_times):
    guards = {}
    prev_action = None
    for month, day, _, minute, guard, action in sorted_times:
        if action == 'shift':
            cur_guard = guard
            start = -1
            stop = -1
            if cur_guard not in guards:
                guards[cur_guard] = Counter()
        elif action == 'asleep':
            start = minute
        else:
            stop = minute
        if stop != -1 and start != -1:
            for minute in range(start, stop):
                guards[cur_guard][minute] += 1
            stop = -1
            start = -1
    return guards


def get_answer(data, part2=False):
    lines = parse_file(data)
    guards = follow_guards(lines)
    max_time = 0
    max_check = 0
    for k, v in guards.iteritems():
        cur_time = sum(v.values())
        if len(v) > 0:
            check_2 = v.most_common()[0][1]
        else:
            check_2 = 0
        if cur_time > max_time:
            max_time = cur_time
            value = (k * v.most_common()[0][0])
        if check_2 > max_check:
            max_check = check_2
            value_2 = (k * v.most_common()[0][0])
    return value, value_2


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs))
