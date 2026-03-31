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

    decoded_message = ''
    for i in range(0, len(message), 3):
        chunk = message[i:i+3]
        if chunk in galactic_protocols:
            decoded_message += galactic_protocols[chunk]
        else:
            for char in chunk:
                decoded_message += galactic_cipher.get(char, char)
    return decoded_message
