import numpy as np

class Lightsnp(object):
        def __init__(self, x=1000, y=1000, options=None):
            self.grid = np.zeros((x, y))
            if not options:
                self.options = {'on' : lambda x: 1,
                                'off' : lambda x: 0,
                                'toggle' : lambda x: 1 - x}
            else:
                self.options = options

        def __call__(self, line):
            temp = line.split()
            if temp[0] == 'turn':
                start = 1
            else:
                start = 0
            command = temp[start]
            x1, y1 = map(int, temp[start + 1].split(','))
            x2, y2 = map(int, temp[-1].split(','))
            self.grid[x1:x2 +1, y1:y2 + 1] = self.options[command](self.grid[x1:x2 +1, y1:y2 + 1])

        def sum_grid(self):
            return np.sum(self.grid)

class Lights(object):
    
    def __init__(self, x=1000, y=1000, options=None):
        self.grid = [[0 for _ in xrange(x)] for __ in xrange(y)]
        self.x = x
        self.y = y
        if not options:
            self.options = {'on' : lambda x: 1,
                            'off' : lambda x: 0,
                            'toggle' : lambda x: 1 - x}
        else:
            self.options = options

    def __call__(self, line):
        temp = line.split()
        if temp[0] == 'turn':
            start = 1
        else:
            start = 0
        command = temp[start]
        x1, y1 = map(int, temp[start + 1].split(','))
        x2, y2 = map(int, temp[-1].split(','))
        for y_index, row in enumerate(self.grid[y1:y2 + 1]):
            self.grid[y1 + y_index][x1:x2 + 1] = map(self.options[command], row[x1:x2 + 1])

    def sum_grid(self):
        count = 0
        for row in self.grid:
            for light in row:
                count += light
        return count

    def print_grid(self):
        for row in self.grid:
            print ''.join(str(x) for x in row)


def get_results(instructions):
    grid = Lightsnp()
    grid2 = Lightsnp(options={'on' : lambda x: x + 1, 
                            'off' : lambda x: np.maximum(x - 1, 0),
                            'toggle' : lambda x: x + 2})
    for line in instructions.split('\n'):
        grid(line)
        grid2(line)
    print grid.sum_grid()
    return grid2.sum_grid()


if __name__ == '__main__':
    with open('instructions_day6.txt', 'r') as f:
        instructions = f.read().strip()
    print get_results(instructions)