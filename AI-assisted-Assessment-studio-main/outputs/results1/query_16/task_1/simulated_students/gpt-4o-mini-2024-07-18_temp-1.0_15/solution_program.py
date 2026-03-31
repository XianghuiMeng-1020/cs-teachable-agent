class CommsHandler:
    def __init__(self, factor=1):
        self.transmit_code_factor = factor

    def send_message(self, message):
        try:
            ascii_sum = sum(ord(char) for char in message)
            transmit_code = ascii_sum * self.transmit_code_factor
            return f'{message}#{transmit_code}'
        except Exception as e:
            raise ValueError(f'Error sending message: {str(e)}')

    def receive_message(self, received_message):
        try:
            message, code = received_message.rsplit('#', 1)
            ascii_sum = sum(ord(char) for char in message)
            calculated_code = ascii_sum * self.transmit_code_factor
            if str(calculated_code) != code:
                raise ValueError('Transmit code mismatch')
            return message
        except ValueError as ve:
            raise ve
        except Exception as e:
            raise ValueError(f'Error receiving message: {str(e)}')