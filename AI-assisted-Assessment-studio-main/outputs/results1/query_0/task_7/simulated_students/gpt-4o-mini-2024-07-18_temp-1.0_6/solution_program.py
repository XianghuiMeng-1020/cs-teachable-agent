def game_of_chance(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    score = 10
    bet = 0

    for line in lines:
        line = line.strip()
        if line.isdigit():
            bet = int(line)
        elif line == 'win':
            score += bet
        elif line == 'lose':
            if bet <= score:
                score -= bet
        elif line == 'draw':
            continue  # no change in score

    with open('result.txt', 'w') as result_file:
        result_file.write(str(score))