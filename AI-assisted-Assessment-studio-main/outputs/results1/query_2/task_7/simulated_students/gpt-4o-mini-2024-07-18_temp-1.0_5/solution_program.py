import random

def select_winner(input_filename, output_filename):
    with open(input_filename, 'r') as file:
        participants = file.readlines()
    winner = random.choice(participants).strip()  # Select a winner randomly
    with open(output_filename, 'w') as file:
        file.write(winner.split(' ')[0])  # Write only the name of the winner
