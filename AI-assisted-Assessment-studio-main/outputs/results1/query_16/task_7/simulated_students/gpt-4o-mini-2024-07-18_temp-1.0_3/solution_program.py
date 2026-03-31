class InterstellarMessage:
    def __init__(self, message, offset):
        self.message = message
        self.offset = offset
        self.validate_message(message)

    def validate_message(self, message):
        for char in message:
            if not (32 <= ord(char) <= 126):
                raise ValueError("Message contains non-printable ASCII characters.")

    def encode(self):
        encoded_message = ''.join(chr(ord(char) + self.offset) for char in self.message)
        return encoded_message

    def decode(self, encoded_message):
        self.validate_message(encoded_message)
        decoded_message = ''.join(chr(ord(char) - self.offset) for char in encoded_message)
        return decoded_message