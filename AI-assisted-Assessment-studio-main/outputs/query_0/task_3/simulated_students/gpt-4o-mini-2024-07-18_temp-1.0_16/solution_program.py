def calculate_score_from_rolls(input_file, output_file):
    total_score = 0
    with open(input_file, 'r') as file:
        rolls = file.readlines()
        for roll in rolls:
            roll_value = int(roll.strip())
            if roll_value == 6:
                score = 0
            elif roll_value % 2 == 0:
                score = roll_value * 2
            else:
                score = roll_value * 3
            total_score += score
    with open(output_file, 'w') as file:
        file.write(str(total_score))

calculate_score_from_rolls('rolls.txt', 'score.txt')