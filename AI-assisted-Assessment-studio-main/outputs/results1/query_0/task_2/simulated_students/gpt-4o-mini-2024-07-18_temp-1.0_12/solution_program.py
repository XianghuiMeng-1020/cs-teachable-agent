def game_of_chance(input_file, ticket_number, draw_number):
    with open(input_file, 'r') as file:
        tickets = file.read().splitlines()
    if ticket_number in tickets:
        if len(ticket_number) > len(draw_number):
            return "JACKPOT"
        elif len(ticket_number) == len(draw_number):
            return "WIN"
        else:
            return "NO WIN"
    else:
        return "TICKET NOT FOUND"