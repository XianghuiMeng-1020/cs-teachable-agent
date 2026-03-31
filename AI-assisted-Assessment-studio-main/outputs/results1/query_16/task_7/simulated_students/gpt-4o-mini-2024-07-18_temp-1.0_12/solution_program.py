class InterstellarMessage:
    def __init__(self, message, offset):
        self.message = message
        self.offset = offset
        if not self._is_printable(message):
            raise ValueError("Message contains non-printable characters.")

    def _is_printable(self, message):
        return all(32 <= ord(char) <= 126 for char in message)

    def encode(self):
        encoded_chars = [chr(ord(char) + self.offset) for char in self.message]
        return ''.join(encoded_chars)

    def decode(self, encoded_message):
        if not self._is_printable(encoded_message):
            raise ValueError("Encoded message contains non-printable characters.")
        decoded_chars = [chr(ord(char) - self.offset) for char in encoded_message]
        return ''.join(decoded_chars)