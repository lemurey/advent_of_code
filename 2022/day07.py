from aoc_utilities import get_instructions
from pathlib import Path


class Dir:
    def __init__(self, name, parent):
        self.name = name
        if parent is None:
            self.root = True
            self.parent = self
        else:
            self.root = False
            self.parent = parent
        self.children = []
        self.files = {}
        self.size = None

    def add_child(self, child):
        self.children.append(child)

    def add(self, contents):
        for val in contents:
            prefix, name = val.split(' ')
            if prefix.isdigit():
                self.files[name] = int(prefix)

    def get_size(self):
        if self.size is None:
            self._calculate_size()
        return self.size

    def _calculate_size(self):
        self.size = sum(self.files.values())
        for child in self.children:
            self.size += child.get_size()

    def __iter__(self):
        yield self
        for child in self.children:
            yield from child


class FS:
    def __init__(self, data):
        self.data = data
        self.loc = None
        self.index = 0
        self.root = Dir('/', None)
        self.node = self.root

    def __call__(self):
        cmd = self._get()
        if cmd == -1:
            return -1
        if cmd == '$ ls':
            contents = self.get_contents()
            self.node.add(contents)
        else:
            loc = cmd.split(' ')[-1]
            if loc == '/':
                self.node = self.root
            elif loc == '..':
                self.node = self.node.parent
            else:
                new = Dir(loc, self.node)
                self.node.add_child(new)
                self.node = new
        return 1

    def _get(self):
        if self.index < len(self.data):
            cmd = self.data[self.index]
            self.index += 1
            return cmd
        return -1

    def get_contents(self):
        val = self._get()
        contents = []
        while not val.startswith('$'):
            contents.append(val)
            val = self._get()
            if val == -1:
                return tuple(contents)
        self.index -= 1
        return tuple(contents)

    def __iter__(self):
        yield from self.root


def parse_instructions(data):
    cmds = set()
    for line in data:
        if line.startswith('$'):
            val = line.split(' ')[1]
            cmds.add(val)
    return cmds


def get_answer(data, part2=False):
    fs = FS(data)
    val = 1
    while val != -1:
        val = fs()
    total = 0
    remaining_size = 70000000 - fs.root.get_size()
    needed_size = 30000000 - remaining_size
    candidates = []
    for d in fs:
        if d.get_size() < 100000:
            total += d.get_size()
        if d.get_size() >= needed_size:
            candidates.append(d.get_size())
    print(total)
    return min(candidates)



if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs = '''$ cd /
# $ ls
# dir a
# 14848514 b.txt
# 8504156 c.dat
# dir d
# $ cd a
# $ ls
# dir e
# 29116 f
# 2557 g
# 62596 h.lst
# $ cd e
# $ ls
# 584 i
# $ cd ..
# $ cd ..
# $ cd d
# $ ls
# 4060174 j
# 8033020 d.log
# 5626152 d.ext
# 7214296 k'''.split('\n')
    print(get_answer(inputs, part2=False))
    # print(get_answer(inputs, part2=True))
