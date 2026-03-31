def analyse_dice_game(input_file, output_file):
    with open(input_file, 'r') as infile:
        outcomes = infile.readlines()

    count_wins = outcomes.count('win\n')
    count_loses = outcomes.count('lose\n')
    count_draws = outcomes.count('draw\n')

    with open(output_file, 'w') as outfile:
        outfile.write(f'Wins: {count_wins}\n')
        outfile.write(f'Loses: {count_loses}\n')
        outfile.write(f'Draws: {count_draws}\n')