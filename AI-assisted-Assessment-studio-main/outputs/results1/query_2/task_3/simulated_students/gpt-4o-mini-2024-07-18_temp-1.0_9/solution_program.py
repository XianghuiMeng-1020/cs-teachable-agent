def analyse_dice_game(input_file, output_file):
    wins = 0
    loses = 0
    draws = 0

    with open(input_file, 'r') as infile:
        for line in infile:
            result = line.strip()
            if result == 'win':
                wins += 1
            elif result == 'lose':
                loses += 1
            elif result == 'draw':
                draws += 1

    with open(output_file, 'w') as outfile:
        outfile.write(f'Wins: {wins}\n')
        outfile.write(f'Loses: {loses}\n')
        outfile.write(f'Draws: {draws}\n')