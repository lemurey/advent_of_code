from collections import deque

def make_first_node(instructions, second_pass=False):
    '''
    parse the instructions and make the first node tuple
    node tuples have the form:
        (elevator index, contents of floor1, contents of floor2, ...)
    where the contents of each floor are a tuple, 
    this allows the nodes to be keys in dictionaries
    INPUT: string, boolean
    OUTPUT (int, tuple, tuple, tuple, tuple)
    '''
    lines = instructions.split('\n')
    info = [[], [], [], []]
    for index, line in enumerate(lines):
        temp = line.split()[::-1]
        prescript = None
        element = None
        for index_2, word in enumerate(temp[:-2]):
            if 'microchip' in word.lower():
                prescript = 'M'
            elif 'generator' in word.lower():
                prescript = 'G'
            if prescript:
                element = temp[index_2 + 1][:2].capitalize()
                info[index].append(prescript + element)
                prescript = None
        index -= 1

    if second_pass:
        info[0].extend(['MEl', 'GEl', 'MDi', 'GDi'])

    f1 = tuple(info[0])
    f2 = tuple(info[1])
    f3 = tuple(info[2])
    f4 = tuple(info[3])

    return (1, f1, f2, f3, f4)


class Solver(object):
    '''
    do breadth first search for the graph of floor nodes
    dynamically generate and score neighbor nodes as search progresses
    prunes out nodes with low scores, are invalid, or which are equivalent to 
    an already visited node.
    '''
    def __init__(self, first_node, verbose=True, iter_check=500):
        self.path = {first_node: []}
        self.end_condition = self._get_end_condition(first_node)
        self.verbose = verbose
        self.iter_check = iter_check
        self.Q = deque([first_node])
        self.out_string = 'iteration number: {}, length of Q: {}'
        self.history = set()
        self.iters = 0
        self.cur_key = None

    def search(self):
        '''
        perform the search for shortest path. End condition is when all items
        are on the fourth floor
        '''
        while self.Q:
            node = self.Q.popleft()
            if len(node[4]) == self.end_condition:
                print 'search took {} iterations'.format(self.iters)
                return self.path[node]
            for neighbor in self._get_neighbors(node):
                if not self._check_node(neighbor):
                    continue
                self._update(node, neighbor)
                self.iters += 1
                if self.verbose and self.iters % self.iter_check == 0:
                    print self.out_string.format(self.iters, len(self.Q))

        print 'FAILED TO FIND SHORTEST PATH'
        return self.path

    def _check_node(self, node):
        '''
        checks if a node is valid and not equivalent to a node already in the
        search history
        '''
        if node in self.path:
            return False
        self.cur_key = self._make_node_key(node)
        if self.cur_key in self.history:
            return False
        return True

    def _update(self, node, neighbor):
        '''
        updates the path, history and queue for the search
        '''
        self.path[neighbor] = self.path[node] + [neighbor]
        self.history.add(self.cur_key)
        self.Q.append(neighbor)

    def _make_node_key(self, node):
        '''
        creates a tuple of elevator location, generators per floor, and chips
        pre floor. This identifies equivalent nodes for exclusion from search
        space
        '''
        g_sum = [0, 0, 0, 0]
        c_sum = [0, 0, 0, 0]
        for i, floor in enumerate(node[1:]):
            g_sum[i] = sum(1 for item in floor if item[0] == 'G')
            c_sum[i] = sum(1 for item in floor if item[0] == 'M')
        return (node[0], tuple(g_sum), tuple(c_sum))

    def _get_neighbors(self, node):
        '''
        generator for getting neighbors of a node
        '''
        elevator = node[0]
        items = node[elevator]
        lower_floors = sum(len(floor) for floor in node[1:elevator])
        for index, item in enumerate(items[:-1]):
            pair = (item, items[index + 1])
            if elevator < 4: #if elevator is not at top floor try going up
                node2 = self._make_node(node, pair, elevator + 1)
                node1 = self._make_node(node, [item], elevator + 1)
                if self._check_valid(node2) and self._score(node2, node1) >= 0:
                    yield node2
                elif self._check_valid(node1):
                    yield node1
            if elevator > 1 and lower_floors > 0:
                node2 = self._make_node(node, pair, elevator - 1)
                node1 = self._make_node(node, [item], elevator - 1)
                if self._check_valid(node2) and self._score(node2, node1) >= 0:
                    yield node2
                elif self._check_valid(node1):
                    yield node1

    def _make_node(self, node, items, floor):
        '''
        make a tuple of tuples from a previous node
        INPUT:
            node: tuple 
                node to alter to get new node
            items: list 
                items to move to a new floor
            floor: int
                new floor to put items on
        OUTPUT:
            node
            (int, tuple, tuple, tuple, tuple)
        '''
        new_node = [floor]
        for index in xrange(1, 5):
            if index != floor:
                new_node.append(tuple(set(node[index]) - set(items)))
            else:
                new_node.append(tuple(set(node[index]) | set(items)))
        return tuple(new_node)

    def _check_valid(self, node):
        '''
        checks if a node is valid, invalid nodes are ones with mismatched
        chips and generators on the same floor
        '''
        for floor in node[1:]:
            generators = {item[1:] for item in floor if item[0] == 'G'}
            chips = {item[1:] for item in floor if item[0] == 'M'}

            if len(generators - chips) > 0 and len(chips - generators) > 0:
                return False

        return True

    def _score(self, node1, node2):
        '''
        score the nodes, score is weighted sum of items on a floor, the weight 
        is the floor number. return difference in score
        INPUT:
            node1: node
            node2: node
        OUTPUT:
            int: score(node1) - score(node2)
        '''
        score1 = sum([len(f) * m for m, f in enumerate(node1[1:], 1)])
        score2 = sum([len(f) * m for m, f in enumerate(node2[1:], 1)])
        return score1 - score2

    def _get_end_condition(self, node):
        '''
        get number of items total in a node
        '''
        return sum(len(x) for x in node[1:])


def get_results(instructions):
    first_node = make_first_node(instructions)
    second_node = make_first_node(instructions, True)

    s1 = Solver(first_node, verbose=False)
    print 'shortest path is {} steps'.format(len(s1.search()))
    s2 = Solver(second_node, verbose=False)
    print 'shortest path is {} steps'.format(len(s2.search()))

if __name__ == '__main__':
    with open('instructions_day11.txt', 'r') as f:
        instructions = f.read().strip()
    get_results(instructions)
