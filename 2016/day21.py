from utilities import timeit




def parse_instructions(instructions, moves):
    output = []
    for line in instructions.split('\n'):
        words = line.split()
        action = moves[' '.join(words[:2])]
        c = len(words)
        f = int(words[2]) if words[2].isdigit() else words[2]
        if c == 4:
            output.append((action, f, None))
        else:
            s = int(words[-1]) if words[-1].isdigit() else words[-1]
        if c == 5 or c == 6:
            output.append((action, f, s))
        elif c == 7:
            output.append((action, s, None))
    return output
        

def swap_position(s, p1, p2, undo):
    if p1 > p2:
        p1, p2 = p2, p1
    return '{}{}{}{}{}'.format(s[:p1], s[p2], s[p1 + 1:p2], s[p1], s[p2 + 1:])


def swap_letters(s, a, b, undo):
    return s.replace(a, '*#*').replace(b, a).replace('*#*', b)


def rotate_left(s, d, undo):   
    if undo:
        return rotate_right(s, d, False)     
    d = d % len(s)
    return s[d:] + s[:d]


def rotate_right(s, d, undo):
    if undo:
        return rotate_left(s, d, False)
    d = -1 * d % len(s)
    return s[d:] + s[:d]


def rotate_by_x(s, X, undo):
    index = s.find(X)
    if undo:
        replace = {0 : 1, 1 : 9, 2 : 6, 3 : 2, 4 : 7, 5 : 3, 6 : 8, 7 : 4}
        return rotate_left(s, replace[index], False)

    if index >= 4:
        index += 1
    index += 1
    return rotate_right(s, index, undo)


def reverse(s, X, Y, undo):
    begin = s[:X]
    swapped = s[X:Y + 1]
    end = s[Y + 1:]
    return begin + swapped[::-1] + end


def move(s, p1, p2, undo):
    if undo:
        p1, p2 = p2, p1
    a = s[p1]
    temp = s[:p1] + s[p1 + 1:]
    return temp[:p2] + a + temp[p2:]


@timeit
def get_results(instructions, part2=False):
    string = 'abcdefgh'
    moves = {'swap position'     : swap_position,
             'swap letter'       : swap_letters,
             'rotate left'       : rotate_left,
             'rotate right'      : rotate_right,
             'rotate based'      : rotate_by_x,
             'reverse positions' : reverse,
             'move position'     : move}
    operations = parse_instructions(instructions, moves)
    encoder = Encoder(instructions)
    encoder(string)
    print encoder
    if part2:
        operations = operations[::-1]
        string = 'fbgdceah'
    for action, option1, option2 in operations:
        if option2 is not None:
            string = action(string, option1, option2, part2)
        else:
            string = action(string, option1, part2)
    return string



if __name__ == '__main__':
    with open('instructions_day21.txt', 'r') as f:
        instructions = f.read().strip()
    print get_results(instructions, part2=False)
    print get_results(instructions, part2=True)
