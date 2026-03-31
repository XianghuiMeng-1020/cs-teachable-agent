class InterstellarMessage:
    def __init__(self, message, offset):
        self.message = message
        self.offset = offset
        if any(ord(c) < 32 or ord(c) > 126 for c in message):
            raise ValueError("Message contains non-printable characters.")

    def encode(self):
        encoded_message = ''.join(chr(ord(c) + self.offset) for c in self.message)
        return encoded_message

    def decode(self, encoded_message):
        if any(ord(c) < 32 or ord(c) > 126 for c in encoded_message):
            raise ValueError("Encoded message contains non-printable characters.")
        decoded_message = ''.join(chr(ord(c) - self.offset) for c in encoded_message)
        return decoded_message