class CommsHandler:
    def __init__(self, factor=1):
        self.factor = factor

    def send_message(self, message):
        ascii_sum = sum(ord(char) for char in message)
        transmit_code = ascii_sum * self.factor
        return f"{message}#{transmit_code}"

    def receive_message(self, message_with_code):
        try:
            message, code = message_with_code.rsplit('#', 1)
            code = int(code)
            expected_code = sum(ord(char) for char in message) * self.factor
            if expected_code != code:
                raise ValueError("Transmit code mismatch")
            return message
        except ValueError:
            raise ValueError("Transmit code mismatch")
        except Exception as e:
            raise ValueError("Invalid message format")