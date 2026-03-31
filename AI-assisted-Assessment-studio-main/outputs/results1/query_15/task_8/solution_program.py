def encode_message(message):
    result = ""
    for char in message:
        if char == 'a':
            result += 'e'
        elif char == 'e':
            result += 'i'
        elif char == 'i':
            result += 'o'
        elif char == 'o':
            result += 'u'
        elif char == 'u':
            result += 'a'
        else:
            result += char
    return result