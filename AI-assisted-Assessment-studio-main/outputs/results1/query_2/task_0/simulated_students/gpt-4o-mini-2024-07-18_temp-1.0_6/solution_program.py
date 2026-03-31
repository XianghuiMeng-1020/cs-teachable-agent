import random

def get_lucky_winner(file_path):
    tickets = []
    names = []
    total_length = 0
    
    with open(file_path, 'r') as file:
        for line in file:
            name, ticket = line.strip().split(':')
            tickets.append(ticket)
            names.append(name)
            total_length += len(ticket)
    
    if total_length == 0:
        return None
    
    stopping_position = random.randint(0, total_length - 1)
    position = 0
    
    for i, ticket in enumerate(tickets):
        ticket_length = len(ticket)
        position += ticket_length
        if position > stopping_position:
            return names[i]

    return None
