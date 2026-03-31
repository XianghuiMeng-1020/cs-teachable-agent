class CommsHandler:
    def __init__(self, factor=1):
        self.transmit_code_factor = factor

    def send_message(self, message):
        try:
            ascii_sum = sum(ord(char) for char in message)
            transmit_code = ascii_sum * self.transmit_code_factor
            return f'{message}#{transmit_code}'
        except Exception as e:
            raise RuntimeError(f'Error sending message: {str(e)}')

    def receive_message(self, transmitted_message):
        try:
            message, code = transmitted_message.rsplit('#', 1)
            ascii_sum = sum(ord(char) for char in message)
            expected_code = ascii_sum * self.transmit_code_factor
            if int(code) != expected_code:
                raise ValueError('Transmit code mismatch')
            return message
        except ValueError:
            raise ValueError('Transmit code mismatch')
        except Exception as e:
            raise RuntimeError(f'Error receiving message: {str(e)}')