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

    decrypted_message = ''
    for i in range(0, len(message), 3):
        chunk = message[i:i+3]
        if chunk in galactic_protocols:
            decrypted_message += galactic_protocols[chunk]
        else:
            decrypted_message += ''.join(galactic_cipher.get(char, char) for char in chunk)

    return decrypted_message