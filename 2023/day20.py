from aoc_utilities import get_instructions
from pathlib import Path
from math import lcm


class FlipFlop():
    def __init__(self, name, connections):
        self.low = 0
        self.high = 0
        self.name = name
        self.state = 0
        self.connections = connections

    def __call__(self, pulse, _):
        # if pulse is high ignore it
        if pulse:
            return None
        # pulse is low, change state
        self.state = (self.state + 1) % 2
        for c in self.connections:
            if self.state:
                self.high += 1
                yield c, 1, self.name
            else:
                self.low += 1
                yield c, 0, self.name


class Conjunction():
    def __init__(self, name, modules, connections):
        self.low = 0
        self.high = 0
        self.name = name
        self.memory = {m: None for m in modules}
        self.connections = connections

    def __call__(self, pulse, module):
        self.memory[module] = pulse
        for c in self.connections:
            if all(self.memory.values()):
                self.low += 1
                yield c, 0, self.name
            else:
                self.high += 1
                yield c, 1, self.name


class BroadCaster():
    def __init__(self, name, connections):
        self.low = 0
        self.high = 0
        self.name = name
        self.connections = connections

    def __call__(self, pulse):
        for c in self.connections:
            if pulse:
                self.high += 1
            else:
                self.low += 1
            yield c, pulse, self.name


class Reciever():
    def __init__(self, name):
        self.name = name
        self.low = 0
        self.high = 0

    def __call__(self, pulse, connections):
        return None


class System():
    def __init__(self, modules):
        self.modules = modules
        self.checks = {'kr': None, 'zs': None, 'kf': None, 'qk': None}

    def __call__(self):
        sending = list(self.modules['broadcaster'](0))
        while sending:
            new = []
            for dest, pulse, sender in sending:
                # print(dest, pulse, sender)
                if dest in self.checks and not pulse:
                    self.checks[dest] = 1
                check = self.modules[dest](pulse, sender)
                if check:
                    new.extend(list(check))
            sending = new
            # print(sending)

    def count(self):
        low = 1
        high = 0
        for m in self.modules.values():
            low += m.low
            high += m.high
            m.low = 0
            m.high = 0
        return low, high


def make_system(data):
    modules = {}
    conjunctions = set()
    system = {}
    for line in data:
        module, connections = line.split(' -> ')
        c = connections.split(', ')
        if module[0] == '%':
            modules[module[1:]] = c
        elif module[0] == '&':
            modules[module[1:]] = {'in': [], 'out': c}
            conjunctions.add(module[1:])
        else:
            modules['broadcaster'] = c
    adds = {}
    for m in modules:
        if m in conjunctions:
            conns = modules[m]['out']
        else:
            conns = modules[m]
        for c in conns:
            if c in conjunctions:
                modules[c]['in'].append(m)
            if c not in modules:
                adds[c] = Reciever(c)

    for m in modules:
        if m in conjunctions:
            system[m] = Conjunction(m, modules[m]['in'], modules[m]['out'])
        elif m == 'broadcaster':
            system[m] = BroadCaster(m, modules[m])
        else:
            system[m] = FlipFlop(m, modules[m])

    system.update(adds)
    return System(system)



def get_answer(data, part2=False):
    system = make_system(data)
    counts = []

    if part2:
        iters = 0
        # these are the keys that trigger rx going positive
        # all need to be 1 at once, will grab cycles with the state
        # in system
        tracker = {'kr': None, 'zs': None, 'kf': None, 'qk': None}
        while True:
            iters += 1
            system()
            for k in tracker:
                if system.checks[k] == 1 and tracker[k] is None:
                    tracker[k] = iters

            if all(tracker.values()):
                return lcm(*tracker.values())
            if iters % 5000 == 0:
                print(f'at iteration {iters}')
                break

        for k in ('kr', 'zs', 'kf', 'qk'):
            print(system.modules[k].low, system.modules[k].high)
        return

    for i in range(1000):
        c = system()
        if c == "STOP":
            print(i)
        low, high = system.count()
        counts.append((low, high))

    print(len(counts))
    tl = sum(c[0] for c in counts)
    th = sum(c[1] for c in counts)
    return tl * th



if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''broadcaster -> a, b, c
# %a -> b
# %b -> c
# %c -> inv
# &inv -> a'''.split('\n')
#     inputs = '''broadcaster -> a
# %a -> inv, con
# &inv -> b
# %b -> con
# &con -> output'''.split('\n')
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
