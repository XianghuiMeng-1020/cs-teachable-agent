class InterstellarMessage:
    def __init__(self, message, offset):
        self.message = message
        self.offset = offset
        self.validate_message(message)

    def encode(self):
        encoded_message = ''
        for char in self.message:
            encoded_char = chr(ord(char) + self.offset)
            encoded_message += encoded_char
        return encoded_message

    def decode(self, encoded_message):
        self.validate_message(encoded_message)
        decoded_message = ''
        for char in encoded_message:
            decoded_char = chr(ord(char) - self.offset)
            decoded_message += decoded_char
        return decoded_message

    def validate_message(self, msg):
        for char in msg:
            if not (32 <= ord(char) <= 126):
                raise ValueError('Message contains non-printable ASCII characters.')