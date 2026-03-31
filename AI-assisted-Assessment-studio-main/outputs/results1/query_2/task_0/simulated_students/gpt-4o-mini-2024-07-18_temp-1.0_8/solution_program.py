import random

def get_lucky_winner(file_path):
    with open(file_path, 'r') as file:
        tickets = [line.strip().split(':') for line in file if line.strip()]
    
    ticket_dict = {name: number for name, number in tickets}
    ticket_lengths = [len(number) for number in ticket_dict.values()]
    total_length = sum(ticket_lengths)
    
    if total_length == 0:
        return None
    
    position = random.randint(0, total_length - 1)
    current_length = 0
    
    for name, number in ticket_dict.items():
        current_length += len(number)
        if current_length > position:
            return name
    
    return None