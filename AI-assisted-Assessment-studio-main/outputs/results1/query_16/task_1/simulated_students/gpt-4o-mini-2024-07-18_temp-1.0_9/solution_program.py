class CommsHandler:
    def __init__(self, factor=1):
        self.factor = factor

    def send_message(self, message):
        try:
            ascii_sum = sum(ord(char) for char in message)
            transmit_code = ascii_sum * self.factor
            return f"{message}#{transmit_code}"
        except Exception as e:
            raise RuntimeError(f"Error sending message: {e}")

    def receive_message(self, message_with_code):
        try:
            message, code_str = message_with_code.rsplit('#', 1)
            ascii_sum = sum(ord(char) for char in message)
            expected_code = ascii_sum * self.factor
            if int(code_str) != expected_code:
                raise ValueError("Transmit code mismatch")
            return message
        except ValueError:
            raise
        except Exception as e:
            raise RuntimeError(f"Error receiving message: {e}")