class InterstellarMessage:
    def __init__(self, message, offset):
        if not all(32 <= ord(c) <= 126 for c in message):
            raise ValueError("Message contains non-printable ASCII characters.")
        self.message = message
        self.offset = offset

    def encode(self):
        encoded_message = ''.join(chr(ord(c) + self.offset) for c in self.message)
        return encoded_message

    def decode(self, encoded_message):
        if not all(32 <= ord(c) <= 126 for c in encoded_message):
            raise ValueError("Encoded message contains non-printable ASCII characters.")
        decoded_message = ''.join(chr(ord(c) - self.offset) for c in encoded_message)
        return decoded_message