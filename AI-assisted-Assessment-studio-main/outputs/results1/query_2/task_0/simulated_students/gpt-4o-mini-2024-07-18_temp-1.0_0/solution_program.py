import random

def get_lucky_winner(file_path):
    with open(file_path, 'r') as file:
        tickets = [line.strip().split(':') for line in file]

    names = [ticket[0] for ticket in tickets]
    ticket_numbers = [ticket[1] for ticket in tickets]

    total_length = sum(len(ticket) for ticket in ticket_numbers)
    wheel_position = random.randint(1, total_length)  

    current_position = 0
    for ticket_number in ticket_numbers:
        current_position += len(ticket_number)
        if current_position >= wheel_position:
            return names[ticket_numbers.index(ticket_number)]
    
    return None