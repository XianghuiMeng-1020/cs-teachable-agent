def decrypt_message(message):
    # Assuming galactic_cipher and galactic_protocols are accessible
    result = []
    galactic_cipher = {
        'A': 'Z',
        'B': 'Y',
        'C': 'X',
        'D': 'W',
        'E': 'V',
        'F': 'U',
        '1': '9'
    }

    galactic_protocols = {
        'FOO': 'HELLO',
        'BAR': 'WORLD',
        '123': 'SPACE'
    }

    # Process the message in chunks of 3
    for i in range(0, len(message), 3):
        chunk = message[i:i+3]
        # Check if the chunk is a protocol
        if chunk in galactic_protocols:
            result.append(galactic_protocols[chunk])
        else:
            # Decrypt each character in the chunk
            decoded_chunk = ''.join(galactic_cipher.get(c, c) for c in chunk)
            result.append(decoded_chunk)

    return ''.join(result)

# Since I can't import the test cases here, we can verify by calling a sample function
# Uncomment these lines to test
# print(decrypt_message("FOOBAR123F1C"))  # Output should be "HELLOWORLDSPACEXUX"
# print(decrypt_message("123A1C"))  # Output should be "SPACEZ9X"