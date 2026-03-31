class CommsHandler:
    def __init__(self, factor):
        self.transmit_code_factor = factor

    def send_message(self, message):
        try:
            ascii_sum = sum(ord(char) for char in message)
            transmit_code = ascii_sum * self.transmit_code_factor
            return f"{message}#{transmit_code}"
        except Exception as e:
            raise ValueError(f"Error in sending message: {e}")

    def receive_message(self, message_with_code):
        try:
            message, received_code = message_with_code.rsplit('#', 1)
            ascii_sum = sum(ord(char) for char in message)
            expected_code = ascii_sum * self.transmit_code_factor
            if str(expected_code) != received_code:
                raise ValueError("Transmit code mismatch")
            return message
        except ValueError as ve:
            raise ve
        except Exception as e:
            raise ValueError(f"Error in receiving message: {e}")