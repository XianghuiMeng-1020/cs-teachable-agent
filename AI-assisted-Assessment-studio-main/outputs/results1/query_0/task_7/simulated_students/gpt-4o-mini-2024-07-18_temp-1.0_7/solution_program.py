def game_of_chance(filename):
    score = 10
    last_bet = 0
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line.isdigit():
                bet_amount = int(line)
                if bet_amount <= score:
                    last_bet = bet_amount
            elif line == 'win':
                score += last_bet
            elif line == 'lose':
                score -= last_bet
            elif line == 'draw':
                pass
    with open('result.txt', 'w') as result_file:
        result_file.write(str(score))