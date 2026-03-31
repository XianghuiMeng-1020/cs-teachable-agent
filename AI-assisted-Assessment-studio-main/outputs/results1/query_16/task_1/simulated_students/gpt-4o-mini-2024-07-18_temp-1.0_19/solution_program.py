class CommsHandler:
    def __init__(self, factor):
        self.factor = factor

    def send_message(self, message):
        try:
            ascii_sum = sum(ord(char) for char in message)
            transmit_code = ascii_sum * self.factor
            return f'{message}#{transmit_code}'
        except Exception as e:
            print(f'Error sending message: {e}')  

    def receive_message(self, message_with_code):
        try:
            message, transmit_code_str = message_with_code.rsplit('#', 1)
            ascii_sum = sum(ord(char) for char in message)
            calculated_code = ascii_sum * self.factor
            if str(calculated_code) == transmit_code_str:
                return message
            else:
                raise ValueError('Transmit code mismatch')
        except ValueError as ve:
            raise ve
        except Exception as e:
            print(f'Error receiving message: {e)'}