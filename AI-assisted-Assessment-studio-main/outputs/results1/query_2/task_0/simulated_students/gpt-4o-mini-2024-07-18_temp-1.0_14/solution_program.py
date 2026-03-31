import random


def get_lucky_winner(file_path):
    with open(file_path, 'r') as file:
        tickets = {}  
        total_length = 0
        
        for line in file:
            name, ticket_number = line.strip().split(':')
            tickets[ticket_number] = name
            total_length += len(ticket_number)
            
    # Generate a stopping position by generating a random number
    # and taking modulus by total_length
    stopping_position = random.randint(1, total_length)
    current_position = 0
    
    for ticket_number in tickets:
        current_position += len(ticket_number)
        if current_position >= stopping_position:
            return tickets[ticket_number]
    
    return None