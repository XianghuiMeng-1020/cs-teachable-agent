def game_of_chance(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    score = 10
    current_bet = 0

    for line in lines:
        line = line.strip()
        if line.isdigit():
            bet_amount = int(line)
            if bet_amount <= score:
                current_bet = bet_amount
        elif line == 'win':
            score += current_bet
            current_bet = 0  # Reset current bet after action
        elif line == 'lose':
            score -= current_bet
            current_bet = 0  # Reset current bet after action
        elif line == 'draw':
            continue  # No score change

    with open('result.txt', 'w') as result_file:
        result_file.write(str(score))