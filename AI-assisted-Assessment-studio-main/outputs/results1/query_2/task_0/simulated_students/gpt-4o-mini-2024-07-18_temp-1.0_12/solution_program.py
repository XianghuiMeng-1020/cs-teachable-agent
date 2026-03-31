import random

def get_lucky_winner(file_path):
    participants = {}
    ticket_lengths = []

    with open(file_path, 'r') as file:
        for line in file:
            name, ticket = line.strip().split(':')
            participants[ticket] = name
            ticket_lengths.append(len(ticket))

    total_length = sum(ticket_lengths)
    position = random.randint(0, total_length - 1)

    current_position = 0
    for i, ticket in enumerate(ticket_lengths):
        current_position += ticket
        if current_position > position:
            winning_ticket = list(participants.keys())[i]
            return participants[winning_ticket]
