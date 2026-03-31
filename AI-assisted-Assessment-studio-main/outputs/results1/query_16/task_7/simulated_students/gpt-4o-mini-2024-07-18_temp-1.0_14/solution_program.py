class InterstellarMessage:
    def __init__(self, message, offset):
        self.message = message
        self.offset = offset
        self.validate_message()

    def validate_message(self):
        for char in self.message:
            if not (32 <= ord(char) <= 126):
                raise ValueError("Message contains non-printable ASCII characters")

    def encode(self):
        encoded_message = ''.join(chr(ord(char) + self.offset) for char in self.message)
        return encoded_message

    def decode(self, encoded_message):
        for char in encoded_message:
            if not (32 <= ord(char) <= 126):
                raise ValueError("Encoded message contains non-printable ASCII characters")
        decoded_message = ''.join(chr(ord(char) - self.offset) for char in encoded_message)
        return decoded_message