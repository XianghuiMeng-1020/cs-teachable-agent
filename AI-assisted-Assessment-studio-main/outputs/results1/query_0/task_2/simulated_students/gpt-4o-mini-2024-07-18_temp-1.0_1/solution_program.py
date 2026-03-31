def game_of_chance(input_file, ticket_number, draw_number):
    with open(input_file, 'r') as file:
        tickets = file.read().splitlines()
    
    if ticket_number in tickets:
        ticket_length = len(ticket_number)
        draw_length = len(draw_number)
        
        if ticket_length > draw_length:
            return "JACKPOT"
        elif ticket_length == draw_length:
            return "WIN"
        else:
            return "NO WIN"
    else:
        return "TICKET NOT FOUND"