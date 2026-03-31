import os

def get_lucky_winner(file_path):
    if not os.path.exists(file_path):
        return None
    
    ticket_dict = {}
    total_length = 0
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if ':' in line:
                name, ticket_number = line.split(':')
                ticket_dict[name] = ticket_number
                total_length += len(ticket_number)

    if not ticket_dict:
        return None

    position = 0
    for name, ticket_number in ticket_dict.items():
        position = (position + len(ticket_number)) % total_length

    # At this point, the position's round completes the circle
    # We need to find the key at the position
    current_position = 0
    for name, ticket_number in ticket_dict.items():
        current_position = (current_position + len(ticket_number)) % total_length
        if current_position >= position:
            return name
    
    return None