def analyse_dice_game(input_file, output_file):
    with open(input_file, 'r') as infile:
        outcomes = infile.readlines()

    win_count = 0
    lose_count = 0
    draw_count = 0

    for outcome in outcomes:
        outcome = outcome.strip()
        if outcome == 'win':
            win_count += 1
        elif outcome == 'lose':
            lose_count += 1
        elif outcome == 'draw':
            draw_count += 1

    with open(output_file, 'w') as outfile:
        outfile.write(f'Wins: {win_count}\n')
        outfile.write(f'Loses: {lose_count}\n')
        outfile.write(f'Draws: {draw_count}\n')