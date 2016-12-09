with open('instructions_day2.txt', 'r') as f:
    instructions = f.read().strip()

keypad = '123\n456\n789'


def get_dirs(char, index, line, prev_line, next_line):
    U = get_result(char, index, prev_line, len(prev_line), 0)
    D = get_result(char, index, next_line, len(next_line), 0)
    L = get_result(char, index, line + ' ', len(line) + 1, -1)
    R = get_result(char, index, line, len(line) - 1, 1)
    return U, D, L, R


def get_result(char, index, line, condition, mod):
    if index < condition:
        if line[index + mod] != ' ':
            return line[index + mod]
    return char


def get_move_dict(keypad):
    move_dict = {}
    prev_line = ''
    lines = keypad.split('\n')
    max_lines = len(lines)
    U, D, L, R = None, None, None, None
    for line_num, line in enumerate(lines):
        if line_num < max_lines - 1:
            next_line = lines[line_num + 1]
        else:
            next_line = ''
        for i, char in enumerate(line):
            if char == ' ':
                continue
            U, D, L, R = get_dirs(char, i, line, prev_line, next_line)
            for name, direction in [('U', U), ('D', D), ('L', L), ('R', R)]:
                if direction:
                    if char in move_dict:
                        move_dict[char][name] = direction
                    else:
                        move_dict[char] = {name: direction}
        prev_line = line
    return move_dict


move_dict = get_move_dict(keypad)


def get_code(instructions, location, move_dict=move_dict):
    code = ''
    for line in instructions.split():
        for instruction in line:
            location = move_dict[location][instruction]
        code += location
    return code


if __name__ == '__main__':
    print get_code(instructions, '5', move_dict)
    keypad = '  1\n 234\n56789\n ABC\n  D'
    move_dict = get_move_dict(keypad)
    print get_code(instructions, '7', move_dict)
