import random

def select_winner(input_filename, output_filename):
    with open(input_filename, 'r') as file:
        participants = file.readlines()
    # Randomly select a winner from the participants
    winner = random.choice(participants)
    # Split the winner line to get the name
    winner_name = winner.split()[0]
    # Write the winner's name to the output file
    with open(output_filename, 'w') as file:
        file.write(winner_name + '\n')