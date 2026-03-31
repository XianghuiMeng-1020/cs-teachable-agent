class CommsHandler:
    def __init__(self, transmit_code_factor):
        self.transmit_code_factor = transmit_code_factor

    def send_message(self, message):
        # Calculate the sum of ASCII values of the characters in the message
        ascii_sum = sum(ord(char) for char in message)
        # Calculate the transmit code by multiplying with the transmit code factor
        transmit_code = ascii_sum * self.transmit_code_factor
        # Return the message with the transmit code appended
        return f"{message}#{transmit_code}"

    def receive_message(self, message_with_code):
        try:
            # Separate message and code
            message, code = message_with_code.rsplit('#', 1)
            # Calculate expected transmit code
            ascii_sum = sum(ord(char) for char in message)
            expected_code = ascii_sum * self.transmit_code_factor

            if int(code) == expected_code:
                return message
            else:
                raise ValueError("Transmit code mismatch")
        except (ValueError, IndexError):
            raise ValueError("Transmit code mismatch")