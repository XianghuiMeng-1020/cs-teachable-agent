class InterstellarMessage:
    def __init__(self, message, offset):
        self.message = message
        self.offset = offset

    def encode(self):
        encoded_message = ''
        for char in self.message:
            new_char = chr(ord(char) + self.offset)
            if ord(new_char) < 32 or ord(new_char) > 126:
                raise ValueError('Encoded character out of printable range')
            encoded_message += new_char
        return encoded_message

    def decode(self, encoded_message):
        decoded_message = ''
        for char in encoded_message:
            new_char = chr(ord(char) - self.offset)
            if ord(new_char) < 32 or ord(new_char) > 126:
                raise ValueError('Decoded character out of printable range')
            decoded_message += new_char
        return decoded_message
