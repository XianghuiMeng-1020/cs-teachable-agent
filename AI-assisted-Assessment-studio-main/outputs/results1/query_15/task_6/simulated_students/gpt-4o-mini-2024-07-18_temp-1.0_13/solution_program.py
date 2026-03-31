def decode_alien_message(message):
    return [ord(char) - ord('a') + 1 for char in message]