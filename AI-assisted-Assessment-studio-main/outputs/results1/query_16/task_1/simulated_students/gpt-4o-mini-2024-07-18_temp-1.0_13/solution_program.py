class CommsHandler:
    def __init__(self, factor=1):
        self.factor = factor

    def send_message(self, message):
        try:
            ascii_sum = sum(ord(char) for char in message)
            transmit_code = ascii_sum * self.factor
            return f'{message}#{transmit_code}'
        except Exception as e:
            raise ValueError('Error in sending message') from e

    def receive_message(self, received_message):
        try:
            message, code_str = received_message.rsplit('#', 1)
            calculated_code = sum(ord(char) for char in message) * self.factor
            if str(calculated_code) != code_str:
                raise ValueError('Transmit code mismatch')
            return message
        except ValueError:
            raise
        except Exception as e:
            raise ValueError('Error in receiving message') from e