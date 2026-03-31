def decode_message(galactic_message, codebook):
    words = galactic_message.split()
    decoded_words = [codebook.get(word, 'UNKNOWN') for word in words]
    return ' '.join(decoded_words)