def calculate_score(input_file, output_file):
    total_score = 0
    with open(input_file, 'r') as file:
        for line in file:
            roll = int(line.strip())
            if roll == 6:
                score = 0
            elif roll % 2 == 0:
                score = roll * 2
            else:
                score = roll * 3
            total_score += score
    with open(output_file, 'w') as file:
        file.write(str(total_score))

calculate_score('rolls.txt', 'score.txt')