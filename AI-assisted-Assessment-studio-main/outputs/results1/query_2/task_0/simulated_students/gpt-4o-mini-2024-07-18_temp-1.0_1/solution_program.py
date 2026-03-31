import random


def get_lucky_winner(file_path):
    tickets = []
    total_length = 0

    with open(file_path, 'r') as file:
        for line in file:
            name, ticket = line.strip().split(':')
            tickets.append((name, ticket))
            total_length += len(ticket)

    if total_length == 0:
        return None

    # Pick the stopping position on the roulette wheel
    stopping_position = random.randint(0, total_length - 1)
    current_position = 0

    for name, ticket in tickets:
        current_position += len(ticket)
        if current_position > stopping_position:
            return name

    return None