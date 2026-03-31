def calculate_score_from_rolls(input_file, output_file):
    with open(input_file, 'r') as file:
        rolls = [int(line.strip()) for line in file.readlines()]

    total_score = 0
    for roll in rolls:
        if roll == 6:
            score = 0
        elif roll % 2 == 0:
            score = roll * 2
        else:
            score = roll * 3
        total_score += score

    with open(output_file, 'w') as file:
        file.write(str(total_score))

calculate_score_from_rolls('rolls.txt', 'score.txt')