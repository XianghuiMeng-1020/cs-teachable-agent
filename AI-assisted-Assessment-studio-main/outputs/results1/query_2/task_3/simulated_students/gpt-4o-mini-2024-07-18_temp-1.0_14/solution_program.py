def analyse_dice_game(input_file, output_file):
    with open(input_file, 'r') as infile:
        outcomes = infile.readlines()

    win_count = outcomes.count('win\n')
    lose_count = outcomes.count('lose\n')
    draw_count = outcomes.count('draw\n')

    with open(output_file, 'w') as outfile:
        outfile.write(f'Wins: {win_count}\n')
        outfile.write(f'Loses: {lose_count}\n')
        outfile.write(f'Draws: {draw_count}\n')