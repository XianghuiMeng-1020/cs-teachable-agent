def calculate_score(filename):
    total_score = 0
    with open(filename, 'r') as file:
        rolls = file.readlines()
        for roll in rolls:
            roll = int(roll.strip())
            if roll == 6:
                score = 0
            elif roll % 2 == 0:
                score = roll * 2
            else:
                score = roll * 3
            total_score += score
    return total_score

if __name__ == '__main__':
    score = calculate_score('rolls.txt')
    with open('score.txt', 'w') as output_file:
        output_file.write(str(score))