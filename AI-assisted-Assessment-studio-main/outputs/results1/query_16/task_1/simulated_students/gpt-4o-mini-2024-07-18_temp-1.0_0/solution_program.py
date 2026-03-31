class CommsHandler:
    def __init__(self, transmit_code_factor):
        self.transmit_code_factor = transmit_code_factor

    def send_message(self, message):
        try:
            ascii_sum = sum(ord(char) for char in message)
            transmit_code = ascii_sum * self.transmit_code_factor
            return f'{message}#{transmit_code}'
        except Exception as e:
            raise RuntimeError('Error while sending message') from e

    def receive_message(self, message_with_code):
        try:
            message, code = message_with_code.rsplit('#', 1)
            ascii_sum = sum(ord(char) for char in message)
            expected_code = ascii_sum * self.transmit_code_factor
            if int(code) != expected_code:
                raise ValueError('Transmit code mismatch')
            return message
        except ValueError:
            raise
        except Exception as e:
            raise RuntimeError('Error while receiving message') from e