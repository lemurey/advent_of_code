with open('instructions_day1.txt', 'r') as f:
    instructions = f.read().strip()


def get_turn(cur_direction, turn):
    results = {'N' : {'R' : 'E', 'L' : 'W'},
               'W' : {'R' : 'N', 'L' : 'S'},
               'E' : {'R' : 'S', 'L' : 'N'},
               'S' : {'R' : 'W', 'L' : 'E'}}
    return results[cur_direction][turn]


def move(point, direction, distance):
    map_vals = {'N' : (1, 1), 'E' : (0, 1), 'S' : (1, -1), 'W' : (0, -1)}
    index, multiplier = map_vals[direction]
    x, y = point
    if index == 0:
        x += multiplier * distance
    else:
        y += multiplier * distance
    return x, y


def follow_inst(location, direction, instruction):
    turn = instruction[0]
    distance = instruction[1]
    direction = get_turn(direction, turn)
    return move(location, direction, distance), direction


def get_instruction_list(instructions):
    return [(x.strip()[0], int(x.strip()[1:])) for x in instructions.split(',')]


def parse_instructions(instructions):
    instructions_list = get_instruction_list(instructions)
    location = (0, 0)
    direction = 'N'
    for instruction in instructions_list:
        location, direction = follow_inst(location, direction, instruction)
    return abs(location[0]) + abs(location[1])


def get_range(d1, d2):
    if d1 > d2:
        return xrange(d2, d1 + 1)
    else:
        return xrange(d1, d2 + 1)


def generate_path(location1, location2):
    x_range = get_range(location1[0], location2[0])
    y_range = get_range(location1[1], location2[1])
    path = []
    for x in x_range:
        for y in y_range:
            if (x, y) == location2:
                continue
            path.append((x, y))
    return path


def parse_instructions_2(instructions):
    instructions_list = get_instruction_list(instructions)
    location = (0, 0)
    direction = 'N'
    past_visits = {(0, 0) : 1}
    for instruction in instructions_list:
        prev_location = location
        location, direction = follow_inst(location, direction, instruction)
        path = generate_path(location, prev_location)
        for point in path:
            if point in past_visits:
                return abs(point[0]) + abs(point[1])
            else:
                past_visits[point] = 1
    

if __name__ == '__main__':
    print parse_instructions(instructions)
    print parse_instructions_2(instructions)