def decrypt_message(message):
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

    decrypted_message = ""
    # Process the message in chunks of 3
    for i in range(0, len(message), 3):
        substring = message[i:i+3]
        # Check if the substring exists in galactic_protocols
        if substring in galactic_protocols:
            decrypted_message += galactic_protocols[substring]
        else:
            # If not, decrypt each character using galactic_cipher
            for char in substring:
                decrypted_message += galactic_cipher.get(char, char)

    return decrypted_message