import random

def select_winner(input_filename, output_filename):
    with open(input_filename, 'r') as file:
        participants = file.readlines()
    winner = random.choice(participants)
    winner_name = winner.split()[0]
    with open(output_filename, 'w') as file:
        file.write(winner_name)