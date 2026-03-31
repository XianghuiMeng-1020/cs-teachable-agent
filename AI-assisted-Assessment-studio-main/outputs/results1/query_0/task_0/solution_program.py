def evaluate_lottery_tickets(input_file, output_file, winning_number):
    with open(input_file, 'r') as f:
        lines = f.readlines()
    count_evaluated = len(lines)
    winners = []
    for line in lines:
        ticket_number = line.strip()
        if ticket_number == winning_number:
            winners.append(ticket_number)
    with open(output_file, 'w') as f:
        f.write(f'Tickets evaluated: {count_evaluated}\n')
        if winners:
            f.write(f'Winners: {len(winners)}\n')
            for winner in winners:
                f.write(f'Winner: {winner}\n')
        else:
            f.write('No winners\n')