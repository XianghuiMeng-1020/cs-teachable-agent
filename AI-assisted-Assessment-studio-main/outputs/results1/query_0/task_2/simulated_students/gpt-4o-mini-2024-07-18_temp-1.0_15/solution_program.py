def game_of_chance(input_file, ticket_number, draw_number):
    with open(input_file, 'r') as file:
        tickets = file.read().splitlines()
    
    if ticket_number not in tickets:
        return "TICKET NOT FOUND"
    
    len_ticket = len(ticket_number)
    len_draw = len(draw_number)
    
    if len_ticket > len_draw:
        return "JACKPOT"
    elif len_ticket == len_draw:
        return "WIN"
    else:
        return "NO WIN"