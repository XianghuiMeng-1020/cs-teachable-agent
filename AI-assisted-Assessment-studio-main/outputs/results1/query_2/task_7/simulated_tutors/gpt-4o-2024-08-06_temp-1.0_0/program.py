import random


def select_winner(input_filename, output_filename):
    with open(input_filename, 'r') as infile:
        lines = infile.readlines()

    if not lines:  # Handle case when there are no participants
        with open(output_filename, 'w') as outfile:
            outfile.write('')
            return

    winner_line = random.choice(lines).strip()
    winner_name = winner_line.split(' ')[0]  # The participant's name is the first word

    with open(output_filename, 'w') as outfile:
        outfile.write(winner_name)
