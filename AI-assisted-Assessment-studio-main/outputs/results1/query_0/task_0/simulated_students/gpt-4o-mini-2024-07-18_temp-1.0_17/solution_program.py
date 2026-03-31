def evaluate_lottery_tickets(input_file, output_file, winning_number):
    with open(input_file, 'r') as infile:
        tickets = infile.readlines()

    total_tickets = len(tickets)
    winners = []

    for ticket in tickets:
        ticket = ticket.strip()  # Remove any leading/trailing whitespace
        if ticket == winning_number:
            winners.append(ticket)

    with open(output_file, 'w') as outfile:
        outfile.write(f'Tickets evaluated: {total_tickets}\n')
        outfile.write(f'Winners: {len(winners)}\n')
        if winners:
            for winner in winners:
                outfile.write(f'Winner: {winner}\n')
        else:
            outfile.write('No winners\n')