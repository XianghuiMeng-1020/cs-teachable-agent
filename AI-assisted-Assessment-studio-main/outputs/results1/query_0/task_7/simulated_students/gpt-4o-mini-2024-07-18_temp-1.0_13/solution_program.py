def game_of_chance(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    score = 10
    last_bet = 0

    for line in lines:
        line = line.strip()
        if line.isdigit():
            bet_amount = int(line)
            if bet_amount <= score:
                last_bet = bet_amount
            else:
                last_bet = 0
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