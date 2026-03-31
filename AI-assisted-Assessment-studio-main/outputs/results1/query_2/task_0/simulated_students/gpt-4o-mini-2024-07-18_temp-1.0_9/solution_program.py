import random

def get_lucky_winner(file_path):
    with open(file_path, 'r') as file:
        participants = {}
        for line in file:
            name, ticket = line.strip().split(':')
            participants[ticket] = name

    ticket_numbers = list(participants.keys())
    total_length = sum(len(ticket) for ticket in ticket_numbers)

    if total_length == 0:
        return None

    stopping_position = random.randint(0, total_length - 1)
    current_pos = 0

    for ticket in ticket_numbers:
        current_pos += len(ticket)
        if current_pos > stopping_position:
            return participants[ticket] 

    return None