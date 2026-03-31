import random

def select_winner(input_filename, output_filename):
    with open(input_filename, 'r') as file:
        participants = file.readlines()

    winner_line = random.choice(participants)
    winner_name = winner_line.split()[0]

    with open(output_filename, 'w') as outfile:
        outfile.write(winner_name)