def calculate_score(filename):
    total_score = 0
    with open(filename, 'r') as file:
        for line in file:
            roll = int(line.strip())
            if roll == 6:
                score = 0
            elif roll % 2 == 0:
                score = roll * 2
            else:
                score = roll * 3
            total_score += score
    return total_score

rolls_file = 'rolls.txt'
score = calculate_score(rolls_file)
with open('score.txt', 'w') as score_file:
    score_file.write(str(score))