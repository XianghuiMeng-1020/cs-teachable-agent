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
    
    if not tickets:
        return None
    
    position = random.randint(0, total_length - 1)
    sum_length = 0
    
    for i, ticket in enumerate(tickets):
        sum_length += len(ticket)
        if sum_length > position:
            return names[i]
