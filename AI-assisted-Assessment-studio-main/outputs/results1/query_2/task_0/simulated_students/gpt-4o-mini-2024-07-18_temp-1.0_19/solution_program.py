import random


def get_lucky_winner(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    tickets = []
    names = []

    for line in lines:
        name, ticket = line.strip().split(':')
        names.append(name)
        tickets.append(ticket)

    total_length = sum(len(ticket) for ticket in tickets)
    stopping_position = random.randint(0, total_length - 1)

    current_position = 0
    for i, ticket in enumerate(tickets):
        current_position += len(ticket)
        if current_position > stopping_position:
            return names[i]

    return None