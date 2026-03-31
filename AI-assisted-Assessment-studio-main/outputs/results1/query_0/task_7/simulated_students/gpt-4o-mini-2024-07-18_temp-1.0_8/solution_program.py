def game_of_chance(filename):
    score = 10
    current_bet = 0
    actions = []

    with open(filename, 'r') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        if line.isdigit():
            bet_amount = int(line)
            if bet_amount <= score:
                current_bet = bet_amount
            else:
                current_bet = 0  # ignore the bet as it is higher than the score
        elif line == 'win':
            score += current_bet
            current_bet = 0
        elif line == 'lose':
            score -= current_bet
            current_bet = 0
        elif line == 'draw':
            current_bet = 0  # reset, but score remains the same

    with open('result.txt', 'w') as result_file:
        result_file.write(str(score))