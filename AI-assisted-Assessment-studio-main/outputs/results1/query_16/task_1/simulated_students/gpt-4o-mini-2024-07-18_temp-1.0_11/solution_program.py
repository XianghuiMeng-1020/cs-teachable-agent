class CommsHandler:
    def __init__(self, factor):
        self.factor = factor

    def send_message(self, message):
        try:
            ascii_sum = sum(ord(char) for char in message)
            transmit_code = ascii_sum * self.factor
            return f'{message}#{transmit_code}'
        except Exception as e:
            raise ValueError('Error sending message') from e

    def receive_message(self, message_with_code):
        try:
            message, code_str = message_with_code.rsplit('#', 1)
            expected_code = sum(ord(char) for char in message) * self.factor
            if int(code_str) == expected_code:
                return message
            else:
                raise ValueError('Transmit code mismatch')
        except Exception as e:
            raise ValueError('Error receiving message') from e