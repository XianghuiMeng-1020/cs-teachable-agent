def analyse_dice_game(input_file, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    win_count = sum(1 for line in lines if line.strip() == 'win')
    lose_count = sum(1 for line in lines if line.strip() == 'lose')
    draw_count = sum(1 for line in lines if line.strip() == 'draw')
    
    results = [f"Wins: {win_count}", f"Loses: {lose_count}", f"Draws: {draw_count}"]
    
    with open(output_file, 'w') as file:
        file.write("\n".join(results) + "\n")