class InterstellarMessage:
    def __init__(self, message, offset):
        # Check for non-printable characters in the initial message
        for char in message:
            if ord(char) < 32 or ord(char) > 126:
                raise ValueError("Message contains non-printable ASCII characters")
        self.message = message
        self.offset = offset

    def encode(self):
        encoded_message = ""
        for char in self.message:
            new_char = chr(ord(char) + self.offset)
            if ord(new_char) < 32 or ord(new_char) > 126:
                raise ValueError("Encoded message contains non-printable ASCII characters")
            encoded_message += new_char
        return encoded_message

    def decode(self, encoded_message):
        decoded_message = ""
        for char in encoded_message:
            new_char = chr(ord(char) - self.offset)
            if ord(new_char) < 32 or ord(new_char) > 126:
                raise ValueError("Decoded message contains non-printable ASCII characters")
            decoded_message += new_char
        return decoded_message
