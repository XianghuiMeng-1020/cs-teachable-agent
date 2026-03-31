def game_of_chance(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    score = 10
    last_bet = 0

    for line in lines:
        line = line.strip()
        if line.isdigit():
            bet = int(line)
            if bet <= score:
                last_bet = bet
        elif line == 'win':
            score += last_bet
        elif line == 'lose':
            score -= last_bet
        elif line == 'draw':
            continue

    with open('result.txt', 'w') as result_file:
        result_file.write(str(score))
