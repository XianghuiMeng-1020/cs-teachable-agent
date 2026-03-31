class CommsHandler:
    def __init__(self, transmit_code_factor=1):
        self.transmit_code_factor = transmit_code_factor

    def send_message(self, message):
        try:
            ascii_sum = sum(ord(char) for char in message)
            transmit_code = ascii_sum * self.transmit_code_factor
            return f'{message}#{transmit_code}'
        except Exception as e:
            raise ValueError(f'Error while sending message: {e}') 

    def receive_message(self, received_message):
        try:
            message, received_code = received_message.rsplit('#', 1)
            ascii_sum = sum(ord(char) for char in message)
            expected_code = ascii_sum * self.transmit_code_factor
            if int(received_code) == expected_code:
                return message
            else:
                raise ValueError('Transmit code mismatch')
        except Exception as e:
            raise ValueError(f'Error while receiving message: {e}')