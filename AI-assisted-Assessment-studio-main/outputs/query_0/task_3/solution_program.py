def calculate_score(input_file):
    total_score = 0
    with open(input_file, 'r') as file:
        rolls = file.readlines()
    for roll in rolls:
        roll = int(roll.strip())
        if roll == 6:
            continue
        elif roll % 2 == 0:
            total_score += roll * 2
        else:
            total_score += roll * 3
    with open('score.txt', 'w') as file:
        file.write(str(total_score))