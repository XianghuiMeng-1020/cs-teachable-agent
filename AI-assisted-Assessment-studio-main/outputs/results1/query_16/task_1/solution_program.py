class CommsHandler:
    def __init__(self, transmit_code_factor):
        self.transmit_code_factor = transmit_code_factor

    def send_message(self, message):
        try:
            code_sum = sum(ord(char) for char in message)
            transmit_code = code_sum * self.transmit_code_factor
            return f"{message}#{transmit_code}"
        except Exception:
            raise ValueError("Failed to send message")

    def receive_message(self, message_with_code):
        try:
            message, str_code = message_with_code.rsplit("#", 1)
            actual_code = sum(ord(char) for char in message) * self.transmit_code_factor
            expected_code = int(str_code)
            if actual_code == expected_code:
                return message
            else:
                raise ValueError("Transmit code mismatch")
        except ValueError:
            raise ValueError("Transmit code mismatch")