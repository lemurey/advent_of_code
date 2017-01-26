from utilities import get_data, timeit, add_points

TURN_RESULTS = {'N': {'L': 'W', 'R': 'E'},
                'E': {'L': 'N', 'R': 'S'},
                'S': {'L': 'E', 'R': 'W'},
                'W': {'L': 'S', 'R': 'N'}}

MOVEMENTS = {'N': (1, 0),
             'E': (0, 1),
             'S': (-1, 0),
             'W': (0, -1)}


def parse_instructions(data):
    return map(lambda x: (x[0], int(x[1:])), data.split(', '))


def update_direction(direction, turn):
    return TURN_RESULTS[direction][turn]


def update_position(position, direction):
    addition = MOVEMENTS[direction]
    return add_points(position, addition)


@timeit
def get_results(data, part2=False):
    directions = parse_instructions(data)
    cur_direction = 'N'
    cur_position = (0, 0)
    past_positions = set()
    past_positions.add(cur_position)
    for turn, distance in directions:
        cur_direction = update_direction(cur_direction, turn)
        for _ in xrange(distance):
            cur_position = update_position(cur_position, cur_direction)
            if cur_position in past_positions and part2:
                return sum(map(abs, cur_position))
            past_positions.add(cur_position)

    return sum(map(abs, cur_position))


if __name__ == '__main__':
    data = get_data(1)
    print get_results(data, part2=False)
    print get_results(data, part2=True)
