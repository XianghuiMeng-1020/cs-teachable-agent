def analyse_dice_game(input_file, output_file):
    with open(input_file, 'r') as infile:
        outcomes = infile.readlines()

    wins = outcomes.count('win\n')
    loses = outcomes.count('lose\n')
    draws = outcomes.count('draw\n')

    with open(output_file, 'w') as outfile:
        outfile.write(f"Wins: {wins}\n")
        outfile.write(f"Loses: {loses}\n")
        outfile.write(f"Draws: {draws}\n")