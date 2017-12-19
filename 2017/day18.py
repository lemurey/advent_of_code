from aoc_utilities import get_instructions
import os
from collections import deque, defaultdict


class Process:
    def __init__(self, instructions, pid):
        self.commands = [l.split() for l in instructions.split('\n')]
        self.registers = defaultdict(int)
        self.registers['p'] = pid
        self.index = 0
        self.functions = {'set': self.set,
                          'add': self.add,
                          'mul': self.mul,
                          'mod': self.mod,
                          'jgz': self.jgz,
                          'snd': self.snd,
                          'rcv': self.rcv}
        self.iterations = 0
        self.send_count = 0
        self.status = 'running'
        self.history = []

    def get(self, x):
        if x in 'abcdefghijklmnopqrstuvwxyz':
            return self.registers[x]
        return int(x)

    def snd(self, x):
        self.send_count += 1
        return self.get(x)

    def rcv(self, x):
        self.to_grab = x
        self.status = 'waiting'

    def set(self, x, y):
        self.registers[x] = self.get(y)

    def add(self, x, y):
        self.registers[x] += self.get(y)

    def mul(self, x, y):
        self.registers[x] *= self.get(y)

    def mod(self, x, y):
        self.registers[x] %= self.get(y)

    def jgz(self, x, y):
        x = self.get(x)
        if x > 0:
            self.index += (self.get(y) - 1)

    def run(self):
        while True:
            self.iterations += 1
            if self.index < 0 or self.index >= len(self.commands):
                self.status = 'END'
                return 'END'
            line = self.commands[self.index]
            self.history.append(line)
            self.index += 1
            if line[0] in ['snd', 'rcv']:
                return self.functions[line[0]](line[1])
            else:
                self.functions[line[0]](line[1], line[2])

    def recieve(self, y):
        self.registers[self.to_grab] = y
        self.status = 'running'


def get_answer(data, part2=False):
    ps = [Process(data, 0), Process(data, 1)]
    qs = [deque(), deque()]
    pid = 0

    if not part2:
        p = ps[0]  # only run 1 process
        sound = None
        while True:
            check = p.run()

            if p.status == 'running':
                sound = check  # save last sound played
            elif p.status == 'waiting':
                p.status = 'running'  # trick it to keep running
                if p.registers[p.to_grab] != 0:
                    return sound  # return sound first rcv with non-zero status

    while True:
        if ps[pid].status == 'END':  # process is over, switch to other
            if ps[1 - pid] == 'END':
                break  # both process over, stop iteration
            pid = 1 - pid
            continue

        check = ps[pid].run()

        if ps[pid].status == 'waiting':  # waiting for data
            if qs[1 - pid]:  # is there data to grab
                ps[pid].recieve(qs[1 - pid].popleft())
            else:  # switch to other process
                if len(qs[pid]) == 0 and ps[1 - pid].status == 'waiting':
                    break  # dealock (other process needs data it won't get)
                if ps[1 - pid].status == 'END':
                    break  # deadlock (this process needs data it won't get)
                ps[pid].index -= 1  # do not continue until get data
                pid = 1 - pid
        elif ps[pid].status == 'running':
            qs[pid].append(check)  # send value to other process

    return ps[1].send_count


if __name__ == '__main__':
    day = int(os.path.basename(__file__).split('.')[0].split('y')[1])
    inputs = get_instructions(day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
