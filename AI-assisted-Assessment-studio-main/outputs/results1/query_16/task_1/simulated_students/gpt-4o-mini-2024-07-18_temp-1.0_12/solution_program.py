class CommsHandler:
    def __init__(self, factor=1):
        self.factor = factor

    def send_message(self, message):
        try:
            ascii_sum = sum(ord(char) for char in message)
            transmit_code = ascii_sum * self.factor
            return f'{message}#{transmit_code}'
        except Exception as e:
            raise RuntimeError('Error sending message') from e

    def receive_message(self, message_with_code):
        try:
            message, transmit_code_str = message_with_code.rsplit('#', 1)
            transmit_code = int(transmit_code_str)
            calculated_code = sum(ord(char) for char in message) * self.factor
            if calculated_code != transmit_code:
                raise ValueError('Transmit code mismatch')
            return message
        except ValueError as ve:
            raise ve
        except Exception as e:
            raise RuntimeError('Error receiving message') from e