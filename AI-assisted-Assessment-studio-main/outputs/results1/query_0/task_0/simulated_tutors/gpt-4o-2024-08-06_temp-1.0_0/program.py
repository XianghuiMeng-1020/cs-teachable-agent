import random

# Function to evaluate lottery tickets

def evaluate_lottery_tickets(input_file, output_file, winning_number):
    # Initialize counters
    total_tickets = 0
    winners = []
    
    # Open the input file and read each ticket
    with open(input_file, 'r') as file:
        tickets = file.readlines()

    # Count total tickets and check for winners
    for ticket in tickets:
        ticket = ticket.strip()  # Remove newline characters
        if ticket == winning_number:
            winners.append(ticket)
        total_tickets += 1

    # Open the output file to write results
    with open(output_file, 'w') as file:
        file.write(f"Tickets evaluated: {total_tickets}\n")
        
        # Check if there are any winners
        if winners:
            file.write(f"Winners: {len(winners)}\n")
            for winner in winners:
                file.write(f"Winner: {winner}\n")
        else:
            file.write("No winners\n")

# Example usage of the program:
evaluate_lottery_tickets('input.txt', 'output.txt', '632')