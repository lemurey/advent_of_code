from aoc_utilities import get_instructions
import os
from collections import defaultdict


def parse(data):
    reactions = {}
    for line in data:
        inputs, outputs = line.split(' => ')
        ins = []
        for entry in inputs.split(', '):
            value, chemical = entry.split()
            ins.append((chemical, int(value)))
        for entry in outputs.split(', '):
            value, chemical = entry.split()

        if chemical not in reactions:
            reactions[chemical] = (int(value), ins)
        else:
            raise Exception('MORE THAN ONE RECIPE FOR CHEMICAL')
    return reactions


class Reactor:
    def __init__(self, recipes, desired_fuel=1):
        self.recipes = recipes
        self.needed = defaultdict(int)
        self.on_hand = defaultdict(int)
        self.consumed = defaultdict(int)
        self.needed['FUEL'] = desired_fuel

    def create_step(self, chemical, required):
        num_per_process, process = self.recipes[chemical]

        current = self.on_hand[chemical]
        multiplier = 0
        generated = 0
        while (generated + current) < required:
            multiplier += 1
            generated += num_per_process

        for chemical2, amount in process:
            self.needed[chemical2] += (amount * multiplier)

        self.on_hand[chemical] += generated

    def consume_step(self, chemical, num):
        self.needed[chemical] -= num
        self.on_hand[chemical] -= num
        self.consumed[chemical] += num

    def _check(self):
        c1 = sum([x for k, x in self.needed.items() if k != 'ORE'])
        c2 = all([x >= 0 for x in self.on_hand.values()])
        return (c1 == 0) and c2

    def run(self):
        while not self._check():
            prev = {k: v for k, v in self.needed.items()}
            for chemical, num_needed in prev.items():
                if num_needed == 0 or chemical == 'ORE':
                    continue
                self.create_step(chemical, num_needed)
                self.consume_step(chemical, num_needed)


def react(recipes, on_hand, chemical, desired):

    current = on_hand[chemical]
    if current >= desired:
        return True
    if chemical == 'ORE':
        return False

    num_per_process, process = recipes[chemical]
    n, r = divmod(desired - current, num_per_process)
    if r == 0:
        multiplier = n
    else:
        multiplier = n + 1
    reacted = True
    for chemical2, amount in process:
        to_get = multiplier * amount
        reacted = reacted and react(recipes, on_hand, chemical2, to_get)
        on_hand[chemical2] -= to_get
    if reacted:
        on_hand[chemical] += multiplier * num_per_process
    return reacted


def search(recipes, max_val):
    low = 0
    high = max_val
    while low < high - 1:
        mid = (low + high) // 2
        on_hand = {k: 0 for k in recipes}
        on_hand['ORE'] = max_val

        if react(recipes, on_hand, 'FUEL', mid):
            low = mid
        else:
            high = mid - 1

    if react(recipes, on_hand, 'FUEL', high):
        return high
    return low


def get_answer(data, part2=False):
    recipes = parse(data)
    r = Reactor(recipes)
    r.run()
    if part2:
        num = 1000000000000
        return search(recipes, num)

    return r.needed['ORE']


if __name__ == '__main__':
    year, day = os.path.realpath(__file__).split('/')[-2:]
    day = int(day.split('.')[0].split('y')[1])
    inputs = get_instructions(year, day)
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
