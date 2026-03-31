import random


def get_lucky_winner(file_path):
    try:
        with open(file_path, 'r') as file:
            tickets = [line.strip().split(':') for line in file if line.strip()]
            participants = {name: ticket for name, ticket in tickets}
    except FileNotFoundError:
        return "Error: File not found."
    except Exception as e:
        return f"Error: {str(e)}"

    ticket_numbers = list(participants.values())
    lengths = list(map(len, ticket_numbers))
    wheel_circumference = sum(lengths)
    total_length = sum(lengths)

    if total_length == 0:
        return "No tickets found."

    random_position = random.randint(1, wheel_circumference)
    current_position = 0

    for name, ticket in participants.items():
        current_position += len(ticket)
        if current_position >= random_position:
            return name

    return "No winner found."