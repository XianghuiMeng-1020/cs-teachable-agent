import random


def get_lucky_winner(file_path):
    with open(file_path, 'r') as file:
        participants = file.readlines()

    ticket_numbers = []
    names = []

    for line in participants:
        name, ticket_number = line.strip().split(':')
        names.append(name)
        ticket_numbers.append(ticket_number)  

    total_length = sum(len(ticket) for ticket in ticket_numbers)

    if total_length == 0:
        return None

    current_position = 0
    for ticket in ticket_numbers:
        current_position += len(ticket)
        if current_position >= total_length:
            current_position -= total_length

    winner_index = current_position % len(ticket_numbers)
    return names[winner_index]