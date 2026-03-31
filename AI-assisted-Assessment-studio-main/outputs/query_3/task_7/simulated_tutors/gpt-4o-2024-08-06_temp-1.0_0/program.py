def decode_message(galactic_message, codebook):
    # Splitting the galactic message into individual words (codes)
    message_words = galactic_message.split()
    
    # Decoding each word using the codebook
    decoded_words = []
    for word in message_words:
        # Use .get() to provide 'UNKNOWN' as the default if word is not found
        decoded_word = codebook.get(word, 'UNKNOWN')
        decoded_words.append(decoded_word)
    
    # Concatenating the decoded words into a full message
    decoded_message = ' '.join(decoded_words)
    return decoded_message

# Example usage
codebook = {'QXZ':'hello', 'BFO':'world', 'DZT':'alien'}
galactic_message = 'QXZ BFO GAO'
print(decode_message(galactic_message, codebook))  # Output: 'hello world UNKNOWN'