import random

def select_winner(input_filename, output_filename):
    with open(input_filename, 'r') as file:
        lines = file.readlines()
    if not lines:
        winner = ''
    else:
        winner = random.choice(lines).split()[0]
    with open(output_filename, 'w') as file:
        file.write(winner + '\n')