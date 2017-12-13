from aoc_utilities import get_instructions
import os


class Firewall:
    def __init__(self, data):
        self.setup = {}
        self.state = {}
        self._process_data(data)
        self.location = 0
        self.severity = 0
        self.size = max(self.setup)

    def _process_data(self, data):
        for line in data.split('\n'):
            key, value = line.split(': ')
            key = int(key)
            value = int(value)
            self.state[key] = 0
            self.setup[key] = (value, 1)

    def _advance_1(self):
        for layer, (l_range, direction) in self.setup.items():
            current = self.state[layer]
            current = current + direction * 1
            if current == l_range:
                self.setup[layer] = (l_range, -1 * direction)
            self.state[layer] = current

    def _update_severity(self):
        if self.state[self.location] == 0:
            self.severity += self.location * self.setup[self.location][0]

    def run(self):
        while self.location <= self.size:
            if self.location in self.state:
                self._update_severity()
            self._advance_1()
            self.location += 1
        return self.severity

    # def _print_state(self):
    #     locs = [0 for _ in range(self.size)]
    #     print('Picosecond {}'.format(self.location))
    #     print(''.join(' {} '.format(x) for x in range(self.size)))
    #     line_string = '{}' * self.size
    #     for index, location in self.state.items():
    #         locs[index] = location
    #     for i in range(self.size):
    #         vals = []
    #         for j in range(self.size):

    #         if i not in self.setup:

    #         if locs[i]



def get_answer(data, part2=False):
    firewall = Firewall(data)
    return firewall.run()


if __name__ == '__main__':
    day = int(os.path.basename(__file__).split('.')[0].split('y')[1])
    test='''0: 3
1: 2
4: 4
6: 4'''
    print(get_answer(test))
    # inputs = get_instructions(day)
    # print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))
