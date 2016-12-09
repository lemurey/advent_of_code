with open('instructions_day8.txt', 'r') as f:
    instructions = f.read().strip()

class Display(object):
    def __init__(self, width=50, height=6):
        self.width = width
        self.height = height
        self._reset()

    def __call__(self, command):
        temp = command.split() 
        function = temp[0]
        if function == 'rect':
            A, B = temp[1].split('x')
            self._rect(int(A), int(B))
        elif function == 'rotate':
            option = temp[1]
            A = int(temp[2].split('=')[-1])
            B = int(temp[-1])
            if option == 'row':
                self._rotate_row(A, B)
            else:
                self._rotate_column(A, B)

    def _rect(self, A, B):
        for i in range(B):
            for j in range(A):
                self.grid[i][j] = 1

    def _rotate_row(self, A, B):
        prev = self.grid[A]
        new = prev[:]
        for i, val in enumerate(prev):
            new[(i + B) % self.width] = val
        self.grid[A] = new

    def _rotate_column(self, A, B):
        prev = self._get_column(A)
        new = prev[:]
        for i, val in enumerate(prev):
            new[(i + B) % self.height] = val
        self._set_column(new, A)

    def _get_column(self, index):
        column = []
        for row in self.grid:
            column.append(row[index])
        return column

    def _set_column(self, column, index):
        for i, row in enumerate(self.grid):
            row[index] = column[i]

    def _reset(self):
        self.grid = [[0 for _ in range(self.width)] for _1 in range(self.height)]

    def __str__(self):
        output = ''
        for row in self.grid:
            output += ''.join(' ' if x == 0 else '#' for x in row)
            output += '\n'
        return output.strip()

    def sum_grid(self):
        total = 0
        for row in self.grid:
            for val in row:
                total += val
        return total


def get_result(instructions):
    d = Display()
    for instruction in instructions:
        d(instruction)
    print d.sum_grid()
    print d

if __name__ == '__main__':
    get_result(instructions.split('\n'))
