def calculate_lucky_roll_score(input_file, output_file):
    total_score = 0
    with open(input_file, 'r') as f:
        rolls = f.readlines()
        for roll in rolls:
            roll_value = int(roll.strip())
            if roll_value == 6:
                score = 0
            elif roll_value % 2 == 0:
                score = roll_value * 2
            else:
                score = roll_value * 3
            total_score += score
    with open(output_file, 'w') as f:
        f.write(str(total_score))

calculate_lucky_roll_score('rolls.txt', 'score.txt')