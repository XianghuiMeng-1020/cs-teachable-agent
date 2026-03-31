def decode_message(galactic_message, codebook):
    words = galactic_message.split()
    decoded_words = []
    for word in words:
        if word in codebook:
            decoded_words.append(codebook[word])
        else:
            decoded_words.append('UNKNOWN')
    return ' '.join(decoded_words)