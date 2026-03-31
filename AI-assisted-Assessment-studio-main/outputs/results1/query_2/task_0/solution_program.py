def get_lucky_winner(file_path):
    with open(file_path, 'r') as file:
        participants = file.readlines()
    if not participants:
        return None
    tickets = []
    names = []
    for entry in participants:
        name, ticket_number = entry.strip().split(':')
        names.append(name)
        tickets.append(len(ticket_number))  
    total_length = sum(tickets)
    winner_position = total_length % len(tickets)
    return names[winner_position]