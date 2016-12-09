def get_results(instructions, year2=False):
    all_instructions = ''.join(instructions.split())
    return follow_path(all_instructions, year2)


def follow_path(path, year2=False):
    santa_position = [0, 0]
    robo_position = [0, 0]
    mods = {'<' : (0, -1), '>' : (0, 1), 'v' : (1, -1), '^' : (1, 1)}
    santa_history = set()
    robo_history = set()
    santa_history.add(tuple(santa_position))
    robo_history.add(tuple(robo_position))
    santa_moves = 0
    robo_moves = 0
    for i, char in enumerate(path):
        index, modifier = mods[char]
        if i % 2 == 0 and year2:
            robo_position[index] += modifier
            robo_history.add(tuple(robo_position))
            robo_moves += 1
        else:
            santa_position[index] += modifier
            santa_history.add(tuple(santa_position))
            santa_moves += 1
    visits = len(santa_history.union(robo_history))
    return visits


if __name__ == '__main__':
    with open('instructions_day3.txt', 'r') as f:
        instructions = f.read().strip()
    print get_results(instructions)
    print get_results(instructions, True)
