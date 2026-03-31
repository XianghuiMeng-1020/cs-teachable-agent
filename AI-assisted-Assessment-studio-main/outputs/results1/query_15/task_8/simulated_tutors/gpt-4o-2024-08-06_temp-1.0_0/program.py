def encode_message(message):
    vowel_shift = {'a': 'e', 'e': 'i', 'i': 'o', 'o': 'u', 'u': 'a'}
    encoded_message = []
    
    for char in message:
        if char in vowel_shift:
            encoded_message.append(vowel_shift[char])
        else:
            encoded_message.append(char)
    
    return ''.join(encoded_message)

# Example test
print(encode_message("hello world"))  # Output should be "hillu wurld"