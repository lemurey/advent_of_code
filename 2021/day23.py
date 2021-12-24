from aoc_utilities import get_instructions
from pathlib import Path

import heapq


COSTS = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
HALL_BASE = '.' * 11
ROOMS_LOC = {2: 'A', 4: 'B', 6: 'C', 8: 'D'}
DESIRED_ROOM = {'A': 2, 'B': 4, 'C': 6, 'D': 8}
FORBIDDEN = [k for k in ROOMS_LOC]


class State:
    def __init__(self, hall, rooms):
        self.hall = tuple([x if x != '.' else None for x in hall])
        self.rooms = []
        for room in rooms:
            self.rooms.append(tuple([x if x != '.' else None for x in room]))
        self.rooms = tuple(self.rooms)
        hall_str = str(self).split(',')[0]
        # assert(all([hall_str.count(x) <= 2 for x in COSTS]))

    def __str__(self):
        hall = ''.join(['.' if not x else x for x in self.hall])
        rooms = ''.join([''.join(['.' if not x else x for x in r]) for r in self.rooms])
        return f'{hall,rooms}'

    def __hash__(self):
        return hash((self.hall, self.rooms))

    def __eq__(self, other):
        return (self.hall, self.rooms) == (other.hall, other.rooms)

    def __repr__(self):
        return (self,hall, self.rooms)

    def __lt__(self, other):
        return str(self) < str(other)

    def can_get_in(self, pod, room_idx):
        room = self.rooms[room_idx]
        if not all([c == None or c == pod for c in room]):
            return None, 10000000

        ### I think this update works
        '''
        need to go over the room backwards, find the first spot
        that is empty (value of None) and return that index
        '''
        idx = len(room) - 1
        for val in room[::-1]:
            if val is None:
                steps = idx + 1
                break
            idx -= 1

        new_rooms = [list(room[:]) for room in self.rooms]
        new_rooms[room_idx][steps - 1] = pod
        return new_rooms, COSTS[pod] * steps

    def final(self):
        if not all([x == None for x in self.hall]):
            return False
        for i, room in enumerate(self.rooms):
            if i in ROOMS_LOC:
                if not all([x == ROOMS_LOC[i] for x in room]):
                    return False
        return True

    def get_moves(self):
        out = []

        for move, cost in self.get_hallway_moves():
            if move is None:
                continue
            out.append((cost, move))
        for move, cost in self.get_moves_out_of_room():
            if move is None:
                continue
            out.append((cost, move))

        return sorted(out)

    def get_hallway_moves(self):
        ## enumerate over all the pods
        for i, pod in enumerate(self.hall):
            ## if no pod, no move
            if pod is None:
                yield None, 10000000

            else:
                room_idx = DESIRED_ROOM[pod]

                if i < room_idx:
                    checks = range(i+1, room_idx)
                else:
                    checks = range(room_idx, i)

                ## enumerate over space between pod and room it wants
                for i2 in checks:
                    other = self.hall[i2]
                    # if another pod is in the way, no move
                    if other is not None:
                        yield None, 10000000
                        break
                else:
                    rooms, enter_cost = self.can_get_in(pod, room_idx)
                    if rooms is not None:
                        cost = (abs(i - room_idx) * COSTS[pod]) + enter_cost
                        hall = self.copy_hall(i, None)
                        yield State(hall, rooms), cost

    def get_moves_out_of_room(self):
        # iterate over all valid wanted_pod/room_idx
        for desired_pod, room_idx in DESIRED_ROOM.items():
            room = self.rooms[room_idx]

            if all([c == None or c == desired_pod for c in room]):
                yield None, 10000000
            else:
                ### I think this works for part2
                '''
                need to find the first non-empty pod in room,
                get that index
                '''
                for idx, val in enumerate(room):
                    if val is not None:
                        steps =  idx + 1
                        break

                new_rooms = [list(room[:]) for room in self.rooms]
                pod = new_rooms[room_idx][steps - 1]
                new_rooms[room_idx][steps - 1] = None

                yield from self.move_to_hallway(new_rooms, pod, steps, room_idx)

    def move_to_hallway(self, rooms, pod, steps, room_idx):
        viable_locs = []
        for pos in range(room_idx, len(self.hall)):
            if self.hall[pos] is not None:
                break
            viable_locs.append(pos)
        for pos in range(room_idx, -1, -1):
            if self.hall[pos] is not None:
                break
            viable_locs.append(pos)

        for loc in viable_locs:
            if loc in FORBIDDEN:
                continue
            hall = self.copy_hall(loc, pod)
            cost = COSTS[pod] * (steps + abs(room_idx - loc))
            yield State(hall, rooms), cost

    def copy_hall(self, loc, pod):
        hall = list(self.hall[:])
        hall[loc] = pod
        hall = tuple(hall)
        return hall

def show_path(path):

    for step in path:
        out = '#' * 13 + '\n'
        # print(step, type(step), len(step))
        hallway, rooms = step.split(', ')
        hallway = hallway.strip('()').strip("'").strip()
        rooms = rooms.strip('()').strip("'").strip()
        out += '#' + hallway + '#\n'
        out += '###' + '#'.join([rooms[i] for i in (0, 2, 4, 6)]) + '###\n'
        out += '  #' + '#'.join([rooms[i] for i in (1, 3, 5, 7)]) + '#  \n'
        print(out)


def solve(hall, rooms):

    start = State(hall, rooms)
    visited = set()
    heap = [(0, start, ())]

    with open('check_day23.txt', 'w') as f:
        while heap:
            cost, state, path = heapq.heappop(heap)

            if state in visited:
                continue

            f.write(f'cost: {cost}, state: {state}\n')
            visited.add(state)

            if state.final():
                f.close()
                show_path(path)
                return cost

            for move_cost, move in state.get_moves():
                heapq.heappush(heap, (cost + move_cost,
                                      move,
                                      tuple(list(path) + [str(state)])))


def process_data(data):
    rooms = [[], [], [], [], [], [], [], [], [], [], [], [], []]
    hall = []
    for j, line in enumerate(data):
        if j == 0:
            continue
        elif j == 1:
            hall = line[1:-1]
        else:
            for i, val in enumerate(line, start=-1):
                if val in 'ABCD':
                    rooms[i].append(val)
    return hall, rooms


def get_room_state(string):
    rooms = [[], [], [], [], [], [], [], [], [], [], [], [], []]
    i = 0
    for room_idx in ROOMS_LOC:
        room = rooms[room_idx]
        room.extend([string[i], string[i+1]])
        i += 2
    return rooms

def get_answer(data, part2=False):
    hall, rooms = process_data(data)
    if part2:
        adds = [['D', 'D'], ['C', 'B'], ['B', 'A'], ['A', 'C']]
        for i, idx in enumerate(ROOMS_LOC):
            rooms[idx] = [rooms[idx][0]] + adds[i] + [rooms[idx][-1]]

    return solve(hall, rooms)


if __name__ == '__main__':
    p = Path(__file__).absolute()
    year = p.parent.stem
    day = int(p.stem.split('y')[1])
    inputs = get_instructions(year, day)
#     inputs='''#############
# #...........#
# ###B#C#B#D###
#   #A#D#C#A#
#   #########'''.split('\n')
    print(get_answer(inputs, part2=False))
    print(get_answer(inputs, part2=True))
