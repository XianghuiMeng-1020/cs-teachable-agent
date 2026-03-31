class InterstellarMessage:
    def __init__(self, message, offset):
        self.message = message
        self.offset = offset
        self._validate_message(message)

    def encode(self):
        encoded_chars = [chr(ord(c) + self.offset) for c in self.message]
        return ''.join(encoded_chars)

    def decode(self, encoded_message):
        self._validate_message(encoded_message)
        decoded_chars = [chr(ord(c) - self.offset) for c in encoded_message]
        return ''.join(decoded_chars)

    def _validate_message(self, message):
        for c in message:
            if not (32 <= ord(c) <= 126):
                raise ValueError('Message contains non-printable ASCII characters.')