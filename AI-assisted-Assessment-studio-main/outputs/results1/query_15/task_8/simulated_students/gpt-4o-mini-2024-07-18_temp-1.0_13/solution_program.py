def encode_message(message):
    vowel_shift = {'a': 'e', 'e': 'i', 'i': 'o', 'o': 'u', 'u': 'a'}
    encoded_message = ''

    for char in message:
        if char in vowel_shift:
            encoded_message += vowel_shift[char]
        else:
            encoded_message += char

    return encoded_message