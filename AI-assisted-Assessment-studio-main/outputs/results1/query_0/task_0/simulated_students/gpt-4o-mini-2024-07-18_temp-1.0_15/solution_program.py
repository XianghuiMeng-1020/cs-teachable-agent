import random

def evaluate_lottery_tickets(input_file, output_file, winning_number):
    with open(input_file, 'r') as infile:
        tickets = infile.readlines()
        tickets = [ticket.strip() for ticket in tickets]
    total_tickets = len(tickets)
    winners = [ticket for ticket in tickets if ticket == winning_number]

    with open(output_file, 'w') as outfile:
        outfile.write(f'Tickets evaluated: {total_tickets}\n')
        outfile.write(f'Winners: {len(winners)}\n')
        if winners:
            for winner in winners:
                outfile.write(f'Winner: {winner}\n')
        else:
            outfile.write('No winners\n')