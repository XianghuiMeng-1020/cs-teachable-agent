class InterstellarMessage:
    def __init__(self, message, offset):
        self.message = message
        self.offset = offset
        self._validate_message(message)

    def encode(self):
        encoded_chars = [chr(ord(char) + self.offset) for char in self.message]
        return ''.join(encoded_chars)

    def decode(self, encoded_message):
        self._validate_message(encoded_message)
        decoded_chars = [chr(ord(char) - self.offset) for char in encoded_message]
        return ''.join(decoded_chars)

    def _validate_message(self, message):
        for char in message:
            if not (32 <= ord(char) <= 126):
                raise ValueError('Message contains non-printable ASCII characters.')