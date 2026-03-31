def decode_alien_message(message):
    result = []
    for char in message:
        result.append(ord(char) - ord('a') + 1)
    return result
