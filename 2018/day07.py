from aoc_utilities import get_instructions
import os


def get_starts(data, base_time):
    steps = {}
    before = {}
    seen = {}
    times = {x: i + 1 for i, x in enumerate('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}

    for line in data:
        temp = line.split()
        req, after = temp[1], temp[-3]
        seen[req] = base_time + times[req]
        seen[after] = base_time + times[after]

        if after not in before:
            before[after] = set()
        before[after].add(req)

        if req not in steps:
            steps[req] = set()
        steps[req].add(after)

    start = sorted(set(steps.viewkeys() - before.viewkeys()))
    end = set([x for x in seen if x not in start])

    return start, end, steps, before, seen


def compare(end, done, before):
    to_remove = []
    for char in end:
        checks = before[char]
        if checks.intersection(done) == checks:
            to_remove.append(char)
    for char in to_remove:
        end.remove(char)
    return to_remove, end


def get_order(start, end, steps, before):
    done = set()
    out = ''

    while end:
        cur_char = start.pop(0)
        done.add(cur_char)
        out += cur_char

        updates, end = compare(end, done, before)

        start.extend(updates)
        start.sort()

    return out + ''.join(start)


def get_answer(data, part2=False):
    bt = 60
    num_workers = 5

    start, end, steps, before, times = get_starts(data, base_time=bt)
    if part2:
        workers = {i: ['', -1] for i in range(num_workers)}
    else:
        return get_order(start, end, steps, before)

    times[''] = 0

    s = 0
    done = set()
    while True:
        # get available jobs
        jobs = start[:]

        # get available workers
        to_work = [w for w in workers if workers[w][1] == -1]

        # are there any jobs left to do
        if (((len(jobs) + len(end)) == 0) and
            (len(to_work) == num_workers)):
            break

        # assign jobs do work and check for completion
        for worker, (job, time) in workers.items():
            if job == '':
                if len(jobs) > 0:
                    new_job = jobs.pop(0)
                    start.remove(new_job)
                else:
                    new_job = ''
                workers[worker] = [new_job, times[new_job] - 1]
            elif time == 1:
                done.add(job)
                workers[worker] = ['', -1]
            else:
                workers[worker][1] -= 1

        # add new jobs to start
        updates, end = compare(end, done, before)
        start.extend(updates)
        start.sort()

        s += 1

    return s


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
    inputs = get_instructions(year, day)


#     inputs = '''Step C must be finished before step A can begin.
# Step C must be finished before step F can begin.
# Step A must be finished before step B can begin.
# Step A must be finished before step D can begin.
# Step B must be finished before step E can begin.
# Step D must be finished before step E can begin.
# Step F must be finished before step E can begin.'''.split('\n')


    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))