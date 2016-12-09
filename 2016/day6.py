with open('instructions_day6.txt', 'r') as f:
    instructions = f.read().strip()


def decode_message(data, mod=-1):
    message_length = len(data[0])
    message_counts = tuple(({} for _ in range(message_length)))
    for line in data:
        for i, char in enumerate(line):
            if char in message_counts[i]:
                message_counts[i][char] += 1
            else:
                message_counts[i][char] = 1
    result = ''
    for counts in message_counts:
        char = sorted(counts.iteritems(), key=lambda x: mod * x[1])[0][0]
        result += char
    return result


if __name__ == '__main__':
    print decode_message(instructions.split('\n'))
    print decode_message(instructions.split('\n'), 1)