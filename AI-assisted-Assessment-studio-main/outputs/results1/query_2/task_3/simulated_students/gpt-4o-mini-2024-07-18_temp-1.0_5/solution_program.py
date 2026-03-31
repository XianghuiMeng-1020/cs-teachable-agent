def analyse_dice_game(input_file, output_file):
    win_count = 0
    lose_count = 0
    draw_count = 0

    with open(input_file, 'r') as infile:
        for line in infile:
            outcome = line.strip()
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