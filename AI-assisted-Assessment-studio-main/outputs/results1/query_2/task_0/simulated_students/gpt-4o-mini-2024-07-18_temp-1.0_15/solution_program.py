import random


def get_lucky_winner(file_path):
    tickets = []
    with open(file_path, 'r') as file:
        for line in file:
            name, ticket_number = line.strip().split(':')
            tickets.append((name, ticket_number))

    # Calculate total length of ticket numbers
    if not tickets:
        return None  # No tickets available

    ticket_lengths = [len(ticket) for _, ticket in tickets]
    total_length = sum(ticket_lengths)
    position = random.randint(0, total_length - 1)

    # Traverse ticket lengths to find the winner
    current_position = 0
    for name, ticket in tickets:
        next_position = current_position + len(ticket)
        if current_position <= position < next_position:
            return name  # Return the winner's name
        current_position = next_position

    return None  # If somehow no winner is found