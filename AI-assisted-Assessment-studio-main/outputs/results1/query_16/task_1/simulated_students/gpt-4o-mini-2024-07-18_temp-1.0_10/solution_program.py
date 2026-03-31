class CommsHandler:
    def __init__(self, factor):
        self.factor = factor

    def send_message(self, message):
        try:
            ascii_sum = sum(ord(char) for char in message)
            transmit_code = ascii_sum * self.factor
            return f'{message}#{transmit_code}'
        except Exception as e:
            raise ValueError(f'Error sending message: {str(e)}')

    def receive_message(self, message_with_code):
        try:
            message, received_code = message_with_code.rsplit('#', 1)
            ascii_sum = sum(ord(char) for char in message)
            expected_code = ascii_sum * self.factor
            if expected_code != int(received_code):
                raise ValueError('Transmit code mismatch')
            return message
        except ValueError:
            raise
        except Exception as e:
            raise ValueError(f'Error receiving message: {str(e)}')