def calculate_score(input_file, output_file):
    total_score = 0
    with open(input_file, 'r') as f:
        rolls = f.readlines()
    for roll in rolls:
        die_result = int(roll.strip())
        if die_result == 6:
            score = 0
        elif die_result % 2 == 0:
            score = die_result * 2
        else:
            score = die_result * 3
        total_score += score
    with open(output_file, 'w') as f:
        f.write(str(total_score))

calculate_score('rolls.txt', 'score.txt')