def game_of_chance(filename):
    score = 10
    last_bet = 0
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line.isdigit():
                bet = int(line)
                if bet <= score:
                    last_bet = bet
            elif line == 'win':
                score += last_bet
                last_bet = 0
            elif line == 'lose':
                score -= last_bet
                last_bet = 0
            elif line == 'draw':
                last_bet = 0
    with open('result.txt', 'w') as result_file:
        result_file.write(str(score))