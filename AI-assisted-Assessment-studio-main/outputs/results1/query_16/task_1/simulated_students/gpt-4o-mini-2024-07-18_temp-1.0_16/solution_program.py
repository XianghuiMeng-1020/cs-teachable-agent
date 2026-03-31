class CommsHandler:
    def __init__(self, transmit_code_factor=1):
        self.transmit_code_factor = transmit_code_factor

    def send_message(self, message):
        try:
            ascii_sum = sum(ord(char) for char in message)
            transmit_code = ascii_sum * self.transmit_code_factor
            return f'{message}#{transmit_code}'
        except Exception as e:
            raise e

    def receive_message(self, message_with_code):
        try:
            message, transmitted_code_str = message_with_code.rsplit('#', 1)
            transmitted_code = int(transmitted_code_str)
            ascii_sum = sum(ord(char) for char in message)
            expected_code = ascii_sum * self.transmit_code_factor
            if transmitted_code == expected_code:
                return message
            else:
                raise ValueError('Transmit code mismatch')
        except ValueError:
            raise ValueError('Transmit code mismatch')
        except Exception as e:
            raise e