class CommsHandler:
    def __init__(self, factor=1):
        self.transmit_code_factor = factor

    def send_message(self, message):
        try:
            ascii_sum = sum(ord(char) for char in message)
            transmit_code = ascii_sum * self.transmit_code_factor
            return f'{message}#{transmit_code}'
        except Exception as e:
            raise ValueError(f'Error in sending message: {str(e)}')

    def receive_message(self, message_with_code):
        try:
            message, code_str = message_with_code.split('#')
            calculated_code = sum(ord(char) for char in message) * self.transmit_code_factor
            if int(code_str) == calculated_code:
                return message
            else:
                raise ValueError('Transmit code mismatch')
        except ValueError:
            raise ValueError('Transmit code mismatch')
        except Exception as e:
            raise ValueError(f'Error in receiving message: {str(e)}')