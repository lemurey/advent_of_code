def get_floor(instructions):
    floor = 0
    print_char = True
    for i, char in enumerate(instructions, 1):
        if char == '(':
            floor += 1
        elif char == ')':
            floor -= 1
        if floor == -1:
            if print_char:
                print i
                print_char = False
    return floor


if __name__ == '__main__':
    with open('instructions_day1.txt', 'r') as f:
        instructions = f.read().strip()
    print get_floor(instructions)
