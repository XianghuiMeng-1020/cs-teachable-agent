class CommsHandler:
    def __init__(self, transmit_code_factor):
        self.transmit_code_factor = transmit_code_factor

    def send_message(self, message):
        try:
            ascii_sum = sum(ord(char) for char in message)
            transmit_code = ascii_sum * self.transmit_code_factor
            return f'{message}#{transmit_code}'
        except Exception as e:
            raise ValueError(f'Error sending message: {e}')

    def receive_message(self, message):
        try:
            message_content, code_str = message.rsplit('#', 1)
            calculated_code = sum(ord(char) for char in message_content) * self.transmit_code_factor
            if int(code_str) != calculated_code:
                raise ValueError('Transmit code mismatch')
            return message_content
        except ValueError as ve:
            raise ve
        except Exception as e:
            raise ValueError(f'Error receiving message: {e)'}