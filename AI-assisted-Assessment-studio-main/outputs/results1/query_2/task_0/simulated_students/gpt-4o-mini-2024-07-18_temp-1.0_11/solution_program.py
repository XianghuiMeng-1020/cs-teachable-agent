import random

def get_lucky_winner(file_path):
    try:
        with open(file_path, 'r') as file:
            participants = []
            total_length = 0
            # Read lines and process ticket information
            for line in file:
                name, ticket_number = line.strip().split(':')
                participants.append((name, ticket_number))
                total_length += len(ticket_number)

            if total_length == 0:
                return None

            # Determine the stopping position
            stop_position = random.randint(0, total_length - 1)

            # Traverse through the ticket list to find the winner
            current_position = 0
            for name, ticket_number in participants:
                current_position += len(ticket_number)
                if current_position > stop_position:
                    return name
    except Exception as e:
        return str(e)

