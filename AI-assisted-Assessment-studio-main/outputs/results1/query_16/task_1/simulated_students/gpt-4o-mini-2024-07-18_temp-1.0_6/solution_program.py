class CommsHandler:
    def __init__(self, factor):
        self.factor = factor

    def send_message(self, message):
        try:
            ascii_sum = sum(ord(char) for char in message)
            transmit_code = ascii_sum * self.factor
            return f'{message}#{transmit_code}'
        except Exception as e:
            raise RuntimeError('Error while sending message') from e

    def receive_message(self, received_message):
        try:
            message, transmit_code_str = received_message.rsplit('#', 1)
            transmit_code = int(transmit_code_str)
            calculated_code = sum(ord(char) for char in message) * self.factor
            if calculated_code != transmit_code:
                raise ValueError('Transmit code mismatch')
            return message
        except ValueError:
            raise ValueError('Transmit code mismatch')
        except Exception as e:
            raise RuntimeError('Error while receiving message') from e