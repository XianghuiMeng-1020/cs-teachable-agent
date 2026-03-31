import random

def select_winner(input_filename, output_filename):
    participants = []
    with open(input_filename, 'r') as file:
        for line in file:
            participants.append(line.strip())

    winner = random.choice(participants)
    winner_name = winner.split()[0]

    with open(output_filename, 'w') as file:
        file.write(winner_name)
