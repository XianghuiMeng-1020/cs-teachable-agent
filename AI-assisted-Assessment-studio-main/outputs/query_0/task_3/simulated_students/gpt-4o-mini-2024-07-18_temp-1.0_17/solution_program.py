def calculate_score(input_file, output_file):
    total_score = 0
    with open(input_file, 'r') as infile:
        rolls = infile.readlines()
        for roll in rolls:
            number = int(roll.strip())
            if number == 6:
                score = 0
            elif number % 2 == 0:
                score = number * 2
            else:
                score = number * 3
            total_score += score
    with open(output_file, 'w') as outfile:
        outfile.write(str(total_score))

calculate_score('rolls.txt', 'score.txt')