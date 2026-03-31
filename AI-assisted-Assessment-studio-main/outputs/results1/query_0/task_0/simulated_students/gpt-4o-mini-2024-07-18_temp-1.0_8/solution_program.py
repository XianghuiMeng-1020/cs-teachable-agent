import random

def evaluate_lottery_tickets(input_file, output_file, winning_number):
    with open(input_file, 'r') as file:
        tickets = [line.strip() for line in file.readlines()]  # Read all lines
    total_tickets = len(tickets)
    winners = [ticket for ticket in tickets if ticket == winning_number]  # Find winners
    number_of_winners = len(winners)

    with open(output_file, 'w') as file:
        file.write(f'Tickets evaluated: {total_tickets}\n')
        file.write(f'Winners: {number_of_winners}\n')
        if number_of_winners > 0:
            for winner in winners:
                file.write(f'Winner: {winner}\n')
        else:
            file.write('No winners\n')