import random

def get_lucky_winner(file_path):
    with open(file_path, 'r') as file:
        tickets = {}  
        total_length = 0  
        for line in file:
            name, ticket_number = line.strip().split(':')
            tickets[name] = ticket_number
            total_length += len(ticket_number)
    
    # Create a roulette wheel based on the ticket numbers' lengths
    roulette_positions = []
    for ticket_number in tickets.values():
        roulette_positions.extend([len(ticket_number)] * len(ticket_number))
    
    # Determine the winning position
    stopping_position = random.randint(0, total_length - 1)
    cumulative_length = 0
    winner = None

    for name, ticket_number in tickets.items():
        cumulative_length += len(ticket_number)
        if cumulative_length > stopping_position:
            winner = name
            break

    return winner
