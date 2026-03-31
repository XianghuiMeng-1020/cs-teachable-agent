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
    roulette_position = random.randint(0, total_length - 1)

    current_position = 0
    for index, ticket in enumerate(ticket_numbers):
        current_position += len(ticket)
        if current_position > roulette_position:
            return names[index]

    return None
