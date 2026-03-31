import random

def get_lucky_winner(file_path):
    with open(file_path, 'r') as file:
        tickets = [line.strip().split(':') for line in file]
    participants = {name: ticket for name, ticket in tickets}
    ticket_numbers = list(participants.values())

    total_length = sum(len(ticket) for ticket in ticket_numbers)
    position = random.randint(0, total_length - 1)

    current_position = 0
    for name, ticket in participants.items():
        current_position += len(ticket)
        if current_position > position:
            return name
    return None