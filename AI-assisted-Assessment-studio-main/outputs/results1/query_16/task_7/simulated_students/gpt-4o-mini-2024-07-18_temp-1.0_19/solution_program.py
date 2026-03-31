class InterstellarMessage:
    def __init__(self, message, offset):
        self.message = message
        self.offset = offset
        if not all(32 <= ord(char) <= 126 for char in message):
            raise ValueError("Message contains non-printable ASCII characters.")

    def encode(self):
        encoded_message = ''.join(chr(ord(char) + self.offset) for char in self.message)
        return encoded_message

    def decode(self, encoded_message):
        if not all(32 <= ord(char) <= 126 for char in encoded_message):
            raise ValueError("Encoded message contains non-printable ASCII characters.")
        decoded_message = ''.join(chr(ord(char) - self.offset) for char in encoded_message)
        return decoded_message